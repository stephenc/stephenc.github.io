---
title: "Note to self: Updated usejava BASH function for MacOSX"
date: 2013-02-01T00:00:00Z
tags: ["Shell"]
---

For use when you have multiple JVM providers (Apple & Oracle), you want to be able to switch between JDKs for each CLI

```sh
usejava ()
{
    local sel=$1.jdk
    if [ -x "/Library/Java/JavaVirtualMachines/jdk$sel/Contents/Home/bin/java" -a ! -x "/Library/Java/JavaVirtualMachines/$1/Contents/Home/bin/java" ]
    then
        sel=jdk$sel
    fi
    local base=/Library/Java/JavaVirtualMachines
    if [ -x "/System/Library/Java/JavaVirtualMachines/$sel/Contents/Home/bin/java" ]
    then
        base=/System/Library/Java/JavaVirtualMachines
    fi
    if [ -z "$1" -o ! -x "$base/$sel/Contents/Home/bin/java" ]
    then
        local prefix="Syntax: usejava "
        for i in /Library/Java/JavaVirtualMachines/* /System/Library/Java/JavaVirtualMachines/*
        do
            if [ -x "$i/Contents/Home/bin/java" ]
            then
                /bin/echo -n "$prefix$(basename $i | sed -e "s/^jdk//;s/\.jdk$//;")"
                prefix=" | "
            fi
        done
        /bin/echo ""
    else
        if [ -z "$JAVA_HOME" ]
        then
            export PATH=$base/$sel/Contents/Home/bin:$PATH
        else
            export PATH=$(echo $PATH|sed -e "s:$JAVA_HOME/bin:$base/$sel/Contents/Home/bin:g")
        fi
        export JAVA_HOME=$base/$sel/Contents/Home
        echo -n -e "\033]0;$(java -version 2>&1 | sed -e "s/.*\"\(.*\)\".*/Java \1/;q")\007"
    fi
}
```

There is additional fun to be had, given that most Java based launchers that try to fix `JAVA_HOME` when not set will guess the Apple JVM path… so the following Java program can help

```java
public class FixJavaHome {
    public static void main(String[] args) {
        String javaHome = System.getProperty("java.home");
        if (javaHome.endsWith("/jre")) {
            javaHome = javaHome.substring(0,javaHome.length() - "/jre".length());
        }
        System.out.println("export JAVA_HOME=\""+javaHome+'\"');
    }
}
```

Install like so

```sh
mkdir -p ~/bin/FixJavaHome && cd ~/bin/FixJavaHome && cat > FixJavaHome.java <<EOF
public class FixJavaHome {
    public static void main(String[] args) {
        String javaHome = System.getProperty("java.home");
        if (javaHome.endsWith("/jre")) {
            javaHome = javaHome.substring(0,javaHome.length() - "/jre".length());
        }
        System.out.println("export JAVA_HOME=\""+javaHome+'\"');
    }
}

EOF

javac FixJavaHome.java

cd -
```

If you add the following to your `~/.bash_profile`

```sh
eval $(java -cp ~/bin/FixJavaHome/ FixJavaHome)

echo -n -e "\033]0;$(java -version 2>&1 | sed -e "s/.*\"\(.*\)\".*/Java \1/;q")\007"
```

Then your `JAVA_HOME` should be set up from the start, as well as your Terminal window title