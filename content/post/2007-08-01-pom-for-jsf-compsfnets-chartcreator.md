---
title: "pom for jsf-comp.sf.net's chartcreator"
date: 2007-08-23T01:00:00Z
tags: ["Maven"]
---

Not perfect, but enough to get you going.  

To build with this pom: 

* You will need to grab the sources from http://downloads.sourceforge.net/jsf-comp/chartcreator-1.2.0.source.zip and extract into `src/main/java`

* You will need to grab the `jar` and extract the three files in the `META-INF` (not `MANIFEST.MF`) into `src/main/resources/META-INF`  

Then you can install away to your hearts content.  

```xml
<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>net.sf.jsf-comp</groupId>
  <artifactId>chartcreator</artifactId>
  <version>1.2.0-mavenized</version>
  <packaging>jar</packaging>
  <name>ChartCreator</name>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <configuration>
          <source>1.4</source>
          <target>1.4</target>
        </configuration>
      </plugin>
    </plugins>
  </build>
  <dependencies>
    <dependency>
      <groupId>javax.faces</groupId>
      <artifactId>jsf-api</artifactId>
      <version>1.2-b19</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>javax.faces</groupId>
      <artifactId>jsf-impl</artifactId>
      <version>1.2-b19</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>com.sun.facelets</groupId>
      <artifactId>jsf-facelets</artifactId>
      <version>1.1.11</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>javax.servlet.jsp</groupId>
      <artifactId>jsp-api</artifactId>
      <version>2.1</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>javax.portlet</groupId>
      <artifactId>portlet-api</artifactId>
      <version>1.0</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>servlet-api</artifactId>
      <version>2.5</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>jfree</groupId>
      <artifactId>jfreechart</artifactId>
      <version>1.0.5</version>
    </dependency>
  </dependencies>
</project>
```