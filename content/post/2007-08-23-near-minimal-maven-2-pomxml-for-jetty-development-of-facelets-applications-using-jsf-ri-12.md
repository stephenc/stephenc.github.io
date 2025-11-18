---
title: "Near minimal Maven 2 pom.xml for Jetty development of Facelets applications using JSF RI 1.2"
date: 2007-08-23T00:00:00Z
tags: ["Maven"]
---

Spent ages trying to get close to this... gave up looking at what others had done, here is my version from scratch:  

```xml
<?xml version="1.0"?> 
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>....</groupId>
	<artifactId>....</artifactId>
	<version>1.0-SNAPSHOT</version>
	<packaging>war</packaging>
	<name>....</name>
	<build>
        <plugins>
        	<plugin>
        		<groupId>org.apache.maven.plugins</groupId>
        		<artifactId>maven-compiler-plugin</artifactId>
        		<configuration>
        			<source>1.5</source>
        			<target>1.5</target> 
        		</configuration>
        	</plugin>
        	<plugin>
        		<groupId>org.mortbay.jetty</groupId>
        		<artifactId>maven-jetty-plugin</artifactId>
        		<version>6.1H.5-beta</version>
        		<configuration>
        			<contextPath>/</contextPath>
                    <scanIntervalSeconds>10</scanIntervalSeconds>                 
                </configuration>
           </plugin>
       </plugins>
    </build>
    <dependencies>
        <dependency>
            <groupId>javax.faces</groupId>             
            <artifactId>jsf-api</artifactId>             
            <version>1.2-b19</version>         
        </dependency>         
        <dependency>             
            <groupId>javax.faces</groupId>             
            <artifactId>jsf-impl</artifactId>             
            <version>1.2-b19</version>         
        </dependency>         
        <dependency>             
            <groupId>com.sun.facelets</groupId>             
            <artifactId>jsf-facelets</artifactId>             
            <version>1.1.11</version>         
        </dependency>         
        <dependency>             
            <groupId>commons-digester</groupId>             
            <artifactId>commons-digester</artifactId>             
            <version>1.7</version>         
        </dependency>         
        <dependency>             
            <groupId>commons-beanutils</groupId>             
            <artifactId>commons-beanutils</artifactId>             
            <version>1.7.0</version>         
        </dependency>         
        <dependency>             
            <groupId>commons-collections</groupId>             
            <artifactId>commons-collections</artifactId>             
            <version>3.2</version>         
        </dependency>         
        <dependency>             
            <groupId>javax.servlet</groupId>             
            <artifactId>jstl</artifactId>             
            <version>1.1.0</version>         
        </dependency>         
        <dependency>             
            <groupId>javax.servlet</groupId>             
            <artifactId>servlet-api</artifactId>                 
            <version>2.5</version>             
            <scope>provided</scope>         
        </dependency>     
    </dependencies> 
</project>