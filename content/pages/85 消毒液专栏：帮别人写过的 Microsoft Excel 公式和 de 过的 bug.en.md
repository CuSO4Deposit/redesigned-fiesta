---
title: "85 Disinfectant Column: Microsoft Excel Formulas I Wrote for Others and Bugs I Debugged"
ai: translated
date: 2026-01-17
lastMod: 2026-09-28
tags:
- Microsoft
categories:
summary: "Here I record the useful things I learned while writing Excel formulas for others, and the experience I gained dealing with Excel's strange behavior for them."
slug: excel-formulas
---

# Formulas


  + ## Creating a mask from two ranges


    + In Excel, performing an operation on two ranges of the same size directly yields a boolean array the same size as the range.


      + e.g.: `=(B1:B100 <= C1:C100)`


    + Excel also broadcasts automatically, a bit like numpy. If you perform an operation between a range and a single cell, Excel automatically treats it as an operation between each element in the range and the cell.

      + e.g.: `=(B1:B100 <= $C$1)`


  + ## Variable binding

    + Newer Excel versions introduced the LET function. It takes an odd number of arguments, where the last is the result returned by the LET formula, and the preceding arguments are, in order, variable names and the formulas bound to those variables. Formulas defined later can also use the variable names defined earlier.

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


# Strange Behavior

  + ## As long as I don't calculate, the formula is just text


    + When doing a bulk negation on a range and entering the formula `=B3:B1200 * (-1)`, I hit the following anomalies:


      + The cell does not display the calculated result, but instead shows the formula text verbatim.


      + When trying to troubleshoot via Excel's accessibility feature "Select Blocked Cells", I found that the option was **grayed out and unclickable**.

      + The cause was eventually tracked down: the **Formulas > Formula Auditing > Show Formulas** option was enabled. When this option is on, formulas are not calculated, and F9 etc. will not trigger a recalculation or refresh the page.

    + Other things that can produce this effect:

      + The cell format is "Text"


      + There are other cells with content below this cell, blocking the formula above from spilling over (in this case a "spill error" should be shown)

  + ## Cannot insert a new row

    + https://hsiaofeng.com/archives/374.html
