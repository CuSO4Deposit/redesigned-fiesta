---
title: "Next build stuck on \"Creating an optimized production build\" forever"
ai: translated
date: 2025-06-20
lastMod: 2026-09-28
tags:
- nodejs
- nextjs
categories:
slug: next-build-stuck
---

## Problem


  + `next build` stuck on "Creating an optimized production build" forever, with no useful logs.


```
$ npm run build --verbose
npm verbose cli /nix/store/c8jxsih8yy2rnncdmx2hyraizf689nvp-nodejs-22.14.0/bin/node /nix/store/c8jxsih8yy2rnncdmx2hyraizf689nvp-nodejs-22.14.0/bin/npm
npm info using npm@10.9.2
npm info using node@v22.14.0
npm verbose title npm run build
npm verbose argv "run" "build" "--loglevel" "verbose"
npm verbose logfile logs-max:10 dir:/home/cuso4d/.npm/_logs/2025-06-20T11_37_08_833Z-
npm verbose logfile /home/cuso4d/.npm/_logs/2025-06-20T11_37_08_833Z-debug-0.log

> assistant-ui-starter@0.1.0 build
> next build

   ▲ Next.js 15.3.1
   - Environments: .env

   Creating an optimized production build ...
```


  + The log file produced:

```
0 verbose cli /nix/store/c8jxsih8yy2rnncdmx2hyraizf689nvp-nodejs-22.14.0/bin/node /nix/store/c8jxsih8yy2rnncdmx2hyraizf689nvp-nodejs-22.14.0/bin/npm
1 info using npm@10.9.2
2 info using node@v22.14.0
3 silly config load:file:/nix/store/c8jxsih8yy2rnncdmx2hyraizf689nvp-nodejs-22.14.0/lib/node_modules/npm/npmrc
4 silly config load:file:/home/cuso4d/source/sci-assistant-frontend/.npmrc
5 silly config load:file:/home/cuso4d/.npmrc
6 silly config load:file:/nix/store/c8jxsih8yy2rnncdmx2hyraizf689nvp-nodejs-22.14.0/etc/npmrc
7 verbose title npm
8 verbose argv
9 verbose logfile logs-max:10 dir:/home/cuso4d/.npm/_logs/2025-06-20T11_57_26_719Z-
10 verbose logfile /home/cuso4d/.npm/_logs/2025-06-20T11_57_26_719Z-debug-0.log
11 verbose cwd /home/cuso4d/source/sci-assistant-frontend
12 verbose os Linux 6.12.33
13 verbose node v22.14.0
14 verbose npm  v10.9.2
15 verbose exit 1
16 verbose code 1
```


Many mentioned "**You can't have both dev and build at the same time.**" [source](https://github.com/vercel/next.js/discussions/60147#discussioncomment-7998137), though it is not my case.

Actually, the default page created by `create-next-app` used the Google fonts, and the related `@next/font` package was the case.

  + *After trying all recommendation here and all are not working, I just found out the reason after 2 weeks of debugging is `@next/font` package, removing it completely fixes my issue. The main reason is that most of the time it fail to download fonts without showing any signs of error.* by [jpmadrigal07](https://github.com/jpmadrigal07) at [github discussion](https://github.com/vercel/next.js/discussions/60147#discussioncomment-9476406).


The solution is to comment out the fonts usage in `layout.tsx` in the project.

## Related issues

  + https://github.com/vercel/next.js/discussions/60147
