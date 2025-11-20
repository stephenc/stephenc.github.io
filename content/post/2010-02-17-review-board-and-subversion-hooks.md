---
title: "Review Board and Subversion Hooks"
date: 2010-02-17T00:00:00Z
---

[Review Board](http://www.reviewboard.org/) is quite nice... it has a handy program for posting reviews ([postreview](http://www.reviewboard.org/docs/manual/1.0/users/tools/post-review/))... and you can integrate this into your [subversion](http://subversion.apache.org/) hook scripts quite nicely...

But what if you want to automate submitting reviews on only parts of your code base...

What I want is to be able to set a property on a folder and then any time a file is changed in that folder or it's children, then a review will automatically be scheduled...

So I wrote the following C/C++ helper (because we would potentially be forking a lot of svnlook processes) which checks to see if a property is set on any of the changed paths or the changed path parents.

```c
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

/**
 * Returns a stream for the output of dirs-changed from svnlook.
 */
FILE *svnlook_dirs_changed(char *svnlook, char *repo, char *rev) {
  char *cmd;

  cmd = (char *) malloc(strlen(svnlook) + strlen(" dirs-changed ") + strlen(repo) + strlen(" -r ") + strlen(rev) + 1);
  strcpy(cmd, svnlook);
  strcat(cmd, " dirs-changed ");
  strcat(cmd, repo);
  strcat(cmd, " -r ");
  strcat(cmd, rev);
  return (FILE *) popen(cmd, "r");
}

/**
 * Uses svnlook to check and see if the specified property is set on the specified path in the specified repository.
 */
int svnlook_is_prop_set(char *svnlook, char *repopath, char *propname, char *path) {
  int status;
  pid_t pid;
  pid = fork();
  if (pid == 0) {
    fclose(stdin);
    FILE *fp = fopen("/dev/null", "w+");
    if (fileno(fp) != STDIN_FILENO) {
      _exit(EXIT_FAILURE);
    }
    if (dup2(STDIN_FILENO, STDOUT_FILENO) == -1) {
      _exit(EXIT_FAILURE);
    }
    if (dup2(STDIN_FILENO, STDERR_FILENO) == -1) {
      _exit(EXIT_FAILURE);
    }
    execl(svnlook, svnlook, "pg", repopath, propname, path, NULL);
    printf("exit failure\n");
    _exit(EXIT_FAILURE);
  } else if (pid < 0) {
    status = -1;
  } else {
    if (waitpid(pid, & status, 0) != pid) {
      status = -1;
    }
  }
  return status;
}

/**
 * Checks to see if any of the directories from the stream have the specified property set.
 */
int check_svn_dirs(FILE *fdirschanged, char *svnlook, char *repopath, char *revnum, char *propname, int showallpaths) {
  char line[1024];
  int rv = 0;;
  while (fgets(line, sizeof line, fdirschanged)) {
    for (unsigned int i = 0; i < sizeof line; i++) {
      if (line[i] == '\n') {
        line[i] = 0;
        for (int j = i; j > 0; j--) {
          if (line[j] == '/') {
            line[j] = 0;
            if (0 == svnlook_is_prop_set(svnlook, repopath, propname, line)) {
              printf("%s/\n", line);
              if (!showallpaths) {
                return 1;
              } else {
                rv = 1;
              }
            }
          }
        }
        line[0] = 0;
        if (0 == svnlook_is_prop_set(svnlook, repopath, propname, line)) {
          printf("/\n");
          if (!showallpaths) {
            return 1;
          } else {
            rv = 1;
          }
        }
        break;
      } // else it's a really long path and I'm refusing to check it!
    }
  }
  return rv;
}

int main(int argc, char **argv) {
  FILE *fpipe;

  char *svnlook = "/usr/bin/svnlook";
  char *repopath = "..";
  char *revnum = NULL;
  char *propname = NULL;
  int showallpaths = 0;

  int index = 1;
  int help = 0;
  while (index < argc) {
    if (strcmp("--svn-look", argv[index]) == 0) {
      index++;
      if (index < argc) {
        svnlook = argv[index];
      } else {
        help = 1;
        break;
      }
    } else if (strcmp("-r", argv[index]) == 0) {
      index++;
      if (index < argc) {
        revnum = argv[index];
      } else {
        help = 1;
        break;
      }
    } else if (strcmp("--repo", argv[index]) == 0) {
      index++;
      if (index < argc) {
        repopath = argv[index];
      } else {
        help = 1;
        break;
      }
    } else if (strcmp("--property", argv[index]) == 0) {
      index++;
      if (index < argc) {
        propname = argv[index];
      } else {
        help = 1;
        break;
      }
    } else if (strcmp("--show-all-paths", argv[index]) == 0) {
      showallpaths = 1;
    } else if (strcmp("--help", argv[index]) == 0 || strcmp("-h", argv[index]) == 0 || strcmp("-?", argv[index]) == 0) {
      help = 1;
      break;
    } else {
      help = 1;
      break;
    }
    index++;
  }
  
  if (help || svnlook == NULL || repopath == NULL || revnum == NULL || propname == NULL) {
    printf("Syntax: %s options\n", argv[0]);
    printf("Options:\n");
    printf("    --svn-look PATH     Specify an alternative svnlook binary location (default /usr/bin/svnlook)\n");
    printf("    --repo PATH         Specify the repository to work against (required)\n");
    printf("    -r REVNUM           Specify the revision to process (required)\n");
    printf("    -property NAME      Specify the property to check (required)\n");
    printf("    --show-all-paths    Shows all the changed paths with the property rather than just the first (optional)\n");
    return 2;
  }
  
  int rv = 0;
  fpipe = svnlook_dirs_changed(svnlook, repopath, revnum);
  if (fpipe) {
    rv = check_svn_dirs(fpipe, svnlook, repopath, revnum, propname, showallpaths);
    pclose(fpipe);
  }
  
  return rv;
}
```

Now I should warn you that it's a wee while since I wrote C/C++, so apologies if the above is not perfect... it works for me.

Next I use a `post-commit.sh` script to check for my property:

```sh
#!/bin/bash
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

path=$(/usr/bin/svnlook props --repo "$1" -r $2 --property reviewboard:autoreview)
if [ $? == 1 ]; then
    if [ $(svnlook changed "$1" -r $2 | sed -e "/^_.*/d;" | wc -l) -eq 0 ] ; then
        # Commit does not contain changed files, only changed properties
        exit 0
    fi
    people=$(for p in $(/usr/bin/svnlook props --repo "$1" -r $2 --property reviewboard:autoreview --show-all-paths); \
            do /usr/bin/svnlook pg "$1" reviewboard:autoreview "$p"; echo ""; done \
            | sed -e 's/[, \t]/\n/g;' | sort -u | tr '\n' ',' | sed -e "s/,$//;")
    post-review --server=... --username=... --password=... --submit-as=$(/usr/bin/svnlook author "$1" "$2") \
        --repository-url=... --revision-range=$(($2-1)):$2 "--description=$(/usr/bin/svnlook log "$1" -r "$2")" \
        "--summary=Commit r$2" "--target-people=$people" --publish
fi
exit 0
```

And now, as if by magic, all I need to do is set the property `reviewboard:autoreview` to the list of reviewboard usernames to be reviewers and then any time there is a commit on the folder with the property set, a review is automagically scheduled.

Lovely...

Now all I need to do is tone down how often reviewboard sends emails!