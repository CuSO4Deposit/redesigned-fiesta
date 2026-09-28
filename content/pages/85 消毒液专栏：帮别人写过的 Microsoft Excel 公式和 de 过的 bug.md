---
title: 85 消毒液专栏：帮别人写过的 Microsoft Excel 公式和 de 过的 bug
date: 2026-01-17
lastMod: 2026-01-17
tags:
- Microsoft
categories:
summary: 这里记录下我帮别人写 Excel 公式时候学到的有用的东西，以及帮别人处理 Excel 的奇怪行为时候的经验。
---

# 公式


  + ## 从两个区域创建 mask


    + Excel 中对两个相同大小的区域进行运算，可以直接获得一个和这个区域一样大的布尔数组


      + 如：`=(B1:B100 <= C1:C100)`


    + Excel 还会自动拓展，有点像 numpy。如果你将一个区域和一个单元格进行运算，Excel 会自动当成是这个区域里的每一个元素和单元格作运算。

      + 如：`=(B1:B100 <= $C$1)`


  + ## 变量绑定

    + 较新的 Excel 版本引入了 LET 公式，它接受奇数个参数，其中最后一个为 LET 公式返回的结果，而前面的参数依次为变量名和变量绑定的公式。后面定义的公式也可以使用前面的变量名。

```excel
=LET(
    name, C2,
    dates, '$B$8:$B$114514,
    speakers, '$G$8:$G$114514,
    cutoff, EOMONTH(TODAY(), -1),
    condition, (dates <= cutoff) * (ISNUMBER(SEARCH(name, speakers))),
    selected, FILTER(dates, condition),
    latest, MAX(selected),
    latest
)
```


# 奇怪行为

  + ## 只要我不计算，公式就是文本


    + 在对一个范围进行批量取反运算时，输入公式 `=B3:B1200 * (-1)`，遇到以下的异常：


      + 单元格不显示计算结果，而是直接显示公式原文。


      + 尝试通过 Excel 的辅助功能“选择受阻单元格”进行排查时，发现该选项为**灰色不可点击**状态。

      + 最终排查出原因：**公式 > 公式审核 > 显示公式**选项是开启的。这个选项开启将使得公式不会计算，且 F9 等也不会触发计算和页面更新。

    + 也能产生这种效果的事情：

      + 单元格的格式是“文本”


      + 这个单元格下方存在其他有内容的单元格，阻挡上方公式溢出（这时应当显示“溢出错误”）

  + ## 无法插入新行

    + https://hsiaofeng.com/archives/374.html

