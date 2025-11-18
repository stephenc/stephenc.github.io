---
title: "Keeping up with the latest glassfish builds"
date: 2006-02-01T00:00:00Z
---

Are you keeping up with the latest glassfish builds? Are you running windows 2k or higher? Are you fed up having to manually reinstall the server whenever a new weekly build comes out?

Well I was, so here's a very basic Windows NT command script.

```
@ECHO OFF
REM Change these environment variables to your own config

SET GLASSFISH_DOWNLOADS=c:\java\downloads
SET GLASSFISH_DRIVE=c:
SET GLASSFISH_PARENT_DIR=c:\java

REM Make sure we are in the correct location

%GLASSFISH_DRIVE%
CD %GLASSFISH_PARENT_DIR%

REM Find the latest build that has been downloaded

SET BUILD=aaa
FOR %%i IN (%GLASSFISH_DOWNLOADS%\glassfish-installer-9.0-*.jar) DO IF %%i GTR %BUILD% SET BUILD=%%i

IF A%BUILD%A==AaaaA GOTO no_build

CLS
ECHO .
ECHO .
ECHO Newest build found is:   %BUILD%
IF EXIST glassfish.bld (TYPE glassfish.bld) ELSE (ECHO Current installed build: I don't know)
ECHO .
ECHO .
ECHO .
ECHO [%0] About to remove current installation of Glassfish...
ECHO .
ECHO This will delete any currently deployed applications, so you would want to
ECHO either not care about them or have made a backup already!
ECHO .
ECHO .
ECHO This is your last chance to press Ctrl+C to abort otherwise
ECHO press any other key to continue...
PAUSE >> NUL
ECHO .
ECHO .
ECHO .
ECHO [%0] Stopping domain1...
ECHO .
CALL ASADMIN stop-domain domain1
ECHO .
ECHO .
ECHO .
ECHO [%0] Removing current installation...
ECHO .
RMDIR /S /Q %GLASSFISH_PARENT_DIR%\glassfish
ECHO .
ECHO .
ECHO .
ECHO [%0] Starting installer...
ECHO .JAVA -Xmx256m -jar %BUILD%
ECHO Current installed build: %BUILD% > glassfish.bld
ECHO .
ECHO .
ECHO .
ECHO [%0] Setting up domain1...
ECHO .
CD glassfish
CALL ANT -f setup.xml
ECHO .
ECHO .
ECHO .
ECHO [%0] Starting domain1...
ECHO .
CALL ASADMIN start-domain domain1
ECHO .
ECHO .
ECHO .
ECHO [%0] Glassfish reinstalled!
ECHO .
GOTO end

:no_build
ECHO .
ECHO .
ECHO .
ECHO Cannot find any glassfish builds in %GLASSFISH_DOWNLOADS%
ECHO .

:end
ECHO .
ECHO .
ECHO .
ECHO [%0] I'm done, press a key and I'll be out of here...
ECHO .
PAUSE >> NUL
```

Save it as, e.g. `REINSTALL-GLASSFISH.CMD` and all you need to do is run it every time you download a new build!

Todo:

1. Add some stuff to make it go fetch the latest build from the download page
2. Add some stuff to pull out all the applications from the autodeploy directory before removing the current build and put them back in afterwards.