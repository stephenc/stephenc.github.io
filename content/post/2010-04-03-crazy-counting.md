---
title: "Crazy counting..."
date: 2010-04-03T00:00:00Z
tags: []
---

When you are keeping build/version number in strings, you really need to left pad with 0's in order for string sorting to work...

e.g. `1.0-alpha-2` > `1.0-alpha-1` > `1.0-alpha-10`

So as long as we start off with a leading zero, we are fine, e.g. `1.0-alpha-01`

Of course the next question is how much padding...

Eventually you will reach a point where the amount of padding is too much... enter crazy counting...

Start off with a small amount/no padding and when it looks likely that you will run out, skip versions...

With base 10, you'll probably want to start skipping somewhere around the 5-7 mark, so we'd have

`1.0-alpha-1`, `1.0-alpha-2`, `1.0-alpha-3`, `1.0-alpha-4`
(hmmm we're burning a lot of alphas... looks like we might make 10 or 15, better start crazy counting)
`1.0-alpha-50`, `1.0-alpha-51`, ... `1.0-alpha-99` and we're screwed unless we did another crazy counting... `1.0-alpha-600`! 

If we thought we'd need lots more than 50 builds, we could go really crazy

`1.0-alpha-4` -> `1.0-alpha-500` -> `1.0-alpha-501`, etc

BTW, crazy counting is handy with Maven which uses string based comparison for qualifiers