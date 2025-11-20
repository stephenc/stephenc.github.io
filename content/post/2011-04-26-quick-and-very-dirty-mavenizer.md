---
title: "Quick and very Dirty Mavenizer"
date: 2011-04-26T00:00:00Z
tags: ["Maven"]
---

The following quick and dirty bash script will take a pom and a jar and fake a maven build based on the source files for that that can be found in the current directory.

Really useful when running `mvn dependency:analyze` on a project you are validating POMs for.

```bash
#!/bin/bash

if [ "A$3" == "A" ]
then
    echo "Syntax: $0 pomfile jarfile dir"
    return
fi

rm -rvf "$3/src"
mkdir -p "$3/src/main/java"
cp -f "$1" "$3/pom.xml"
for name in $(jar -tf "$2" | sed -n -e "/\\$/d;s/\\.class/.java/p")
do
    echo -n "Looking for $name ... "
    loc="$(find . | fgrep $name | head -n 1)"
    if [ "A$loc" == "A" ]
    then
        echo "NOT FOUND"
    else
        echo "$loc"
        mkdir -p "$3/src/main/java/$(dirname $name)"
        cp "$loc" "$3/src/main/java/$name"
    fi
done
```