---
title: Probability of Christmas on Wednesday
date: 2021-10-14
lastMod: 2021-10-14
tags:
- mathematica
- NumberTheory
categories:
slug: christmas-probability
---

## Original Problem

Proof: In the system of the current Common Era, the probability of Christmas on Wed. is not 1/7.


## What exactly the probability is

In 400 years there are 303 non-leap years and 97 leap years. Total number of days:

$$T = 303\cdot 365 + 97\cdot 366\equiv 303 + 97\cdot 2\equiv 0\pmod 7.$$

This means: If the Christmas is on Mon. in year x, then it would be on Mon. in year (x + 400). That's to say, there's a difference between a day of the week and another day of the week.

### Solve in C

```C
/*
* {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
*
*       Filename:  LeapYear_Xmas.cpp
*
*    Description:  A program to count which day of the week does the X-mas falls. 
*
*        Version:  1.0
*        Created:  2021/10/9 20:31:35
*       Revision:  none
*       Compiler:  gcc
*
*         Author:  CuSO4_Deposit, CuSO4D@protonmail.com
*
* {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
*/

#include <stdio.h>
#include <iostream>

#define TRUE 1
#define FALSE 0
#define Status int
#define SUCCESS 1
#define FAILURE 0

#define FEB29 59
#define DEC25_nonleap 358

//Function Declaration
bool ifLeap(int year);
Status RunCalendar(int StartYearDay, int w[], int TrackDay);
int RunAYear(int weekday, int TrackDay);

//Function Implement
bool ifLeap(int year){
  /* 
   * {{< logseq/mark >}}=  FUNCTION  {{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}
   *         Name:  ifLeap
   *  Description:  if the year is leap, return 1; else return 0.
   *  Arguments: year: the year to be judged.
   * {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
   */
  if(!(year % 4)){
      if(!(year % 400))   return 1;
      if(!(year % 100))   return 0;
      return 1;
  }
  else return 0;
}

Status RunCalendar(int StartYearDay, int w[], int TrackDay){
  /* 
   * {{< logseq/mark >}}=  FUNCTION  {{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}
   *         Name:  RunCalendar
   *  Preconditon:  TrackDay can only be in a non-leap year(i.e. can't be Feb. 29).
   *  Description:  Run a calendar for 400 years, when the 1st day is StartYearDay, and
   *                  return the day of TrackDay through w[].
   *    Arguments:  StartYearDay: what day of the week is the 1st day.
   *                  w[]: how many times does TrackDay falls in weekday[i].
   *                  TrackDay: the day to track.
   * {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
   */  
  int NextYearStartDay = StartYearDay;

  if(TrackDay >= FEB29)
      for(int i = 0; i < 400; i++){
          w[RunAYear(NextYearStartDay, ifLeap(i) ? TrackDay + 1 : TrackDay)]++;
          NextYearStartDay = ifLeap(i) ? (NextYearStartDay + 366) % 7 : (NextYearStartDay + 365) % 7; 
      }
  else
      for(int i = 0; i < 400; i++){
          w[RunAYear(NextYearStartDay, TrackDay)]++;
          NextYearStartDay = ifLeap(i) ? (NextYearStartDay + 366) % 7 : (NextYearStartDay + 365) % 7;
      }
  return SUCCESS;
}

int RunAYear(int weekday, int TrackDay){
  /* 
   * {{< logseq/mark >}}=  FUNCTION  {{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}
   *         Name:  RunAYear
   *  Description:  Run a year, return what day of the week the targetday is on.  
   * {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
   */
  return (weekday + TrackDay % 7) % 7; 
}

int main(){
  int w[7] = {0}; //the day of the week array
  for(int i = 0; i < 7; i++){
      for(int j = 0; j < 7; j++) //array initialization
          w[j] = 0;
      RunCalendar(i, w, DEC25_nonleap);
      printf("When the 1st day of Year 0 is %d:\n", i);
      printf("S\tM\tT\tW\tT\tF\tS\n");
      for(int i = 0; i < 7; i++){
          printf("%d\t", w[i]);
      }
      printf("\n");
  } 
  return 0;
}
```

result:

When the 1st day of Year 0 is 0:
S M T W T F S
56 58 56 58 57 57 58
When the 1st day of Year 0 is 1:
S M T W T F S
58 56 58 56 58 57 57
When the 1st day of Year 0 is 2:
S M T W T F S
57 58 56 58 56 58 57
When the 1st day of Year 0 is 3:
S M T W T F S
57 57 58 56 58 56 58
When the 1st day of Year 0 is 4:
S M T W T F S
58 57 57 58 56 58 56
When the 1st day of Year 0 is 5:
S M T W T F S
56 58 57 57 58 56 58
When the 1st day of Year 0 is 6:
S M T W T F S
58 56 58 57 57 58 56
Hit any key to close this window...

As the Jan. 1st is on Sat in 2000, we know it's Sat. in year 0 too. Then our chronological system loops as what the 7th result shows. X-mas falls on Wednesday 57 times in 400 years. $$P = \dfrac{57}{400}.$$

### Solve in Wolfram Mathematica[ref] [试编程求圣诞节在星期三的具体概率？](https://www.zhihu.com/answer/397494528) [/ref]

```mathematica
Tally[DayName /@ Tuples[{Range[0, 399], Range[12, 12], {25}}]]
```

result:

```
{{Monday, 56}, {Tuesday, 58}, {Wednesday, 57}, {Thursday, 57}, {Saturday, 56}, {Sunday, 58}, {Friday, 58}}
```
