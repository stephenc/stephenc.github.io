---
title: "Keeping Hudson configuration and data in SVN"
date: 2010-07-08T00:00:00Z
tags: ["Jenkins"]
---

We recently lost our hudson server due to a multiple disk failure in the RAID array storing our hudson configuration. [5 of the 15 disks died]

So I've been looking into a backup script that will allow us to keep a backup of the configuration.  We use Maven for most of our builds, so the released artifacts are in our Maven Repository (which is hosted on two servers each with RAID arrays and using DRBD to mirror between the pair, with an rsync to a NAS in another cabinet and we are trying to get an rsych to an off-site storage going as well).

There seem to be two main options:

1. Use the [Hudson Backup Plugin](http://wiki.hudson-ci.org/display/HUDSON/Backup+Plugin?showComments=false).

2. Backup your Hudson configuration to Source Control.

Option 1 is nice, but you still have to copy off the backup files and find  some safe place to store them. Option 2 sounds better to me as if we loose our source control system, we'll there's nothing to build anyway!

So a quick search of the interwebs revealed [Mike Rooney](http://eng.genius.com/blog/2010/02/02/hudson-in-svn/) has been here before... cool... I have somewhere to start... with a few tweaks I have ended up with the following:

```sh
#!/bin/bash
if [[ ! -d $HUDSON_HOME ]]
then
    echo "Hudson home directory ($HUDSON_HOME) is missing or undefined"
    exit 1
fi

cd $HUDSON_HOME

# Add any new conf files, jobs, users, and content.
svn add -q --parents *.xml jobs/*/config.xml users/*/config.xml userContent/*

# Add the names of plugins so that we know what plugins we have
ls -l plugins > plugins.list
svn add -q -N --parents plugins.list

# Ignore things in the root we don't care about.
echo -e "war\nlog\n*.log\n*.tmp\n*.old\n*.bak\n*.jar\n*.json\nsecret.key\ntools\nshelvedProjects\n.owner\nupdates\nplugins" > myignores
svn ps -q svn:ignore -F myignores . && rm myignores

# Ignore things in jobs/* we don't care about.
echo -e "builds\nlast*\nnext*\n*.txt\n*.log\nworkspace*\ncobertura\njavadoc\nhtmlreports\nncover\ndoclinks" > myignores
svn ps -q svn:ignore -F myignores jobs/* && rm myignores

# Remove anything from SVN that no longer exists in Hudson.
svn st | sed -n -e "s/^\!//p" | xargs -r svn rm

# And finally, check in of course, showing status before and after for logging.
svn st && svn ci --non-interactive --username=hudson-build -m "automated commit of Hudson configuration" && svn st
```

The main changes are that I've updated the root level ignores and I capture a listing of the plugins directory so that you can know exactly what plugins you had installed