---
title: Zustand Notes
date: 2025-09-09
lastMod: 2026-09-28
tags:
  - javascript
  - React
categories:
summary: Zustand is a state management tool for React. This article records some very elementary usages of Zustand for understanding and future reference.
slug: zustand
ai: translated
---

Zustand is a state management tool for [[React]].[~~Its official website is really nice~~](https://zustand-demo.pmnd.rs/)

Zustand automatically merges state. However, nested objects require you to specify the merge behavior manually.[^1]

```javascript
// These two statements are equivalent for simplicity's sake

set((state) => ({ count: state.count + 1 }))
set((state) => ({ ...state, count: state.count + 1 }))

// But for nested object, you have to merge them explicitly
const useCountStore = create((set) => ({
  nested: { count: 0 },
  inc: () =>
    set((state) => ({
      nested: { ...state.nested, count: state.nested.count + 1 },
    })),
}))
```

Zustand's store is a hook. Its standard pattern is as follows.[^2]

```javascript
import create from 'zustand'

// First create a store
const useBearStore = create((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}))

// Then bind your components, and that's it!
function BearCounter() {
  const bears = useBearStore((state) => state.bears)
  return <h1>{bears} around here ...</h1>
}

function Controls() {
  const increasePopulation = useBearStore((state) => state.increasePopulation)
  return <button onClick={increasePopulation}>one up</button>
}
```

Try to use atomic selectors, because whatever a selector returns triggers a component re-render, and `Array` and `Object` are always treated as new results.[^3]

```javascript
// Selector returns a new Object in every invocation
const { bears, fish } = useBearStore((state) => ({
  bears: state.bears,
  fish: state.fish,
}))

// So these two are equivalent..
const { bears, fish } = useBearStore()

// Prefer this!
export const useBears = () => useBearStore((state) => state.bears)
export const useFish = () => useBearStore((state) => state.fish)
```

[^1]: https://github.com/pmndrs/zustand/blob/2b29d736841dc7b3fd7dec8cbfea50fee7295974/docs/guides/immutable-state-and-merging.md

[^2]: https://github.com/pmndrs/zustand/tree/2b29d736841dc7b3fd7dec8cbfea50fee7295974?tab=readme-ov-file#first-create-a-store

[^3]: https://tkdodo.eu/blog/working-with-zustand#prefer-atomic-selectors
