---
title: "My magic Maven and ANT version selection bash functions (for the Mac)"
date: 2011-03-01T00:00:00Z
tags: ["Shell"]
---

OK, so a while back I posted my bash script for selecting the maven version to use for the current session http://s.apache.org/FQ2

Now that I have a Mac for my full time development machine, I thought I would share my version of these functions for Mac users:

usemvn ()

{

if [ -z "$1" -o ! -x "/usr/share/java/maven-$1/bin/mvn" ]

then

local prefix="Syntax: usemvn "

for i in /usr/share/java/maven-*

do

if [ -x "$i/bin/mvn" ]; then

echo -n "$prefix$(basename $i | sed 's/^maven-//')"

prefix=" | "

fi

done

echo ""

else

if [ -z "$MAVEN_HOME" ]

then

export PATH=/usr/share/java/maven-$1/bin:$PATH

else

export PATH=$(echo $PATH|sed -e "s:$MAVEN_HOME/bin:/usr/share/java/maven-$1/bin:g")

fi

export MAVEN_HOME=/usr/share/java/maven-$1

fi

}

useant ()

{

if [ -z "$1" -o ! -x "/usr/share/java/ant-$1/bin/ant" ]

then

local prefix="Syntax: useant "

for i in /usr/share/java/ant-*

do

if [ -x "$i/bin/ant" ]; then

echo -n "$prefix$(basename $i | sed 's/^ant-//')"

prefix=" | "

fi

done

echo ""

else

if [ -z "$ANT_HOME" ]

then

export PATH=/usr/share/java/ant-$1/bin:$PATH

else

export PATH=$(echo $PATH|sed -e "s:$ANT_HOME/bin:/usr/share/java/ant-$1/bin:g")

fi

export ANT_HOME=/usr/share/java/ant-$1

fi

}

Simply add the above into your ~/.bash_profile and you can use them from any bash shell.

For example:

[stephenc@stephenc ~]$ mvn -version

Apache Maven 3.0.2 (r1056850; 2011-01-09 00:58:10+0000)

Java version: 1.6.0_24, vendor: Apple Inc.

Java home: /System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home

Default locale: en_US, platform encoding: MacRoman

OS name: "mac os x", version: "10.6.6", arch: "x86_64", family: "mac"

[stephenc@stephenc ~]$ usemvn

Syntax: usemvn 2.2.0 | 2.2.1 | 3.0.2

[stephenc@stephenc ~]$ usemvn 2.2.1

[stephenc@stephenc ~]$ mvn -version

Apache Maven 2.2.1 (r801777; 2009-08-06 20:16:01+0100)

Java version: 1.6.0_24

Java home: /System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home

Default locale: en_US, platform encoding: MacRoman

OS name: "mac os x" version: "10.6.6" arch: "x86_64" Family: "mac"

[stephenc@stephenc ~]$

The joy of these as bash functions is that they only affect the current session. So I can have one Terminal tab running Maven 2.2.1 and another running Maven 3.0.2

Other tricks that people use by re-pointing the symlink are global and have global effect which makes hopping between tasks or testing different versions of Maven a whole lot harder.