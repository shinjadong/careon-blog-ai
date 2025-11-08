---
title: "Getting Started: Upgrading | Next.js"
source: "https://nextjs.org/docs/app/getting-started/upgrading"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn how to upgrade your Next.js application to the latest version or canary."
tags:
  - "clippings"
---
## Upgrading

## Latest version

To update to the latest version of Next.js, you can use the `upgrade` codemod:

Terminal

```
npx @next/codemod@latest upgrade latest
```

If you prefer to upgrade manually, install the latest Next.js and React versions:

Terminal

```
pnpm i next@latest react@latest react-dom@latest eslint-config-next@latest
```

## Canary version

To update to the latest canary, make sure you're on the latest version of Next.js and everything is working as expected. Then, run the following command:

Terminal

```
npm i next@canary
```

### Features available in canary

The following features are currently available in canary:

**Caching**:

- [`"use cache"`](https://nextjs.org/docs/app/api-reference/directives/use-cache)
- [`cacheLife`](https://nextjs.org/docs/app/api-reference/functions/cacheLife)
- [`cacheTag`](https://nextjs.org/docs/app/api-reference/functions/cacheTag)
- [`cacheComponents`](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)

**Authentication**:

- [`forbidden`](https://nextjs.org/docs/app/api-reference/functions/forbidden)
- [`forbidden.js`](https://nextjs.org/docs/app/api-reference/file-conventions/forbidden)
- [`authInterrupts`](https://nextjs.org/docs/app/api-reference/config/next-config-js/authInterrupts)

## Version guides

See the version guides for in-depth upgrade instructions.### [Version 15](https://nextjs.org/docs/app/guides/upgrading/version-15)

[

Upgrade your Next.js Application from Version 14 to 15.

](https://nextjs.org/docs/app/guides/upgrading/version-15)Version 14

Upgrade your Next.js Application from Version 13 to 14.

[View original](https://nextjs.org/docs/app/guides/upgrading/version-14)

Was this helpful?