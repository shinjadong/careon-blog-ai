---
title: "Guides: Tailwind CSS v3 | Next.js"
source: "https://nextjs.org/docs/app/guides/tailwind-v3-css"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Style your Next.js Application using Tailwind CSS v3 for broader browser support."
tags:
  - "clippings"
---
[App Router](https://nextjs.org/docs/app) [Guides](https://nextjs.org/docs/app/guides) Tailwind CSS v3

## How to install Tailwind CSS v3 in your Next.js application

This guide will walk you through how to install [Tailwind CSS v3](https://v3.tailwindcss.com/) in your Next.js application.

> **Good to know:** For the latest Tailwind 4 setup, see the [Tailwind CSS setup instructions](https://nextjs.org/docs/app/getting-started/css#tailwind-css).

## Installing Tailwind v3

Install Tailwind CSS and its peer dependencies, then run the `init` command to generate both `tailwind.config.js` and `postcss.config.js` files:

Terminal

```
pnpm add -D tailwindcss@^3 postcss autoprefixer

npx tailwindcss init -p
```

## Configuring Tailwind v3

Configure your template paths in your `tailwind.config.js` file:

tailwind.config.js

```
/** @type {import('tailwindcss').Config} */

module.exports = {

  content: [

    './app/**/*.{js,ts,jsx,tsx,mdx}',

    './pages/**/*.{js,ts,jsx,tsx,mdx}',

    './components/**/*.{js,ts,jsx,tsx,mdx}',

  ],

  theme: {

    extend: {},

  },

  plugins: [],

}
```

Add the Tailwind directives to your global CSS file:

app/globals.css

```
@tailwind base;

@tailwind components;

@tailwind utilities;
```

Import the CSS file in your root layout:

app/layout.tsx

```
import './globals.css'

 

export default function RootLayout({

  children,

}: {

  children: React.ReactNode

}) {

  return (

    <html lang="en">

      <body>{children}</body>

    </html>

  )

}
```

## Using classes

After installing Tailwind CSS and adding the global styles, you can use Tailwind's utility classes in your application.

app/page.tsx

```
export default function Page() {

  return <h1 className="text-3xl font-bold underline">Hello, Next.js!</h1>

}
```

## Usage with Turbopack

As of Next.js 13.1, Tailwind CSS and PostCSS are supported with [Turbopack](https://turbo.build/pack/docs/features/css#tailwind-css).

Was this helpful?