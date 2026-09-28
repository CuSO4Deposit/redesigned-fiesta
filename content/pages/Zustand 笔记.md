---
title: Zustand 笔记
date: 2025-09-09
lastMod: 2026-09-28
tags:
- javascript
- React
categories:
summary: Zustand 是一个 React 中的 state 管理工具，本文记录了 Zustand 的一些非常初等的用法以供理解和备忘。
slug: zustand
---

Zustand 是一个 [[React]] 中的 state 管理工具。[~~它的官网真好看~~](https://zustand-demo.pmnd.rs/)


Zustand 会自动 merge state。但是嵌套 object 需要手动指定 merge 行为。[^1]

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

Zustand 的 store 是一个 hook。它的标准 pattern 如下。[^2]

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

尽量使用原子的选择器，因为选择器返回的东西会触发 component 重渲染，`Array` 和 `Object` 永远被看作是新的结果。[^3]

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
