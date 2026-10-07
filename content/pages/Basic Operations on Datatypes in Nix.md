---
title: Basic Operations on Datatypes in Nix
date: 2024-07-09
lastMod: 2024-07-09
tags:
- Nix
categories:
slug: nix-datatypes
---

## Attribute sets


  + This is an example code, where `ex0` to `ex7` are evaluated to true.
```nix
with import <nixpkgs> { };
with lib;
let
  attr = {a="a"; b = 1; c = true;};
  s = "b";
in
{
  #replace all X, everything should evaluate to true
  ex0 = isAttrs attr;
  ex1 = attr.a == "a";
  ex2 = attr.${s} == 1;
  ex3 = attrVals ["c" "b"] attr == [ true 1 ];
  ex4 = attrValues attr == [ "a" 1 true ];
  ex5 = builtins.intersectAttrs attr {a="b"; d=234; c="";} 
    == { a = "b"; c = "";};
  ex6 = removeAttrs attr ["b" "c"] == { a="a"; };
  ex7 = ! attr ? a == false;
}
```
source: https://nixcloud.io/tour/?id=attrset/examples


  + This is an example code, where `ex0` and `ex1` are evaluated to true.
```nix
let
  list = [ { name = "foo"; value = 123; }
           { name = "bar"; value = 456; } ];
  string = ''{"x": [1, 2, 3], "y": null}'';
in 
{
  ex0 = builtins.listToAttrs list == { foo = 123; bar = 456; };
  ex1 = builtins.fromJSON string == { x = [ 1 2 3 ]; y = null; };
}
```
source: https://nixcloud.io/tour/?id=attrset/examples2

  + This is an example code, where `exBonus` is evaluated to true.
```nix
let
  attrSetBonus = {f = {add = (x: y: x + y);
                       mul = (x: y: x * y);};
                  n = {one = 1; two = 2;};};
in
rec {
  #Bonus: use only the attrSetBonus to solve this one
  exBonus = with attrSetBonus; 5 == f.add ( f.mul n.two n.two ) n.one;
}
```
source: https://nixcloud.io/tour/?id=attrset/examples3

  + Attrsets support mapping operations. See `nixpkgs.lib.mapAttrs`.
```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  attrSet = { a = -2; b = 3; };
in 
{
  ex0 = lib.mapAttrs (k: v: v * 7) attrSet;
}
```
source: https://nixcloud.io/tour/?id=mapAttrs

## Lists

  + This is an example on basic functions on lists. `ex\d` are all evaluated to true.
```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  list = [2 "4" true false {a = 27;} false 3];
  f = x: isString x;
  s = "foobar";
in
{
  #replace all X, everything should evaluate to true
  ex00 = isList list;
  ex01 = elemAt list 2 == true;
  ex02 = length list == 7;
  ex03 = last list == 3;
  ex04 = filter f list == [ "4" ];
  ex05 = head list == 2;
  ex06 = tail list == [ "4" true false {a = 27;} false 3 ];
  ex07 = remove true list == [ 2 "4" false {a = 27;} false 3 ];
  ex08 = toList s == [ "foobar" ];
  ex09 = take 3 list == [ 2 "4" true ];
  ex10 = drop 4 list == [ {a = 27;} false 3 ];
  ex11 = unique list == [ 2 "4" true false {a = 27;} 3 ];
  ex12 = list ++ ["x" "y"] == [ 2 "4" true false {a = 27;} false 3 "x" "y" ];
}

```
source: https://nixcloud.io/tour/?id=lists/operations


  + Lists support mapping operations. See `builtins.map`:
```nix
let
  numbers = [1 2 3 4];
in
{
  #multiplies every number by 2
  example = map (n: n * 2) numbers; 
}
```
source: https://nixcloud.io/tour/?id=map

  + Lists support fold. See `nixpkgs.lib.fold`.
`fold func init [x_1 x_2 ... x_n] == func x_1 (func x_2 ... (func x_n init))`
`foldl func init [x_1 x_2 ... x_n] == func (... (func (func init x_1) x_2) ... x_n)`.
```nix
with import <nixpkgs> { };
with lib;
let
  list = ["a" "b" "a" "c" "d" "a"];
  intList = [ 1 2 3 ];
  countA = fold (x: y: if (x == "a") then (y+1) else y) 0;
  mulB = fold (x: y: [ (2 * x) ] ++ y) [8];
in
rec {
  example = fold (x: y: x + y) "z" ["a" "b" "c"]; #is "abcz"
  ex0 = countA list; #should be 3
  ex1 = mulB intList; #should be [ 2 4 6 8 ]
}
```

    + ### Reimplementations using fold


      + Reverse List (`lib.reverseList`)
```nix
reverseList = lib.fold (x: y: y ++ [ x ]) [];
```
source: https://nixcloud.io/tour/?id=reimplementation/reverselist


      + Map (`builtins.map`)
```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  myMap = a: b: lib.fold (x: y: [ (a x) ] ++ y) [] b; 
in
rec {
  #your map should create the same result as the standard map function
  example = map (x: builtins.div x 2) listOfNumbers; 
  result = myMap (x: builtins.div x 2) listOfNumbers;
}
```
source: https://nixcloud.io/tour/?id=reimplementation/map
