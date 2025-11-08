---
title: "Guides: Package Bundling | Next.js"
source: "https://nextjs.org/docs/app/guides/package-bundling"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn how to optimize your application's server and client bundles."
tags:
  - "clippings"
---
## How to optimize package bundling

Bundling external packages can significantly improve the performance of your application. By default, packages imported inside Server Components and Route Handlers are automatically bundled by Next.js. This page will guide you through how to analyze and further optimize package bundling.

## Analyzing JavaScript bundles

[`@next/bundle-analyzer`](https://www.npmjs.com/package/@next/bundle-analyzer) is a plugin for Next.js that helps you manage the size of your application bundles. It generates a visual report of the size of each package and their dependencies. You can use the information to remove large dependencies, split, or [lazy-load](https://nextjs.org/docs/app/guides/lazy-loading) your code.

### Installation

Install the plugin by running the following command:

```
npm i @next/bundle-analyzer

# or

yarn add @next/bundle-analyzer

# or

pnpm add @next/bundle-analyzer
```

Then, add the bundle analyzer's settings to your `next.config.js`.

next.config.js

```
/** @type {import('next').NextConfig} */

const nextConfig = {}

 

const withBundleAnalyzer = require('@next/bundle-analyzer')({

  enabled: process.env.ANALYZE === 'true',

})

 

module.exports = withBundleAnalyzer(nextConfig)
```

### Generating a report

Run the following command to analyze your bundles:

```
ANALYZE=true npm run build

# or

ANALYZE=true yarn build

# or

ANALYZE=true pnpm build
```

The report will open three new tabs in your browser, which you can inspect. Periodically evaluating your application's bundles can help you maintain application performance over time.

## Optimizing package imports

Some packages, such as icon libraries, can export hundreds of modules, which can cause performance issues in development and production.

You can optimize how these packages are imported by adding the [`optimizePackageImports`](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports) option to your `next.config.js`. This option will only load the modules you *actually* use, while still giving you the convenience of writing import statements with many named exports.

next.config.js

```
/** @type {import('next').NextConfig} */

const nextConfig = {

  experimental: {

    optimizePackageImports: ['icon-library'],

  },

}

 

module.exports = nextConfig
```

Next.js also optimizes some libraries automatically, thus they do not need to be included in the optimizePackageImports list. See the [full list](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports).

## Opting specific packages out of bundling

Since packages imported inside Server Components and Route Handlers are automatically bundled by Next.js, you can opt specific packages out of bundling using the [`serverExternalPackages`](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverExternalPackages) option in your `next.config.js`.

next.config.js

```
/** @type {import('next').NextConfig} */

const nextConfig = {

  serverExternalPackages: ['package-name'],

}

 

module.exports = nextConfig
```

Next.js includes a list of popular packages that currently are working on compatibility and automatically opt-ed out. See the [full list](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverExternalPackages).

Learn more about optimizing your application for production.### [Production](https://nextjs.org/docs/app/guides/production-checklist)

[

Recommendations to ensure the best performance and user experience before taking your Next.js application to production.

](https://nextjs.org/docs/app/guides/production-checklist)