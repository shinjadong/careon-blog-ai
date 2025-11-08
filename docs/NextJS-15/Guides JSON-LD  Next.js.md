---
title: "Guides: JSON-LD | Next.js"
source: "https://nextjs.org/docs/app/guides/json-ld"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn how to add JSON-LD to your Next.js application to describe your content to search engines and AI."
tags:
  - "clippings"
---
## How to implement JSON-LD in your Next.js application

[JSON-LD](https://json-ld.org/) is a format for structured data that can be used by search engines and AI to to help them understand the structure of the page beyond pure content. For example, you can use it to describe a person, an event, an organization, a movie, a book, a recipe, and many other types of entities.

Our current recommendation for JSON-LD is to render structured data as a `<script>` tag in your `layout.js` or `page.js` components.

The following snippet uses `JSON.stringify`, which does not sanitize malicious strings used in XSS injection. To prevent this type of vulnerability, you can scrub `HTML` tags from the `JSON-LD` payload, for example, by replacing the character, `<`, with its unicode equivalent, `\u003c`.

Review your organization's recommended approach to sanitize potentially dangerous strings, or use community maintained alternatives for `JSON.stringify` such as, [serialize-javascript](https://www.npmjs.com/package/serialize-javascript).

app/products/\[id\]/page.tsx

```
export default async function Page({ params }) {

  const { id } = await params

  const product = await getProduct(id)

 

  const jsonLd = {

    '@context': 'https://schema.org',

    '@type': 'Product',

    name: product.name,

    image: product.image,

    description: product.description,

  }

 

  return (

    <section>

      {/* Add JSON-LD to your page */}

      <script

        type="application/ld+json"

        dangerouslySetInnerHTML={{

          __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c'),

        }}

      />

      {/* ... */}

    </section>

  )

}
```

You can validate and test your structured data with the [Rich Results Test](https://search.google.com/test/rich-results) for Google or the generic [Schema Markup Validator](https://validator.schema.org/).

You can type your JSON-LD with TypeScript using community packages like [`schema-dts`](https://www.npmjs.com/package/schema-dts):

```
import { Product, WithContext } from 'schema-dts'

 

const jsonLd: WithContext<Product> = {

  '@context': 'https://schema.org',

  '@type': 'Product',

  name: 'Next.js Sticker',

  image: 'https://nextjs.org/imgs/sticker.png',

  description: 'Dynamic at the speed of static.',

}
```