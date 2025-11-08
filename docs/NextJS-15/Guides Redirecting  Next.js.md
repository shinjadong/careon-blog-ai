---
title: "Guides: Redirecting | Next.js"
source: "https://nextjs.org/docs/app/guides/redirecting"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn the different ways to handle redirects in Next.js."
tags:
  - "clippings"
---
## How to handle redirects in Next.js

There are a few ways you can handle redirects in Next.js. This page will go through each available option, use cases, and how to manage large numbers of redirects.

## redirect function

The `redirect` function allows you to redirect the user to another URL. You can call `redirect` in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data).

`redirect` is often used after a mutation or event. For example, creating a post:

> **Good to know**:
> 
> - `redirect` returns a 307 (Temporary Redirect) status code by default. When used in a Server Action, it returns a 303 (See Other), which is commonly used for redirecting to a success page as a result of a POST request.
> - `redirect` throws an error so it should be called **outside** the `try` block when using `try/catch` statements.
> - `redirect` can be called in Client Components during the rendering process but not in event handlers. You can use the [`useRouter` hook](https://nextjs.org/docs/app/guides/#userouter-hook) instead.
> - `redirect` also accepts absolute URLs and can be used to redirect to external links.
> - If you'd like to redirect before the render process, use [`next.config.js`](https://nextjs.org/docs/app/guides/#redirects-in-nextconfigjs) or [Middleware](https://nextjs.org/docs/app/guides/#nextresponseredirect-in-middleware).

See the [`redirect` API reference](https://nextjs.org/docs/app/api-reference/functions/redirect) for more information.

## permanentRedirect function

The `permanentRedirect` function allows you to **permanently** redirect the user to another URL. You can call `permanentRedirect` in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data).

`permanentRedirect` is often used after a mutation or event that changes an entity's canonical URL, such as updating a user's profile URL after they change their username:

> **Good to know**:
> 
> - `permanentRedirect` returns a 308 (permanent redirect) status code by default.
> - `permanentRedirect` also accepts absolute URLs and can be used to redirect to external links.
> - If you'd like to redirect before the render process, use [`next.config.js`](https://nextjs.org/docs/app/guides/#redirects-in-nextconfigjs) or [Middleware](https://nextjs.org/docs/app/guides/#nextresponseredirect-in-middleware).

See the [`permanentRedirect` API reference](https://nextjs.org/docs/app/api-reference/functions/permanentRedirect) for more information.

## useRouter() hook

If you need to redirect inside an event handler in a Client Component, you can use the `push` method from the `useRouter` hook. For example:

> **Good to know**:
> 
> - If you don't need to programmatically navigate a user, you should use a [`<Link>`](https://nextjs.org/docs/app/api-reference/components/link) component.

See the [`useRouter` API reference](https://nextjs.org/docs/app/api-reference/functions/use-router) for more information.

## redirects in next.config.js

The `redirects` option in the `next.config.js` file allows you to redirect an incoming request path to a different destination path. This is useful when you change the URL structure of pages or have a list of redirects that are known ahead of time.

`redirects` supports [path](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#path-matching), [header, cookie, and query matching](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#header-cookie-and-query-matching), giving you the flexibility to redirect users based on an incoming request.

To use `redirects`, add the option to your `next.config.js` file:

next.config.ts

```
import type { NextConfig } from 'next'

 

const nextConfig: NextConfig = {

  async redirects() {

    return [

      // Basic redirect

      {

        source: '/about',

        destination: '/',

        permanent: true,

      },

      // Wildcard path matching

      {

        source: '/blog/:slug',

        destination: '/news/:slug',

        permanent: true,

      },

    ]

  },

}

 

export default nextConfig
```

See the [`redirects` API reference](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects) for more information.

> **Good to know**:
> 
> - `redirects` can return a 307 (Temporary Redirect) or 308 (Permanent Redirect) status code with the `permanent` option.
> - `redirects` may have a limit on platforms. For example, on Vercel, there's a limit of 1,024 redirects. To manage a large number of redirects (1000+), consider creating a custom solution using [Middleware](https://nextjs.org/docs/app/api-reference/file-conventions/middleware). See [managing redirects at scale](https://nextjs.org/docs/app/guides/#managing-redirects-at-scale-advanced) for more.
> - `redirects` runs **before** Middleware.

## NextResponse.redirect in Middleware

Middleware allows you to run code before a request is completed. Then, based on the incoming request, redirect to a different URL using `NextResponse.redirect`. This is useful if you want to redirect users based on a condition (e.g. authentication, session management, etc) or have [a large number of redirects](https://nextjs.org/docs/app/guides/#managing-redirects-at-scale-advanced).

For example, to redirect the user to a `/login` page if they are not authenticated:

> **Good to know**:
> 
> - Middleware runs **after** `redirects` in `next.config.js` and **before** rendering.

See the [Middleware](https://nextjs.org/docs/app/api-reference/file-conventions/middleware) documentation for more information.

## Managing redirects at scale (advanced)

To manage a large number of redirects (1000+), you may consider creating a custom solution using Middleware. This allows you to handle redirects programmatically without having to redeploy your application.

To do this, you'll need to consider:

1. Creating and storing a redirect map.
2. Optimizing data lookup performance.

> **Next.js Example**: See our [Middleware with Bloom filter](https://redirects-bloom-filter.vercel.app/) example for an implementation of the recommendations below.

### 1\. Creating and storing a redirect map

A redirect map is a list of redirects that you can store in a database (usually a key-value store) or JSON file.

Consider the following data structure:

```
{

  "/old": {

    "destination": "/new",

    "permanent": true

  },

  "/blog/post-old": {

    "destination": "/blog/post-new",

    "permanent": true

  }

}
```

In [Middleware](https://nextjs.org/docs/app/api-reference/file-conventions/middleware), you can read from a database such as Vercel's [Edge Config](https://vercel.com/docs/edge-config/get-started) or [Redis](https://vercel.com/docs/redis), and redirect the user based on the incoming request:

middleware.ts

```
import { NextResponse, NextRequest } from 'next/server'

import { get } from '@vercel/edge-config'

 

type RedirectEntry = {

  destination: string

  permanent: boolean

}

 

export async function middleware(request: NextRequest) {

  const pathname = request.nextUrl.pathname

  const redirectData = await get(pathname)

 

  if (redirectData && typeof redirectData === 'string') {

    const redirectEntry: RedirectEntry = JSON.parse(redirectData)

    const statusCode = redirectEntry.permanent ? 308 : 307

    return NextResponse.redirect(redirectEntry.destination, statusCode)

  }

 

  // No redirect found, continue without redirecting

  return NextResponse.next()

}
```

### 2\. Optimizing data lookup performance

Reading a large dataset for every incoming request can be slow and expensive. There are two ways you can optimize data lookup performance:

- Use a database that is optimized for fast reads
- Use a data lookup strategy such as a [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) to efficiently check if a redirect exists **before** reading the larger redirects file or database.

Considering the previous example, you can import a generated bloom filter file into Middleware, then, check if the incoming request pathname exists in the bloom filter.

If it does, forward the request to a [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route) which will check the actual file and redirect the user to the appropriate URL. This avoids importing a large redirects file into Middleware, which can slow down every incoming request.

middleware.ts

```
import { NextResponse, NextRequest } from 'next/server'

import { ScalableBloomFilter } from 'bloom-filters'

import GeneratedBloomFilter from './redirects/bloom-filter.json'

 

type RedirectEntry = {

  destination: string

  permanent: boolean

}

 

// Initialize bloom filter from a generated JSON file

const bloomFilter = ScalableBloomFilter.fromJSON(GeneratedBloomFilter as any)

 

export async function middleware(request: NextRequest) {

  // Get the path for the incoming request

  const pathname = request.nextUrl.pathname

 

  // Check if the path is in the bloom filter

  if (bloomFilter.has(pathname)) {

    // Forward the pathname to the Route Handler

    const api = new URL(

      \`/api/redirects?pathname=${encodeURIComponent(request.nextUrl.pathname)}\`,

      request.nextUrl.origin

    )

 

    try {

      // Fetch redirect data from the Route Handler

      const redirectData = await fetch(api)

 

      if (redirectData.ok) {

        const redirectEntry: RedirectEntry | undefined =

          await redirectData.json()

 

        if (redirectEntry) {

          // Determine the status code

          const statusCode = redirectEntry.permanent ? 308 : 307

 

          // Redirect to the destination

          return NextResponse.redirect(redirectEntry.destination, statusCode)

        }

      }

    } catch (error) {

      console.error(error)

    }

  }

 

  // No redirect found, continue the request without redirecting

  return NextResponse.next()

}
```

Then, in the Route Handler:

app/api/redirects/route.ts

```
import { NextRequest, NextResponse } from 'next/server'

import redirects from '@/app/redirects/redirects.json'

 

type RedirectEntry = {

  destination: string

  permanent: boolean

}

 

export function GET(request: NextRequest) {

  const pathname = request.nextUrl.searchParams.get('pathname')

  if (!pathname) {

    return new Response('Bad Request', { status: 400 })

  }

 

  // Get the redirect entry from the redirects.json file

  const redirect = (redirects as Record<string, RedirectEntry>)[pathname]

 

  // Account for bloom filter false positives

  if (!redirect) {

    return new Response('No redirect', { status: 400 })

  }

 

  // Return the redirect entry

  return NextResponse.json(redirect)

}
```

> **Good to know:**
> 
> - To generate a bloom filter, you can use a library like [`bloom-filters`](https://www.npmjs.com/package/bloom-filters).
> - You should validate requests made to your Route Handler to prevent malicious requests.### [redirect](https://nextjs.org/docs/app/api-reference/functions/redirect)

[

API Reference for the redirect function.

](https://nextjs.org/docs/app/api-reference/functions/redirect)permanentRedirect

API Reference for the permanentRedirect function.

[View original](https://nextjs.org/docs/app/api-reference/functions/permanentRedirect)middleware.js

API reference for the middleware.js file.

[View original](https://nextjs.org/docs/app/api-reference/file-conventions/middleware)redirects

Add redirects to your Next.js app.

[View original](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects)