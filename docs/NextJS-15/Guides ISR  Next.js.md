---
title: "Guides: ISR | Next.js"
source: "https://nextjs.org/docs/app/guides/incremental-static-regeneration"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn how to create or update static pages at runtime with Incremental Static Regeneration."
tags:
  - "clippings"
---
## How to implement Incremental Static Regeneration (ISR)

Examples
- [Next.js Commerce](https://vercel.com/templates/next.js/nextjs-commerce)
- [On-Demand ISR](https://on-demand-isr.vercel.app/)
- [Next.js Forms](https://github.com/vercel/next.js/tree/canary/examples/next-forms)

Incremental Static Regeneration (ISR) enables you to:

- Update static content without rebuilding the entire site
- Reduce server load by serving prerendered, static pages for most requests
- Ensure proper `cache-control` headers are automatically added to pages
- Handle large amounts of content pages without long `next build` times

Here's a minimal example:

app/blog/\[id\]/page.tsx

```
interface Post {

  id: string

  title: string

  content: string

}

 

// Next.js will invalidate the cache when a

// request comes in, at most once every 60 seconds.

export const revalidate = 60

 

export async function generateStaticParams() {

  const posts: Post[] = await fetch('https://api.vercel.app/blog').then((res) =>

    res.json()

  )

  return posts.map((post) => ({

    id: String(post.id),

  }))

}

 

export default async function Page({

  params,

}: {

  params: Promise<{ id: string }>

}) {

  const { id } = await params

  const post: Post = await fetch(\`https://api.vercel.app/blog/${id}\`).then(

    (res) => res.json()

  )

  return (

    <main>

      <h1>{post.title}</h1>

      <p>{post.content}</p>

    </main>

  )

}
```

Here's how this example works:

1. During `next build`, all known blog posts are generated
2. All requests made to these pages (e.g. `/blog/1`) are cached and instantaneous
3. After 60 seconds has passed, the next request will still return the cached (now stale) page
4. The cache is invalidated and a new version of the page begins generating in the background
5. Once generated successfully, the next request will return the updated page and cache it for subsequent requests
6. If `/blog/26` is requested, and it exists, the page will be generated on-demand. This behavior can be changed by using a different [dynamicParams](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamicparams) value. However, if the post does not exist, then 404 is returned.

## Reference

### Route segment config

- [`revalidate`](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#revalidate)
- [`dynamicParams`](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamicparams)

### Functions

- [`revalidatePath`](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)
- [`revalidateTag`](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)

## Examples

### Time-based revalidation

This fetches and displays a list of blog posts on /blog. After an hour has passed, the next visitor will still receive the cached (stale) version of the page immediately for a fast response. Simultaneously, Next.js triggers regeneration of a fresh version in the background. Once the new version is successfully generated, it replaces the cached version, and subsequent visitors will receive the updated content.

app/blog/page.tsx

```
interface Post {

  id: string

  title: string

  content: string

}

 

export const revalidate = 3600 // invalidate every hour

 

export default async function Page() {

  const data = await fetch('https://api.vercel.app/blog')

  const posts: Post[] = await data.json()

  return (

    <main>

      <h1>Blog Posts</h1>

      <ul>

        {posts.map((post) => (

          <li key={post.id}>{post.title}</li>

        ))}

      </ul>

    </main>

  )

}
```

We recommend setting a high revalidation time. For instance, 1 hour instead of 1 second. If you need more precision, consider using on-demand revalidation. If you need real-time data, consider switching to [dynamic rendering](https://nextjs.org/docs/app/getting-started/partial-prerendering#dynamic-rendering).

### On-demand revalidation with revalidatePath

For a more precise method of revalidation, invalidate cached pages on-demand with the `revalidatePath` function.

For example, this Server Action would get called after adding a new post. Regardless of how you retrieve your data in your Server Component, either using `fetch` or connecting to a database, this will invalidate the cache for the entire route. The next request to that route will trigger regeneration and serve fresh data, which will then be cached for subsequent requests.

> **Note:**`revalidatePath` invalidates the cache entries but regeneration happens on the next request. If you want to eagerly regenerate the cache entry immediately instead of waiting for the next request, you can use the Pages router [`res.revalidate`](https://nextjs.org/docs/app/guides/docs/pages/guides/incremental-static-regeneration#on-demand-validation-with-resrevalidate) method. We're working on adding new methods to provide eager regeneration capabilities for the App Router.

app/actions.ts

```
'use server'

 

import { revalidatePath } from 'next/cache'

 

export async function createPost() {

  // Invalidate the cache for the /posts route

  revalidatePath('/posts')

}
```

[View a demo](https://on-demand-isr.vercel.app/) and [explore the source code](https://github.com/vercel/on-demand-isr).

### On-demand revalidation with revalidateTag

For most use cases, prefer revalidating entire paths. If you need more granular control, you can use the `revalidateTag` function. For example, you can tag individual `fetch` calls:

app/blog/page.tsx

```
export default async function Page() {

  const data = await fetch('https://api.vercel.app/blog', {

    next: { tags: ['posts'] },

  })

  const posts = await data.json()

  // ...

}
```

If you are using an ORM or connecting to a database, you can use `unstable_cache`:

app/blog/page.tsx

```
import { unstable_cache } from 'next/cache'

import { db, posts } from '@/lib/db'

 

const getCachedPosts = unstable_cache(

  async () => {

    return await db.select().from(posts)

  },

  ['posts'],

  { revalidate: 3600, tags: ['posts'] }

)

 

export default async function Page() {

  const posts = getCachedPosts()

  // ...

}
```

You can then use `revalidateTag` in a [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data) or [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route):

app/actions.ts

```
'use server'

 

import { revalidateTag } from 'next/cache'

 

export async function createPost() {

  // Invalidate all data tagged with 'posts'

  revalidateTag('posts')

}
```

### Handling uncaught exceptions

If an error is thrown while attempting to revalidate data, the last successfully generated data will continue to be served from the cache. On the next subsequent request, Next.js will retry revalidating the data. [Learn more about error handling](https://nextjs.org/docs/app/getting-started/error-handling).

### Customizing the cache location

You can configure the Next.js cache location if you want to persist cached pages and data to durable storage, or share the cache across multiple containers or instances of your Next.js application. [Learn more](https://nextjs.org/docs/app/guides/self-hosting#caching-and-isr).

## Troubleshooting

### Debugging cached data in local development

If you are using the `fetch` API, you can add additional logging to understand which requests are cached or uncached. [Learn more about the `logging` option](https://nextjs.org/docs/app/api-reference/config/next-config-js/logging).

next.config.js

```
module.exports = {

  logging: {

    fetches: {

      fullUrl: true,

    },

  },

}
```

### Verifying correct production behavior

To verify your pages are cached and revalidated correctly in production, you can test locally by running `next build` and then `next start` to run the production Next.js server.

This will allow you to test ISR behavior as it would work in a production environment. For further debugging, add the following environment variable to your `.env` file:

.env

```
NEXT_PRIVATE_DEBUG_CACHE=1
```

This will make the Next.js server console log ISR cache hits and misses. You can inspect the output to see which pages are generated during `next build`, as well as how pages are updated as paths are accessed on-demand.

## Caveats

- ISR is only supported when using the Node.js runtime (default).
- ISR is not supported when creating a [Static Export](https://nextjs.org/docs/app/guides/static-exports).
- If you have multiple `fetch` requests in a statically rendered route, and each has a different `revalidate` frequency, the lowest time will be used for ISR. However, those revalidate frequencies will still be respected by the [Data Cache](https://nextjs.org/docs/app/guides/caching#data-cache).
- If any of the `fetch` requests used on a route have a `revalidate` time of `0`, or an explicit `no-store`, the route will be [dynamically rendered](https://nextjs.org/docs/app/getting-started/partial-prerendering#dynamic-rendering).
- Middleware won't be executed for on-demand ISR requests, meaning any path rewrites or logic in Middleware will not be applied. Ensure you are revalidating the exact path. For example, `/post/1` instead of a rewritten `/post-1`.

## Platform Support

Learn how to [configure ISR](https://nextjs.org/docs/app/guides/self-hosting#caching-and-isr) when self-hosting Next.js.

## Version history

| Version | Changes |
| --- | --- |
| `v14.1.0` | Custom `cacheHandler` is stable. |
| `v13.0.0` | App Router is introduced. |
| `v12.2.0` | Pages Router: On-Demand ISR is stable |
| `v12.0.0` | Pages Router: [Bot-aware ISR fallback](https://nextjs.org/blog/next-12#bot-aware-isr-fallback) added. |
| `v9.5.0` | Pages Router: [Stable ISR introduced](https://nextjs.org/blog/next-9-5). |