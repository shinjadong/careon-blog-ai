---
title: "Getting Started: Image Optimization | Next.js"
source: "https://nextjs.org/docs/app/getting-started/images"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn how to optimize images in Next.js"
tags:
  - "clippings"
---
[App Router](https://nextjs.org/docs/app) [Getting Started](https://nextjs.org/docs/app/getting-started) Image Optimization

## Image Optimization

The Next.js [`<Image>`](https://nextjs.org/docs/app/api-reference/components/image) component extends the HTML `<img>` element to provide:

- **Size optimization:** Automatically serving correctly sized images for each device, using modern image formats like WebP.
- **Visual stability:** Preventing [layout shift](https://web.dev/articles/cls) automatically when images are loading.
- **Faster page loads:** Only loading images when they enter the viewport using native browser lazy loading, with optional blur-up placeholders.
- **Asset flexibility:** Resizing images on-demand, even images stored on remote servers.

To start using `<Image>`, import it from `next/image` and render it within your component.

app/page.tsx

```
import Image from 'next/image'

 

export default function Page() {

  return <Image src="" alt="" />

}
```

The `src` property can be a [local](https://nextjs.org/docs/app/getting-started/#local-images) or [remote](https://nextjs.org/docs/app/getting-started/#remote-images) image.

> **🎥 Watch:** Learn more about how to use `next/image` → [YouTube (9 minutes)](https://youtu.be/IU_qq_c_lKA).

## Local images

You can store static files, like images and fonts, under a folder called [`public`](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) in the root directory. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

![Folder structure showing app and public folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fpublic-folder.png&w=1920&q=75)

Folder structure showing app and public folders

app/page.tsx

```
import Image from 'next/image'

 

export default function Page() {

  return (

    <Image

      src="/profile.png"

      alt="Picture of the author"

      width={500}

      height={500}

    />

  )

}
```

If the image is statically imported, Next.js will automatically determine the intrinsic [`width`](https://nextjs.org/docs/app/api-reference/components/image#width-and-height) and [`height`](https://nextjs.org/docs/app/api-reference/components/image#width-and-height). These values are used to determine the image ratio and prevent [Cumulative Layout Shift](https://web.dev/articles/cls) while your image is loading.

app/page.tsx

```
import Image from 'next/image'

import ProfileImage from './profile.png'

 

export default function Page() {

  return (

    <Image

      src={ProfileImage}

      alt="Picture of the author"

      // width={500} automatically provided

      // height={500} automatically provided

      // blurDataURL="data:..." automatically provided

      // placeholder="blur" // Optional blur-up while loading

    />

  )

}
```

## Remote images

To use a remote image, you can provide a URL string for the `src` property.

app/page.tsx

```
import Image from 'next/image'

 

export default function Page() {

  return (

    <Image

      src="https://s3.amazonaws.com/my-bucket/profile.png"

      alt="Picture of the author"

      width={500}

      height={500}

    />

  )

}
```

Since Next.js does not have access to remote files during the build process, you'll need to provide the [`width`](https://nextjs.org/docs/app/api-reference/components/image#width-and-height), [`height`](https://nextjs.org/docs/app/api-reference/components/image#width-and-height) and optional [`blurDataURL`](https://nextjs.org/docs/app/api-reference/components/image#blurdataurl) props manually. The `width` and `height` are used to infer the correct aspect ratio of image and avoid layout shift from the image loading in. Alternatively, you can use the [`fill` property](https://nextjs.org/docs/app/api-reference/components/image#fill) to make the image fill the size of the parent element.

To safely allow images from remote servers, you need to define a list of supported URL patterns in [`next.config.js`](https://nextjs.org/docs/app/api-reference/config/next-config-js). Be as specific as possible to prevent malicious usage. For example, the following configuration will only allow images from a specific AWS S3 bucket:

next.config.ts

```
import type { NextConfig } from 'next'

 

const config: NextConfig = {

  images: {

    remotePatterns: [

      {

        protocol: 'https',

        hostname: 's3.amazonaws.com',

        port: '',

        pathname: '/my-bucket/**',

        search: '',

      },

    ],

  },

}

 

export default config
```

## API Reference

See the API Reference for the full feature set of Next.js Image.### [Image Component](https://nextjs.org/docs/app/api-reference/components/image)

[

Optimize Images in your Next.js Application using the built-in \`next/image\` Component.

](https://nextjs.org/docs/app/api-reference/components/image)