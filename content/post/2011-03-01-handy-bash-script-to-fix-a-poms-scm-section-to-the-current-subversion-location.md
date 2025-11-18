---
title: "Handy bash script to fix a pom's SCM section to the current Subversion location"
date: 2011-03-01T00:00:00Z
tags: ["Maven", "Shell"]
---

#!/bin/bash

URL="$(svn info | sed -n -e '/^URL:/{s/URL: *//p}')"

ROOT="$(svn info | sed -n -e "/^Repository Root:/{s/Repository Root: *//p}")"

NEW_PATH="${URL#$ROOT}"

OLD_URL="$(sed -n '/< *scm *>/,/< *\/scm *>/p' pom.xml | sed -n '/< *connection *>/,/< *\/ *connection *>/{s/.*connection *> *scm:svn:\([^ <]*\)[ <].*/\1/p}')"

OLD_PATH="${OLD_URL#$ROOT}"

echo "OLD URL: $OLD_URL"

echo "NEW URL: $URL"

echo "ROOT: $ROOT"

echo "OLD PATH: $OLD_PATH"

echo "NEW PATH: $NEW_PATH"

sed -i '/< *scm *>/,/< *\/scm *>/{s/'${OLD_PATH//\//\\\/}'/'${NEW_PATH//\//\\\/}'/}' pom.xml