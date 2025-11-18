---
title: "Quick and dirty remove -SNAPSHOTS from your local maven repository"
date: 2010-07-01T00:00:00Z
tags: ["Maven", "Shell"]
---

Works on *nixfind ~/.m2/repository -type d -name \*-SNAPSHOT -exec rm -rvf {} \;By searching for the directories we should catch the -YYYYMMDD.HHMMSS format of snapshots also