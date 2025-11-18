---
title: "Unit testing of annotated classes"
date: 2006-04-11T00:00:00Z
---

I ran into some fun while trying to unit test my annotated entities as some of the annotations were on private fields.  

Rather than create constructors to do the injection for me, or change the access type on the fields, I came up with this little framework that people might be interested in. (Or be able to help improve)  

Temporary home: http://www.stvconsultants.com/community/easygloss/  

Permanent home: hopefully on dev.java.net  

Has anyone any comments?