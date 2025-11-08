---
title: "Getting Started: Project Structure | Next.js"
source: "https://nextjs.org/docs/app/getting-started/project-structure"
author:
  - "[[Vercel]]"
published:
created: 2025-09-25
description: "Learn the folder and file conventions in Next.js, and how to organize your project."
tags:
  - "clippings"
---
[App Router](https://nextjs.org/docs/app) [Getting Started](https://nextjs.org/docs/app/getting-started) Project Structure

## Project structure and organization

This page provides an overview of **all** the folder and file conventions in Next.js, and recommendations for organizing your project.

## Folder and file conventions

### Top-level folders

Top-level folders are used to organize your application's code and static assets.

![Route segments to path segments](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ftop-level-folders.png&w=1920&q=75)

Route segments to path segments

|  |  |
| --- | --- |
| [`app`](https://nextjs.org/docs/app) | App Router |
| [`pages`](https://nextjs.org/docs/pages/building-your-application/routing) | Pages Router |
| [`public`](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) | Static assets to be served |
| [`src`](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) | Optional application source folder |

### Top-level files

Top-level files are used to configure your application, manage dependencies, run middleware, integrate monitoring tools, and define environment variables.

|  |  |
| --- | --- |
| **Next.js** |  |
| [`next.config.js`](https://nextjs.org/docs/app/api-reference/config/next-config-js) | Configuration file for Next.js |
| [`package.json`](https://nextjs.org/docs/app/getting-started/installation#manual-installation) | Project dependencies and scripts |
| [`instrumentation.ts`](https://nextjs.org/docs/app/guides/instrumentation) | OpenTelemetry and Instrumentation file |
| [`middleware.ts`](https://nextjs.org/docs/app/api-reference/file-conventions/middleware) | Next.js request middleware |
| [`.env`](https://nextjs.org/docs/app/guides/environment-variables) | Environment variables |
| [`.env.local`](https://nextjs.org/docs/app/guides/environment-variables) | Local environment variables |
| [`.env.production`](https://nextjs.org/docs/app/guides/environment-variables) | Production environment variables |
| [`.env.development`](https://nextjs.org/docs/app/guides/environment-variables) | Development environment variables |
| [`.eslintrc.json`](https://nextjs.org/docs/app/api-reference/config/eslint) | Configuration file for ESLint |
| `.gitignore` | Git files and folders to ignore |
| `next-env.d.ts` | TypeScript declaration file for Next.js |
| `tsconfig.json` | Configuration file for TypeScript |
| `jsconfig.json` | Configuration file for JavaScript |

### Routing Files

|  |  |  |
| --- | --- | --- |
| [`layout`](https://nextjs.org/docs/app/api-reference/file-conventions/layout) | `.js``.jsx``.tsx` | Layout |
| [`page`](https://nextjs.org/docs/app/api-reference/file-conventions/page) | `.js``.jsx``.tsx` | Page |
| [`loading`](https://nextjs.org/docs/app/api-reference/file-conventions/loading) | `.js``.jsx``.tsx` | Loading UI |
| [`not-found`](https://nextjs.org/docs/app/api-reference/file-conventions/not-found) | `.js``.jsx``.tsx` | Not found UI |
| [`error`](https://nextjs.org/docs/app/api-reference/file-conventions/error) | `.js``.jsx``.tsx` | Error UI |
| [`global-error`](https://nextjs.org/docs/app/api-reference/file-conventions/error#global-error) | `.js``.jsx``.tsx` | Global error UI |
| [`route`](https://nextjs.org/docs/app/api-reference/file-conventions/route) | `.js``.ts` | API endpoint |
| [`template`](https://nextjs.org/docs/app/api-reference/file-conventions/template) | `.js``.jsx``.tsx` | Re-rendered layout |
| [`default`](https://nextjs.org/docs/app/api-reference/file-conventions/default) | `.js``.jsx``.tsx` | Parallel route fallback page |

### Nested routes

|  |  |
| --- | --- |
| `folder` | Route segment |
| `folder/folder` | Nested route segment |

### Dynamic routes

|  |  |
| --- | --- |
| [`[folder]`](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#convention) | Dynamic route segment |
| [`[...folder]`](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#catch-all-segments) | Catch-all route segment |
| [`[[...folder]]`](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#optional-catch-all-segments) | Optional catch-all route segment |

### Route Groups and private folders

|  |  |
| --- | --- |
| [`(folder)`](https://nextjs.org/docs/app/api-reference/file-conventions/route-groups#convention) | Group routes without affecting routing |
| [`_folder`](https://nextjs.org/docs/app/getting-started/#private-folders) | Opt folder and all child segments out of routing |

### Parallel and Intercepted Routes

|  |  |
| --- | --- |
| [`@folder`](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes#slots) | Named slot |
| [`(.)folder`](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes#convention) | Intercept same level |
| [`(..)folder`](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes#convention) | Intercept one level above |
| [`(..)(..)folder`](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes#convention) | Intercept two levels above |
| [`(...)folder`](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes#convention) | Intercept from root |

#### App icons

|  |  |  |
| --- | --- | --- |
| [`favicon`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#favicon) | `.ico` | Favicon file |
| [`icon`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#icon) | `.ico``.jpg``.jpeg``.png``.svg` | App Icon file |
| [`icon`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#generate-icons-using-code-js-ts-tsx) | `.js``.ts``.tsx` | Generated App Icon |
| [`apple-icon`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#apple-icon) | `.jpg``.jpeg`, `.png` | Apple App Icon file |
| [`apple-icon`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#generate-icons-using-code-js-ts-tsx) | `.js``.ts``.tsx` | Generated Apple App Icon |

|  |  |  |
| --- | --- | --- |
| [`opengraph-image`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image#opengraph-image) | `.jpg``.jpeg``.png``.gif` | Open Graph image file |
| [`opengraph-image`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image#generate-images-using-code-js-ts-tsx) | `.js``.ts``.tsx` | Generated Open Graph image |
| [`twitter-image`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image#twitter-image) | `.jpg``.jpeg``.png``.gif` | Twitter image file |
| [`twitter-image`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image#generate-images-using-code-js-ts-tsx) | `.js``.ts``.tsx` | Generated Twitter image |

#### SEO

|  |  |  |
| --- | --- | --- |
| [`sitemap`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap#sitemap-files-xml) | `.xml` | Sitemap file |
| [`sitemap`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap#generating-a-sitemap-using-code-js-ts) | `.js``.ts` | Generated Sitemap |
| [`robots`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots#static-robotstxt) | `.txt` | Robots file |
| [`robots`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots#generate-a-robots-file) | `.js``.ts` | Generated Robots file |

## Organizing your project

Next.js is **unopinionated** about how you organize and colocate your project files. But it does provide several features to help you organize your project.

### Component hierarchy

The components defined in special files are rendered in a specific hierarchy:

- `layout.js`
- `template.js`
- `error.js` (React error boundary)
- `loading.js` (React suspense boundary)
- `not-found.js` (React error boundary)
- `page.js` or nested `layout.js`
![Component Hierarchy for File Conventions](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ffile-conventions-component-hierarchy.png&w=1920&q=75)

Component Hierarchy for File Conventions

The components are rendered recursively in nested routes, meaning the components of a route segment will be nested **inside** the components of its parent segment.

![Nested File Conventions Component Hierarchy](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fnested-file-conventions-component-hierarchy.png&w=1920&q=75)

Nested File Conventions Component Hierarchy

### Colocation

In the `app` directory, nested folders define route structure. Each folder represents a route segment that is mapped to a corresponding segment in a URL path.

However, even though route structure is defined through folders, a route is **not publicly accessible** until a `page.js` or `route.js` file is added to a route segment.

![A diagram showing how a route is not publicly accessible until a page.js or route.js file is added to a route segment.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-not-routable.png&w=1920&q=75)

A diagram showing how a route is not publicly accessible until a page.js or route.js file is added to a route segment.

And, even when a route is made publicly accessible, only the **content returned** by `page.js` or `route.js` is sent to the client.

![A diagram showing how page.js and route.js files make routes publicly accessible.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-routable.png&w=1920&q=75)

A diagram showing how page.js and route.js files make routes publicly accessible.

This means that **project files** can be **safely colocated** inside route segments in the `app` directory without accidentally being routable.

![A diagram showing colocated project files are not routable even when a segment contains a page.js or route.js file.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-colocation.png&w=1920&q=75)

A diagram showing colocated project files are not routable even when a segment contains a page.js or route.js file.

> **Good to know**: While you **can** colocate your project files in `app` you don't **have** to. If you prefer, you can [keep them outside the `app` directory](https://nextjs.org/docs/app/getting-started/#store-project-files-outside-of-app).

### Private folders

Private folders can be created by prefixing a folder with an underscore: `_folderName`

This indicates the folder is a private implementation detail and should not be considered by the routing system, thereby **opting the folder and all its subfolders** out of routing.

![An example folder structure using private folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-private-folders.png&w=1920&q=75)

An example folder structure using private folders

Since files in the `app` directory can be [safely colocated by default](https://nextjs.org/docs/app/getting-started/#colocation), private folders are not required for colocation. However, they can be useful for:

- Separating UI logic from routing logic.
- Consistently organizing internal files across a project and the Next.js ecosystem.
- Sorting and grouping files in code editors.
- Avoiding potential naming conflicts with future Next.js file conventions.

> **Good to know**:
> 
> - While not a framework convention, you might also consider marking files outside private folders as "private" using the same underscore pattern.
> - You can create URL segments that start with an underscore by prefixing the folder name with `%5F` (the URL-encoded form of an underscore): `%5FfolderName`.
> - If you don't use private folders, it would be helpful to know Next.js [special file conventions](https://nextjs.org/docs/app/getting-started/project-structure#routing-files) to prevent unexpected naming conflicts.

### Route groups

Route groups can be created by wrapping a folder in parenthesis: `(folderName)`

This indicates the folder is for organizational purposes and should **not be included** in the route's URL path.

![An example folder structure using route groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-route-groups.png&w=1920&q=75)

An example folder structure using route groups

Route groups are useful for:

- Organizing routes by site section, intent, or team. e.g. marketing pages, admin pages, etc.
- Enabling nested layouts in the same route segment level:
	- [Creating multiple nested layouts in the same segment, including multiple root layouts](https://nextjs.org/docs/app/getting-started/#creating-multiple-root-layouts)
	- [Adding a layout to a subset of routes in a common segment](https://nextjs.org/docs/app/getting-started/#opting-specific-segments-into-a-layout)

### src folder

Next.js supports storing application code (including `app`) inside an optional [`src` folder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder). This separates application code from project configuration files which mostly live in the root of a project.

![An example folder structure with the `src` folder](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-src-directory.png&w=1920&q=75)

An example folder structure with the \`src\` folder

## Examples

The following section lists a very high-level overview of common strategies. The simplest takeaway is to choose a strategy that works for you and your team and be consistent across the project.

> **Good to know**: In our examples below, we're using `components` and `lib` folders as generalized placeholders, their naming has no special framework significance and your projects might use other folders like `ui`, `utils`, `hooks`, `styles`, etc.

### Store project files outside of app

This strategy stores all application code in shared folders in the **root of your project** and keeps the `app` directory purely for routing purposes.

![An example folder structure with project files outside of app](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-project-root.png&w=1920&q=75)

An example folder structure with project files outside of app

### Store project files in top-level folders inside of app

This strategy stores all application code in shared folders in the **root of the `app` directory**.

![An example folder structure with project files inside app](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-app-root.png&w=1920&q=75)

An example folder structure with project files inside app

### Split project files by feature or route

This strategy stores globally shared application code in the root `app` directory and **splits** more specific application code into the route segments that use them.

![An example folder structure with project files split by feature or route](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-app-root-split.png&w=1920&q=75)

An example folder structure with project files split by feature or route

### Organize routes without affecting the URL path

To organize routes without affecting the URL, create a group to keep related routes together. The folders in parenthesis will be omitted from the URL (e.g. `(marketing)` or `(shop)`).

![Organizing Routes with Route Groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-organisation.png&w=1920&q=75)

Organizing Routes with Route Groups

Even though routes inside `(marketing)` and `(shop)` share the same URL hierarchy, you can create a different layout for each group by adding a `layout.js` file inside their folders.

![Route Groups with Multiple Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-multiple-layouts.png&w=1920&q=75)

Route Groups with Multiple Layouts

### Opting specific segments into a layout

To opt specific routes into a layout, create a new route group (e.g. `(shop)`) and move the routes that share the same layout into the group (e.g. `account` and `cart`). The routes outside of the group will not share the layout (e.g. `checkout`).

![Route Groups with Opt-in Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-opt-in-layouts.png&w=1920&q=75)

Route Groups with Opt-in Layouts

To apply a [loading skeleton](https://nextjs.org/docs/app/api-reference/file-conventions/loading) via a `loading.js` file to a specific route, create a new route group (e.g., `/(overview)`) and then move your `loading.tsx` inside that route group.

![Folder structure showing a loading.tsx and a page.tsx inside the route group](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-loading.png&w=1920&q=75)

Folder structure showing a loading.tsx and a page.tsx inside the route group

Now, the `loading.tsx` file will only apply to your dashboard → overview page instead of all your dashboard pages without affecting the URL path structure.

### Creating multiple root layouts

To create multiple [root layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout), remove the top-level `layout.js` file, and add a `layout.js` file inside each route group. This is useful for partitioning an application into sections that have a completely different UI or experience. The `<html>` and `<body>` tags need to be added to each root layout.

![Route Groups with Multiple Root Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-multiple-root-layouts.png&w=1920&q=75)

Route Groups with Multiple Root Layouts

In the example above, both `(marketing)` and `(shop)` have their own root layout.