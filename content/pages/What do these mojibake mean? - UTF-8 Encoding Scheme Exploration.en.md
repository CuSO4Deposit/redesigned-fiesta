---
title: What do these mojibake mean? - UTF-8 Encoding Scheme Exploration
date: 2021-12-08
lastMod: 2021-12-08
tags:
  - Unicode
categories:
slug: utf8-mojibake
ai: translated
---

This article may contain horrific and gory videos. Be careful when clicking on the URLs. If you have any discomfort when browsing, please stop and leave.

## Introduction

We often meet mojibake, in games, web pages, or somewhere else. UTF-8 is the most widespread encoding scheme. These days @叉叉 and @北嘲 find some weird videos on YouTube, with obscure titles and terrifying cover. We are curious about the origin of these creepy videos. This article is to record our exploration process.

Some Example Videos

[.... ø·ø ̈ùšù„ø© ... ø£øoù†ùšø© ù„ù„ø£ø·ù ø§ù„ ... ù„ùšø ̈ùšø§](https://www.youtube.com/watch?v=6fAE1VxKbOQ)
[.. آمراة تدعى أنها السيدة مريم العذراء بأنها متزوجة من المسيح](https://www.youtube.com/watch?v=Fxd_bUi3cog)

## Exploration

#### Association with encoding

When @叉叉 first send me the video title (.... ø·ø ̈ùšù„ø© ... ø£øoù†ùšø© ù„ù„ø£ø·ù ø§ù„ ... ù„ùšø ̈ùšø§), it reminds me of what my misconfigured C-language IDE returns me as console error info:

What the IDE returns: "²»ÊÇÄڲ¿»òÍⲿÃüÁҲ²»ÊǿÉÔËÐеĳÌÐò
»òÅú´¦ÀíÎļþ¡£"

This is apparently a decoding error. Characters are all Latin Characters. Remind me of some schemes like ISO 8859-1. @叉叉 found that of these titles, some are mojibake and the other are Arabic. So I put my attention on Arabic Encoding.

#### Organize known information

@北嘲 and @刺刺 provide the following conclusion: we have many videos, with similar, creepy contents. The titles are 2 kinds: mojibake and Arabic. But all the Arabic-titled videos nearly have the same title: ".. آمراة تدعى أنها السيدة مريم العذراء بأنها متزوجة من المسيح" which means "yes A woman who claimed to be the Virgin Mary married Jesus."

All these videos have one or more "."(full stop punctuation) in there title. And there are some "Don't search full stop punctualation on Youtube", "YouTube's dark side" trends on YouTube. Guess this "." may be an "Entrance" the authors left for the viewers.

@北嘲 also found a Youtuber updated a video with an introduction full of 0-1 strings. It attracts my attention. The mojibake may be the real garbled mojibake, but in 0-1 strings must hides some infomation, this must be a useful infomation. So I went on to find the meaning of this 0-1 string.

what @北嘲 found

The content of the 0-1 string:

001011100010000011011000101000101101100110000101110110001011000111011000101001111101100010101001001000001101100010101010110110001010111111011000101110011101100110001001001000001101100010100011110110011000011011011001100001111101100010100111001000001101100010100111110110011000010011011000101100111101100110001010110110001010111111011000101010010010000011011001100001011101100010110001110110011000101011011001100001010010000011011000101001111101100110000100110110001011100111011000101100001101100010110001110110001010011111011000101000010010000011011000101010001101100010100011110110011000011011011001100001111101100010100111001000001101100110000101110110001010101011011000101100101101100110001000110110001010110011011000101010010010000011011001100001011101100110000110001000001101100010100111110110011000010011011001100001011101100010110011110110011000101011011000101011010010000011011000

#### Directly converting - New Mojibake found

A simple thought is to directly read these bits, and each 8 bit I output an ASCII character. This is the first version of this program.

```C
/*
* {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
*
*       Filename:  01-to-ASCII.cpp
*
*    Description:  An converter, input 0-1 string and output ASCII.
*
*        Version:  1.0
*        Created:  2021/12/6 11:52:42
*       Revision:  none
*       Compiler:  gcc
*         Author:  CuSO4_Deposit (depoze.xyz), CuSO4D@protonmail.com
*
* {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
*/
#include <stdio.h>
#include <iostream>

#define INPUT_PATH ".\\input.txt"
#define OUTPUT_PATH ".\\output.txt"

int main(){
  FILE* fpi;
  FILE* fpo;
  if ((fopen_s(&fpi, INPUT_PATH, "r"))){
      printf("Cannot open the input file.\n");    
  exit(-1);
  } 
  if ((fopen_s(&fpo, OUTPUT_PATH, "w"))){
      printf("Cannot open the output file.\n");    
  exit(-1);
  }
  char Word = 0;
  char temp;
//  int counter = 100;  // At first I don't know why feof() doesn't work, so I have to
//                      //   manually specify the loop counter.
  while(1){
//      if (counter-- == 0)    break;
      unsigned char mask = 0x80;
      Word = 0;
      for(int i = 0; i < 8; i++){
          if(feof(fpi)) break;
          temp = fgetc(fpi);
          switch(temp){
              case '0':   break;
              case '1':   Word = Word  mask;    break;
              default:    
                  printf("\n Unexpected character: %c, 0x%x", temp, temp);
                  break;
          }
          mask = mask >> 1;
      }
      if(feof(fpi))   break;
      fputc(Word, fpo);
      printf("%c, 0x%x\n", Word, Word);
  }
  return 0;
}
```

This program's output file:

. 丌賲乇丕丞 鬲丿毓賶 兀賳賴丕 丕賱爻賷丿丞 賲乇賷賲 丕賱毓匕乇丕亍 亘兀賳賴丕 賲鬲夭賵噩丞 賲賳 丕賱賲爻賷丨 ?

When I thought I got something wrong, I find this new kind of mojibake has some relationship with Arabic: When I type them into Bing, the seraching result(containg these mojibake) all contains Arabic. Here are some examples of the searching results:

[http://stg-learn.sketchup.com/u-23497.php](http://stg-learn.sketchup.com/u-23497.php)
[https://www.docin.com/p-2280050009.html](https://www.docin.com/p-2280050009.html)
[https://xueshu.baidu.com/usercenter/paper/show?paperid=10668a70e990c9fd526b3e0382dfaf16](https://xueshu.baidu.com/usercenter/paper/show?paperid=10668a70e990c9fd526b3e0382dfaf16)

Screenshots

That's to say, what I decode is not completely wrong. At least it has something to do with Arabic.

#### Dig Deeper - UTF-8 scheme

As mentioned in the code comment, when debugging, I use a manual loop counter. By accident I find that, sometimes in the output file there is a complete Arabic sentence, not garmbled words:

. آمراة تدعى أنها السيدة مريم

This is when the loopcounter is set to 50. But when I reset to 100, it will becomes garbled again. But 101 was OK. Then I printed it out byte by byte:

```
., 0x2e
, 0x20
? 0xffffffd8
? 0xffffffa2
? 0xffffffd94
? 0xffffff85
? 0xffffffd8
? 0xffffffb1
? 0xffffffd8
? 0xffffffa7
? 0xffffffd8
? 0xffffffa9
, 0x20
? 0xffffffd8
? 0xffffffaa
? 0xffffffd8
? 0xffffffaf
? 0xffffffd8
? 0xffffffb9
? 0xffffffd9
? 0xffffff89
, 0x20
? 0xffffffd8
? 0xffffffa3
? 0xffffffd9
? 0xffffff86
? 0xffffffd9
? 0xffffff87
? 0xffffffd8
? 0xffffffa7
, 0x20
? 0xffffffd8
? 0xffffffa7
? 0xffffffd9
? 0xffffff84
? 0xffffffd8
? 0xffffffb3
? 0xffffffd9
? 0xffffff8a
? 0xffffffd8
? 0xffffffaf
? 0xffffffd8
? 0xffffffa9
, 0x20
? 0xffffffd9
? 0xffffff85
? 0xffffffd8
? 0xffffffb1
? 0xffffffd9
? 0xffffff8a
? 0xffffffd9
? 0xffffff85
, 0x20
? 0xffffffd8
? 0xffffffa7
? 0xffffffd9
? 0xffffff84
? 0xffffffd8
? 0xffffffb9
? 0xffffffd8
? 0xffffffb0
? 0xffffffd8
? 0xffffffb1
? 0xffffffd8
? 0xffffffa7
? 0xffffffd8
? 0xffffffa1
, 0x20
? 0xffffffd8
? 0xffffffa8
? 0xffffffd8
? 0xffffffa3
? 0xffffffd9
? 0xffffff86
? 0xffffffd9
? 0xffffff87
? 0xffffffd8
? 0xffffffa7
, 0x20
? 0xffffffd9
? 0xffffff85
? 0xffffffd8
? 0xffffffaa
? 0xffffffd8
? 0xffffffb2
? 0xffffffd9
? 0xffffff88
? 0xffffffd8
? 0xffffffac
? 0xffffffd8
? 0xffffffa9
, 0x20
? 0xffffffd9
? 0xffffff85
? 0xffffffd9
? 0xffffff86
, 0x20
? 0xffffffd8
? 0xffffffa7
? 0xffffffd9
```

It's clear that the single-byte character 0x20 interrupted the decoding process, maybe made a double-byte character separated then caused the garmbled. So I should learn how UTF-8 is encoded.

**UTF-8** is a **variable-width** character encoding used for electronic communication. Defined by the Unicode Standard, the name is derived from _Unicode_ (or _Universal Coded Character Set_) _Transformation Format – 8-bit_. While Unicode is a character set.
[UTF-8 - From Wikipedia, the free encyclopedia](https://en.wikipedia.org/wiki/UTF-8)

First code point

Last code point

```
Byte 1

Byte 2

Byte 3

Byte 4

U+0000

U+007F

0xxxxxxx

U+0080

U+07FF

110xxxxx

10xxxxxx

U+0800

U+FFFF

1110xxxx

10xxxxxx

10xxxxxx

U+10000

[nb 2](https://en.wikipedia.org/wiki/UTF-8#cite_note-16)U+10FFFF

11110xxx

10xxxxxx

10xxxxxx

10xxxxxx
```

Unicode <-> UTF-8

Example:

D (U+0044) -> 01000100 (same with its ASCII: 0x44), that's to say UTF-8 is downward compatible with ASCII.

沉 (U+6C89) -> (1110)0110 (10)110010 (10)001001. (0x6C89 -> 0110 1100 1000 1001)

A Chinese character takes 3 bytes to save. While an Arabic character takes 2 bytes.

But as a variable-width character, UTF-8 is a prefix code, won't create this kind of error(separating 2 bytes, making the whole seentence error).

To solve this puzzle, I add bit-by-bit printing code to the decoding program:

```C
switch(temp){
              case '0':   printf("0"); break;
              case '1':   printf("1");    Word = Word  mask;    break;
              default:    
                  printf("\n Unexpected character: %c, 0x%x", temp, temp);
                  break;
          }
          mask = mask >> 1;
      }
```

When loopcounter is set to 100 or 101, these are what they ouput:

```
100:
00101110
00100000
11011000
10100010
11011001
10000101
11011000
10110001
11011000
10100111
11011000
10101001
00100000
11011000
10101010
11011000
10101111
11011000
10111001
11011001
10001001
00100000
11011000
10100011
11011001
10000110
11011001
10000111
11011000
10100111
00100000
11011000
10100111
11011001
10000100
11011000
10110011
11011001
10001010
11011000
10101111
11011000
10101001
00100000
11011001
10000101
11011000
10110001
11011001
10001010
11011001
10000101
00100000
11011000
10100111
11011001
10000100
11011000
10111001
11011000
10110000
11011000
10110001
11011000
10100111
11011000
10100001
00100000
11011000
10101000
11011000
10100011
11011001
10000110
11011001
10000111
11011000
10100111
00100000
11011001
10000101
11011000
10101010
11011000
10110010
11011001
10001000
11011000
10101100
11011000
10101001
00100000
11011001
10000101
11011001
10000110
00100000
11011000
10100111
11011001

110:
00101110
00100000
11011000
10100010
11011001
10000101
11011000
10110001
11011000
10100111
11011000
10101001
00100000
11011000
10101010
11011000
10101111
11011000
10111001
11011001
10001001
00100000
11011000
10100011
11011001
10000110
11011001
10000111
11011000
10100111
00100000
11011000
10100111
11011001
10000100
11011000
10110011
11011001
10001010
11011000
10101111
11011000
10101001
00100000
11011001
10000101
11011000
10110001
11011001
10001010
11011001
10000101
00100000
11011000
10100111
11011001
10000100
11011000
10111001
11011000
10110000
11011000
10110001
11011000
10100111
11011000
10100001
00100000
11011000
10101000
11011000
10100011
11011001
10000110
11011001
10000111
11011000
10100111
00100000
11011001
10000101
11011000
10101010
11011000
10110010
11011001
10001000
11011000
10101100
11011000
10101001
00100000
11011001
10000101
11011001
10000110
00100000
11011000
10100111
11011001
10000100
```

It's clear that loopcounter {{< logseq/mark >}} 100 split the last double-byte character. ("11011001 10000100" -> "11011001"), and loopcounter {{< / logseq/mark >}} 101 solves this problem. But this will only cause the last character's decoding error, why does the entire sentence falls into garbled words? The lower right corner of the Notepad draws my attention:

The status bar shows that they are now decoded in different schemes(ANSI, UTF-8).

Windows runs in UTF-8. The last character was cut up, which caused the notepad think it is ANSI(GBK, in China)-encoded. At the time I copy these words into clipboard, Windows automatically converts the encoding scheme of contents to UTF-8, keeping the characters unchanged. This process entirely damaged the original 0-1 code of the string.

A guessing

To verify this guessing, I read the Arabic's code byte-by-byte, and it's first 2 Arabic bytes are: "11011000 10100010 11011001 10000101"(a.k.a. 0xD8A2 0xD985). And I find a GBK encoding chart:
[Understanding GBK (with a full character encoding list): the high bit of the low byte of the expanded 20,000 Chinese characters is not equal to 1, and many encoding spaces remain unused](https://www.cnblogs.com/findumars/p/4541421.html)(Already known that GBK is a 2-byte character encoding scheme), go find the 0xD8A2 and the 0xD985, corresponding to "丌" and "賲", this verifies my guessing.

Knowing this, I can specify the loopcounter, not separating a character to 2 parts. Then I can get the complete original sentence:

.. آمراة تدعى أنها السيدة مريم العذراء بأنها متزوجة من المسيح

This Arabic sentence(decoded from an introduction of a video) and the Arabic titles we first found, are identical.

#### Other mojibake

Knowing the process of decoding this kind of mojibake, it's then possible to decode the another:

.... ø·ø ̈ùšù„ø© ... ø£øoù†ùšø© ù„ù„ø£ø·ù ø§ù„ ... ù„ùšø ̈ùšø

It looks like some latin characters. So I should find how latin characters are encoded in Europe if we don't use UTF-8. I asked this question to @Erik, and his answer is Windows-1252.

Windows 1252 is a single-byte character encoding of the Latin Alphabet.[Windows-1252 - From Wikipedia, the free encyclopedia](https://en.wikipedia.org/wiki/Windows-1252)When keeping the character identical, the binary code has to convert like this:

Windows-1252(Hex) Windows-1252(Bin) -> UTF-8(bin)
0x00 - 0x7f 0xxxxxxx -> 0xxxxxxx
0x80 - 0xff 1xxxxxxx -> 1100001x 10xxxxxx

Code:

```C
/*
* {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
*
*       Filename:  Windows1252-to-UTF8.cpp
*
*    Description:  convert input Windows1252 encoded characters to UTF8 encoded char.
*                      Keeping the char identical, the code changes.
*        Version:  1.0
*        Created:  2021/12/8 18:20:44
*       Revision:  none
*       Compiler:  gcc
*         Author:  CuSO4_Deposit (depoze.xyz), CuSO4D@protonmail.com
*
* {{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}{{< logseq/mark >}}{{< / logseq/mark >}}=
*/
#include <stdio.h>
#include <iostream>

#define INPUT_PATH ".\\input.txt"
#define OUTPUT_PATH ".\\output.txt"

int main(){
  FILE* fpi;
  FILE* fpo;
  if ((fopen_s(&fpi, INPUT_PATH, "r"))){
      printf("Cannot open the input file.\n");    
  exit(-1);
  } 
  if ((fopen_s(&fpo, OUTPUT_PATH, "w"))){
      printf("Cannot open the output file.\n");    
  exit(-1);
  }
  unsigned char Word1 = 0;
  unsigned char Word2 = 0x80; // Word2 = 10000000b 
  unsigned char temp;
  int counter = 50;   //   manually specify the loop counter.
  while(1){
      if (counter-- == 0)    break;
      Word1 = 0; 
      temp = fgetc(fpi);
      if(temp >= 0x00 && temp <= 0x7f){   //temp = 0xxxxxxxb
          Word1 = Word1  temp;   //Word1 initially == 0x00
          fputc(Word1, fpo);
          printf("0x%x\n", Word1);
      }
      else{   // temp = 1xxxxxxxb
          if(0x40 & temp) //temp = 11xxxxxxb
              Word1 = 0xc3;   //Word1 = 11000011b
          else    //temp = 10xxxxxb
              Word1 = 0xc2;   //Word1 = 11000010b
          fputc(Word1, fpo);
          printf("0x%x\t", Word1);
          Word2 = temp;   //Word2 = 1yxxxxxxb
          Word2 = Word2 & 0xbf; // Word2 = 10xxxxxxb
          fputc(Word2, fpo);
          printf("0x%x\n", Word2);
      }
  }
  return 0;
}
```

Sadly, the output doesn't make any sense:

.... Ã¸Â·Ã¸ ÌÃ¹Å¡Ã¹âÃ¸Â© ... Ã¸Â£Ã¸oÃ¹â Ã¹Å¡Ã¸

After checking each character, it turns out the program works well. The reason may be the followings:

This mojibake isn't generated by this kind of decoding error, maybe just garbled words;

This is generated by decoding error, but the origin language isn't Latin(not using Windows-1252)

To be continued...
