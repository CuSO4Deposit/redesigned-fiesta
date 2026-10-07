---
title: Crawl song lyrics in NetEase
date: 2022-02-08
lastMod: 2022-02-08
tags:
categories:
slug: netease-lyrics
---

## Introduction

Beginning to learn Python, @Zei_Wai and I want to do some simple tasks, instead of diving into the sea of the documentation of Python. Then we chose this: generating a WordCloud picture of the lyrics of NeteaseMusic Songlist.


## Using urllib package

First we found an api of Netease:

[https://music.163.com/api/song/lyric?id=<song.id>&lv=1&kv=1&tv=-1](https://music.163.com/api/song/lyric?id=%3Csong.id%3E&lv=1&kv=1&tv=-1)

where <song.id> is the id of songs in Netease database. When we use web client to play music, the URL of music playing page contains this id. For a simple example, if we want to get the lyrics of *Bad Apple!!* we just need to do like this:

Then we just need to get the songs' id in a automatic way, then we can generate a text file. But when we use this method to send request to Netease Songlist page, what it returns doesn't contain songid. This is the code we use:[【python爬虫自学笔记】-----爬取网易云歌单中歌曲歌词](https://blog.csdn.net/m0_38103546/article/details/81666687)

```python
import json
import requests
import re
import urllib
from bs4 import *

def get_html(url):
  myheaders = {
          "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11 ",
          "Referer": "http://music.163.com/",
          "Host": "music.163.com"
          }
  try:
      response = requests.get(url, headers= myheaders)
      html = response.text
      return html
  except:
      print('request error')
      pass
print(get_html("https://music.163.com/#/playlist?id=117012154"))
myurl = "https://music.163.com/#/playlist?id=117012154"
myheaders = {
      "Host" : "music.163.com",
      "User-Agent" : "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11 "
      }
myrequest = urllib.request.Request(myurl, headers = myheaders)
myresponse = urllib.request.urlopen(myrequest)
html = myresponse.read().decode('utf-8', 'ignore')
soup = BeautifulSoup(html, 'lxml')
file = open('/home/cuso4d/Archives/Python/NeteaseCrawler/NeteasePageEx.txt', 'w')
file.write(soup.prettify())
file.close()
print("done")
```

And here are some pieces of file it returns, it's not what we expected.

expected

actual result

According to a Zhihu article, it's because Netease hides its data, we need to figure out a "real" url of song list. Code:[利用Python网络爬虫抓取网易云音乐歌词](https://zhuanlan.zhihu.com/p/208837699)

```python
import json
import requests
import re
import urllib
from bs4 import *

def get_html(url):
  myheaders = {
          "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11 ",
          "Referer": "http://music.163.com/",
          "Host": "music.163.com"
          }
  try:
      response = requests.get(url, headers= myheaders)
      html = response.text
      return html
  except:
      print('request error')
      pass
file = open('/home/cuso4d/Archives/Python/NeteaseCrawler/NeteasePageEx.txt', 'w')
file.write(get_html("https://music.163.com/#/playlist?id=117012154"))
file.close()
print("done")
```

But sadly the result html still remains the ${x.id} form. Maybe Netease has updated its code and the tutorial I followed are all outdated.

## Using cloudmusic package

[github author = "p697" project = "cloudmusic"][/github]

Using this package, implementing our goal is just a simple thing.

```python
import cloudmusic
import re

User = cloudmusic.getUser(114514) # 114514: userid 

def PrettifyLyrics(LyricsWithTimeline):
  return re.sub("[^\u4e00-\u9fa5+]",'', LyricsWithTimeline)

file = open("/home/cuso4d/Archives/Python/NeteaseCrawler/Lyrics.txt", 'a+')
Record = User.getRecord(1)   # Argument 1 means Recent 1 week, 0 means Total history.
for SingleRecord in Record:                   # SingleRecord is Dict
  SingleMusic = SingleRecord["music"]       # SingleMusic is MusicObj
  SingleLyric = SingleMusic.getLyrics()[1]  # 1 means Translated lyrics.
  file.write(PrettifyLyrics(SingleLyric))
file.close()
print("done")
```

Since we use Chinese translated lyrics to create WordCloud(in case of listening many languages and can't unify), we use 1 as the argument of getLyrics.

Cloudmusic package is good, but it hasn't been maintained for 2 years. When getting data of abstract music, python returns a KeyError. So I have to edit the package file:

```python
# 获取歌词
  def getLyrics(self):
      lrc =  api.Api().get_lyrics(dict(ID = self.id))
      lyric = ""
      tlyric = ""

      if "lrc" in lrc:
          lyric = lrc["lrc"]["lyric"]
          if "tlyric" in lrc:                         # Edited to support Absolute Music
              if "lyric" in lrc["tlyric"]:
                  tlyric = lrc["tlyric"]["lyric"]
          else:                                       # Edited to support Absolute Music
              print(self.id, self.name, '-', self.artist)     # Edited to support Absolute Music
      return [lyric, tlyric]

//music.Obj, Line 114
```

Then the program can work well, generating a file full of Chinese Lyrics:

## WordCloud

To be continued...

## Integration

### File Organization:

After generating process, two files "Lyrics.txt" and "wd-picture.jpg" will appear in output directory.

### Readme.md

We use package:

cloudmusic
re
wordcloud
image
jieba

Before starting, please edit the musicObj.py in cloudmusic package [like this](#FixAbstractMusic).

You can get the id of user from the URL of the personal page in Netease. Please ensure one has enabled "visible to everyone" settings of the Song Ranking.

### start.bash

Simply running the main program:

```
#!/bin/bash
python3 "./input/NeteaseLyricsCloud.py"
```

### Main program:

```python
#      Filename: NeteaseLyricsCloud.py
#
#   Description: Crawl data from Netease Music, make a wordcloud out
#                 of the Record of recent 1 week.
#
#       Version: 1.0
#       Created: 2022/02/05 20:52:00
#        Author: Zei_Wai & CuSO4_Deposit, CuSO4D@protonmail.com
#
#

# Support for Crawler
import cloudmusic
import re

# Support for WordCloud
from wordcloud import WordCloud
import PIL .Image as image
import jieba

def jbcut(t):
  result=' '.join(jieba.cut(t))
  return result

def PrettifyLyrics(LyricsWithTimeline):
  return re.sub("[^\u4e00-\u9fa5+]",'', LyricsWithTimeline)

print("Please input your Netease user id:")
userid = input()
User = cloudmusic.getUser(userid) 
file = open("./output/Lyrics.txt", 'a+')
Record = User.getRecord(1)   # Argument 1 means Recent 1 week, 0 means Total history.
for SingleRecord in Record:                   # SingleRecord is Dict
  SingleMusic = SingleRecord["music"]       # SingleMusic is MusicObj
  SingleLyric = SingleMusic.getLyrics()[1]  # 1 means Translated lyrics.
  file.write(PrettifyLyrics(SingleLyric))
file.close()

with open("./output/Lyrics.txt") as fp:
          text = fp.read()
          text = jbcut(text)

          cn_stpwords = set()
          content = [line.strip() for line in open('./input/stopwords.txt','r').readlines()]
          cn_stpwords.update(content)

          WordCloud = WordCloud(stopwords=cn_stpwords,font_path='./input/Fonts.TTF',width=800,height=800).generate(text)
          image_produce = WordCloud.to_image()
          image_produce.save('./output/wd-picture.jpg')

print("All done")
```

## Result Output

やっぱり世界（
