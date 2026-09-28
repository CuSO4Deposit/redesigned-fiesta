---
title: Leetcode 142 - Linked List Cycle II
date: 2023-04-26
lastMod: 2025-10-18
tags:
- LeetCode
- linklist
- pointer
- 快慢指针
categories:
---

## Problem

Given the `head` of a linked list, return *the node where the cycle begins. If there is no cycle, return* `null`.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to (**0-indexed**). It is `-1` if there is no cycle. **Note that** `pos` **is not passed as a parameter**.

**Do not modify** the linked list.

Example 1:

**Input:** head = [3,2,0,-4], pos = 1
**Output:** tail connects to node index 1
**Explanation:** There is a cycle in the linked list, where tail connects to the second node.

Example 2:

**Input:** head = [1], pos = -1
**Output:** no cycle
**Explanation:** There is no cycle in the linked list.


## My Solution

I have explored this problem 2 yrs ago. [Link](/pages/单链表的含环和相交性质探究过程记录/)

In that post I mostly focused on the correctness of two-pointer algorithm, but did not explain well on how to solve this problem. So I write another post here to explain the solution of this problem.

(Color in this image: #0E9E69 Green Haze)

Let 2 pointers `fp` and `sp` point to `head`. In each iteration, `sp` moves ahead 1 step one time while `fp` moves ahead 2. Stop the loop when `fp` and `sp` are at the same node. `s` denotes the final position of the slower pointer (also the final position of the faster), and `f_0` denotes the positon of the faster pointer when the slower pointer has just enter the circle. L_c denotes the length of circle. L_f,\ L_s denote the total length the faster and the slower goes. Other lengths' notations are in the figure.

We have the following equations:

```
L_f = 2L_s.
```

since at every iteration, `fp` moves 2 steps and `sp` moves 1.

```
L_s = L_0 + L_{fs}.
```

since we define the distance between `s` and the node where cycle begins as L_{fs}.

```
L_s = L_f - L_s = nL_c.
```

The 1st equal sign holds because L_f = 2L_s. The 2nd equal sign holds because `fp` just moves several more cycles than `sp` - they start from the same node and stops from the same node.

Alg:

Use fast-and-slow pointers to traverse the linklist from `head`. Record the node where `fp` and `sp` meets as `s`. We also have L_f and L_s.

Use fast-and-slow pointers to traverse the linklist, starting from `s`. Record the distance `sp` goes, it should be L_c, since `fp` moves 1 step relative to `sp`. so we can solve n = \frac{L_s}{L_c}.

Let a pointer `p` starts from `head` and goes (n - 1)L_c steps. Since L_s = L_0 + L_{fs} = nL_c, distance between `p` and the node where the cycle begins is L_c - L_{fs}. Let a pointer `q` points to s. The distance between `q` and the node where the cycle begins is also L_c - L_{fs}.

Let `p` and `q` moves at the same speed of 1. The node where they meet should be where the cycle begins.

## My Implementation (in C)

```C
/**
* Definition for singly-linked list.
* struct ListNode {
*     int val;
*     struct ListNode *next;
* };
*/

struct ListNode* fsTraverse(struct ListNode* list, int* n){
  // return the node where fast and slow pointer meets
  // (*n) records the # of steps the slow pointer goes
  struct ListNode* f = list;
  struct ListNode* s = list;
  *n = 0;
  while (1){
      if (f == NULL)
          return NULL;
      f = f->next;
      if (f == NULL)
          return NULL;
      s = s->next;
      (*n)++;
      f = f->next;

      if (f == s)
          return f;
  }
}

struct ListNode *detectCycle(struct ListNode *head) {
  int Ls = 0; 
  struct ListNode* meet = fsTraverse(head, &Ls);
  if (meet == NULL)
      return NULL;
  int Lc = 0;
  fsTraverse(meet, &Lc); // Lc is the length of the circle.
  int n = Ls / Lc;

  struct ListNode* p = head;
  for (size_t i = 0; i < (n - 1) * Lc; i++) {
      p = p->next;
  }

  while (p != meet){
      p = p->next;
      meet = meet->next;
  }
  return p;
}
```
