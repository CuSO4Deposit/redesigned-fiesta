# TODO

待办：想加进这一站的东西。这里只是草稿清单，随时改。

## 内容

- 主页正文（现在还是 “test text”）；中英两版。
- `/about`、`/uses`、`/colophon`、`/links` 独立页。
- 房间页：音频房、数据房的正式内容。

## 数据源（pipeline）

- rhythm（Arcaea）：投影已跑通，还没接到图。
- band（Gadgetbridge，走 CPI）。
- firefox（places.sqlite，走 CPI）。
- maloja（听歌 scrobble）。
- wakapi（写码时长）。
- video（PipePipe，走 CPI）。

## 图表

- Node + Observable Plot → `assets/charts/*.svg`。
- 把 `stat` / `chart` 短代码加回来（之前删了，用到再说）。

## 管线

- 把 `cpi`、`Y-Offline` 重新写成 git 依赖（不要 `../` 相对路径）：
  - CPI：`github.com/CuSO4Deposit/CPI`
  - Y-Offline：`codeberg.org/cocvu/Y-Offline`
- `translate` 命令（LLM 中→英，构建外跑）。

## 部署

- GitHub Pages：开启、Source 设为 Actions、自定义域 `depoze.xyz`、加 `static/CNAME`。

## 主题 / 基建

- hugo-tufte `index.html:15` 的 `.IsNode` 已废弃——首页列表非空时会警告。
- infra：给节点加 `tier` 属性 + public 生成器/lint。
