---
title: "Guides: Self-Hosting | Next.js"
source: "https://nextjs.org/docs/app/guides/self-hosting"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn how to self-host your Next.js application on a Node.js server, Docker image, or static HTML files (static exports)."
tags:
  - "clippings"
---
## How to self-host your Next.js application

When [deploying](https://nextjs.org/docs/app/getting-started/deploying) your Next.js app, you may want to configure how different features are handled based on your infrastructure.

> **🎥 Watch:** Learn more about self-hosting Next.js → [YouTube (45 minutes)](https://www.youtube.com/watch?v=sIVL4JMqRfc).

## Image Optimization

[Image Optimization](https://nextjs.org/docs/app/api-reference/components/image) through `next/image` works self-hosted with zero configuration when deploying using `next start`. If you would prefer to have a separate service to optimize images, you can [configure an image loader](https://nextjs.org/docs/app/api-reference/components/image#loader).

Image Optimization can be used with a [static export](https://nextjs.org/docs/app/guides/static-exports#image-optimization) by defining a custom image loader in `next.config.js`. Note that images are optimized at runtime, not during the build.

> **Good to know:**
> 
> - On glibc-based Linux systems, Image Optimization may require [additional configuration](https://sharp.pixelplumbing.com/install#linux-memory-allocator) to prevent excessive memory usage.
> - Learn more about the [caching behavior of optimized images](https://nextjs.org/docs/app/api-reference/components/image#minimumcachettl) and how to configure the TTL.
> - You can also [disable Image Optimization](https://nextjs.org/docs/app/api-reference/components/image#unoptimized) and still retain other benefits of using `next/image` if you prefer. For example, if you are optimizing images yourself separately.

## Middleware

[Middleware](https://nextjs.org/docs/app/api-reference/file-conventions/middleware) works self-hosted with zero configuration when deploying using `next start`. Since it requires access to the incoming request, it is not supported when using a [static export](https://nextjs.org/docs/app/guides/static-exports).

Middleware uses the [Edge runtime](https://nextjs.org/docs/app/api-reference/edge), a subset of all available Node.js APIs to help ensure low latency, since it may run in front of every route or asset in your application. If you do not want this, you can use the [full Node.js runtime](https://nextjs.org/blog/next-15-2#nodejs-middleware-experimental) to run Middleware.

If you are looking to add logic (or use an external package) that requires all Node.js APIs, you might be able to move this logic to a [layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout) as a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components). For example, checking [headers](https://nextjs.org/docs/app/api-reference/functions/headers) and [redirecting](https://nextjs.org/docs/app/api-reference/functions/redirect). You can also use headers, cookies, or query parameters to [redirect](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#header-cookie-and-query-matching) or [rewrite](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites#header-cookie-and-query-matching) through `next.config.js`. If that does not work, you can also use a [custom server](https://nextjs.org/docs/pages/guides/custom-server).

## Environment Variables

Next.js can support both build time and runtime environment variables.

**By default, environment variables are only available on the server**. To expose an environment variable to the browser, it must be prefixed with `NEXT_PUBLIC_`. However, these public environment variables will be inlined into the JavaScript bundle during `next build`.

You safely read environment variables on the server during dynamic rendering.

This allows you to use a singular Docker image that can be promoted through multiple environments with different values.

> **Good to know:**
> 
> - You can run code on server startup using the [`register` function](https://nextjs.org/docs/app/guides/instrumentation).
> - We do not recommend using the [runtimeConfig](https://nextjs.org/docs/pages/api-reference/config/next-config-js/runtime-configuration) option, as this does not work with the standalone output mode. Instead, we recommend [incrementally adopting](https://nextjs.org/docs/app/guides/migrating/app-router-migration) the App Router.

## Caching and ISR

Next.js can cache responses, generated static pages, build outputs, and other static assets like images, fonts, and scripts.

Caching and revalidating pages (with [Incremental Static Regeneration](https://nextjs.org/docs/app/guides/incremental-static-regeneration)) use the **same shared cache**. By default, this cache is stored to the filesystem (on disk) on your Next.js server. **This works automatically when self-hosting** using both the Pages and App Router.

You can configure the Next.js cache location if you want to persist cached pages and data to durable storage, or share the cache across multiple containers or instances of your Next.js application.

### Automatic Caching

- Next.js sets the `Cache-Control` header of `public, max-age=31536000, immutable` to truly immutable assets. It cannot be overridden. These immutable files contain a SHA-hash in the file name, so they can be safely cached indefinitely. For example, [Static Image Imports](https://nextjs.org/docs/app/getting-started/images#local-images). You can [configure the TTL](https://nextjs.org/docs/app/api-reference/components/image#minimumcachettl) for images.
- Incremental Static Regeneration (ISR) sets the `Cache-Control` header of `s-maxage: <revalidate in getStaticProps>, stale-while-revalidate`. This revalidation time is defined in your [`getStaticProps` function](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) in seconds. If you set `revalidate: false`, it will default to a one-year cache duration.
- Dynamically rendered pages set a `Cache-Control` header of `private, no-cache, no-store, max-age=0, must-revalidate` to prevent user-specific data from being cached. This applies to both the App Router and Pages Router. This also includes [Draft Mode](https://nextjs.org/docs/app/guides/draft-mode).

### Static Assets

If you want to host static assets on a different domain or CDN, you can use the `assetPrefix` [configuration](https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix) in `next.config.js`. Next.js will use this asset prefix when retrieving JavaScript or CSS files. Separating your assets to a different domain does come with the downside of extra time spent on DNS and TLS resolution.

[Learn more about `assetPrefix`](https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix).

### Configuring Caching

By default, generated cache assets will be stored in memory (defaults to 50mb) and on disk. If you are hosting Next.js using a container orchestration platform like Kubernetes, each pod will have a copy of the cache. To prevent stale data from being shown since the cache is not shared between pods by default, you can configure the Next.js cache to provide a cache handler and disable in-memory caching.

To configure the ISR/Data Cache location when self-hosting, you can configure a custom handler in your `next.config.js` file:

next.config.js

```
module.exports = {

  cacheHandler: require.resolve('./cache-handler.js'),

  cacheMaxMemorySize: 0, // disable default in-memory caching

}
```

Then, create `cache-handler.js` in the root of your project, for example:

cache-handler.js

```
const cache = new Map()

 

module.exports = class CacheHandler {

  constructor(options) {

    this.options = options

  }

 

  async get(key) {

    // This could be stored anywhere, like durable storage

    return cache.get(key)

  }

 

  async set(key, data, ctx) {

    // This could be stored anywhere, like durable storage

    cache.set(key, {

      value: data,

      lastModified: Date.now(),

      tags: ctx.tags,

    })

  }

 

  async revalidateTag(tags) {

    // tags is either a string or an array of strings

    tags = [tags].flat()

    // Iterate over all entries in the cache

    for (let [key, value] of cache) {

      // If the value's tags include the specified tag, delete this entry

      if (value.tags.some((tag) => tags.includes(tag))) {

        cache.delete(key)

      }

    }

  }

 

  // If you want to have temporary in memory cache for a single request that is reset

  // before the next request you can leverage this method

  resetRequestCache() {}

}
```

Using a custom cache handler will allow you to ensure consistency across all pods hosting your Next.js application. For instance, you can save the cached values anywhere, like [Redis](https://github.com/vercel/next.js/tree/canary/examples/cache-handler-redis) or AWS S3.

> **Good to know:**
> 
> - `revalidatePath` is a convenience layer on top of cache tags. Calling `revalidatePath` will call the `revalidateTag` function with a special default tag for the provided page.

## Build Cache

Next.js generates an ID during `next build` to identify which version of your application is being served. The same build should be used and boot up multiple containers.

If you are rebuilding for each stage of your environment, you will need to generate a consistent build ID to use between containers. Use the `generateBuildId` command in `next.config.js`:

next.config.js

```
module.exports = {

  generateBuildId: async () => {

    // This could be anything, using the latest git hash

    return process.env.GIT_HASH

  },

}
```

## Version Skew

Next.js will automatically mitigate most instances of [version skew](https://www.industrialempathy.com/posts/version-skew/) and automatically reload the application to retrieve new assets when detected. For example, if there is a mismatch in the `deploymentId`, transitions between pages will perform a hard navigation versus using a prefetched value.

When the application is reloaded, there may be a loss of application state if it's not designed to persist between page navigations. For example, using URL state or local storage would persist state after a page refresh. However, component state like `useState` would be lost in such navigations.

## Streaming and Suspense

The Next.js App Router supports [streaming responses](https://nextjs.org/docs/app/api-reference/file-conventions/loading) when self-hosting. If you are using Nginx or a similar proxy, you will need to configure it to disable buffering to enable streaming.

For example, you can disable buffering in Nginx by setting `X-Accel-Buffering` to `no`:

## Partial Prerendering

[Partial Prerendering (experimental)](https://nextjs.org/docs/app/getting-started/partial-prerendering) works by default with Next.js and is not a CDN-only feature. This includes deployment as a Node.js server (through `next start`) and when used with a Docker container.

## Usage with CDNs

When using a CDN in front on your Next.js application, the page will include `Cache-Control: private` response header when dynamic APIs are accessed. This ensures that the resulting HTML page is marked as non-cacheable. If the page is fully prerendered to static, it will include `Cache-Control: public` to allow the page to be cached on the CDN.

If you don't need a mix of both static and dynamic components, you can make your entire route static and cache the output HTML on a CDN. This Automatic Static Optimization is the default behavior when running `next build` if dynamic APIs are not used.

As Partial Prerendering moves to stable, we will provide support through the Deployment Adapters API.

## after

[`after`](https://nextjs.org/docs/app/api-reference/functions/after) is fully supported when self-hosting with `next start`.

When stopping the server, ensure a graceful shutdown by sending `SIGINT` or `SIGTERM` signals and waiting. This allows the Next.js server to wait until after pending callback functions or promises used inside `after` have finished.