---
title: ⚛️💡 LLM Prompts
ai: translated
date: 2025-03-04
lastMod: 2026-09-28
tags:
- persistent-page
categories:
slug: llm-prompts
---

**en - Prompt Creator**


```
I want you to become my Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt will be used by you, ChatGPT. You will follow the following process:
Your first response will be to ask me what the prompt should be about. I will provide my answer, but we will need to improve it through continual iterations by going through the next steps.

Based on my input, you will generate 3 sections.

Revised Prompt (provide your rewritten prompt. it should be clear, concise, and easily understood by you)
Suggestions (provide 3 suggestions on what details to include in the prompt to improve it)
Questions (ask the 3 most relevant questions pertaining to what additional information is needed from me to improve the prompt)

At the end of these sections give me a reminder of my options which are:

Option 1: Read the output and provide more info or answer one or more of the questions
Option 2: Type "Use this prompt" and I will submit this as a query for you
Option 3: Type "Restart" to restart this process from the beginning
Option 4: Type "Quit" to end this script and go back to a regular ChatGPT session

If I type "Option 2", "2" or "Use this prompt" then we have finished and you should use the Revised Prompt as a prompt to generate my request
If I type "option 3", "3" or "Restart" then forget the latest Revised Prompt and restart this process
If I type "Option 4", "4" or "Quit" then finish this process and revert back to your general mode of operation

We will continue this iterative process with me providing additional information to you and you updating the prompt in the Revised Prompt section until it is complete.

```


**zh-cn - Prompt Creator**

```
我希望你成为我的提示词创建者。你的目标是帮助我为我的需求打造最佳提示词。这个提示将由你，ChatGPT 使用。你将遵循以下流程：
你的第一个回应将是询问我提示词应该关于什么。我会提供我的答案，但我们需要通过以下步骤的持续迭代来改进它。

根据我的输入，你将生成三个部分。

修订后的提示词（提供你的重写提示。它应该清晰、简洁，并且你能够轻松理解）
建议（提供3个关于在提示词中包含哪些细节以改进它的建议）
问题（询问3个最相关的问题，以获取更多信息以改进提示词）
在这些部分的末尾，给我一个关于我的选项的提醒：
选项1：阅读输出并提供更多信息或回答一个或多个问题
选项2：输入“使用此提示词”，我将提交此作为你的查询
选项3：输入“重启”以从头开始此过程
选项4：输入“退出”以结束此脚本并返回到常规的ChatGPT会话

如果我输入“选项2”、“2”或“使用此提示词”，那么我们已完成，你应该使用修订后的提示词作为生成我请求的提示词
如果我输入“选项3”、“3”或“重启”，那么忘记最新的修订提示词并重新开始此过程
如果我输入“选项4”、“4”或“退出”，那么结束此过程并恢复到你的常规工作模式

我们将继续这个迭代过程，我会向你提供更多信息，而你将在修订后的提示词部分更新提示词，直到它完成。

```


**zh-cn -  Emoji Translator**

```
请为以下文章标题生成一个包含不超过两个 emoji 的概括，确保 emoji 能准确传达标题的核心内容和情感基调，并能为不同的标题提供区分度：
```


**en - Translator**

```
I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations.
```


zh-cn - summary

```
请为我提供的文本生成一个简洁、准确的摘要，长度为一两句话。这个摘要应该能够让文章的读者快速了解文章所讲的内容和深度。
```


zh-cn - desensitization

```
请对以下文本进行脱敏处理。移除所有文件路径和用户名，并使用英文占位符（例如 [directory] 和 [username]）进行替换。确保命令本身、任何命令输出以及文本中的其他潜在敏感信息都得到妥善处理，使其无法识别原始路径和用户名。
```

