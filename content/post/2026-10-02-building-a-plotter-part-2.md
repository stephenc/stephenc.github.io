---
title: "Building a plotter (part 2)"
date: 2026-10-02T14:00:00Z
tags: ["hardware"]
categories: ["Hardware"]
series: ["Hardware Hacking"]
images: [
	"/images/post/2026-10-02-building-a-plotter-part-2-second-design.png", 
	"/images/post/2026-10-02-building-a-plotter-part-2-first-print.jpeg",
	"/images/post/2026-10-02-building-a-plotter-part-2-xy-plotter-bottom-problem.jpg",
	"/images/post/2026-10-02-building-a-plotter-part-2-codex-finds-the-problem.png",
	"/images/post/2026-10-02-building-a-plotter-part-2-second-print.png",
	"/images/post/2026-10-02-building-a-plotter-part-2-third-print.png",
]
---

# Building a plotter (part 2)

So the Makerbase MKS DLC32 arrived. 
My challenge was how to mount it onto the frame and keep all the wires hidden.

Normally I would fire up OpenSCAD and get my calipers out and risk the wrath of my family while I disappear for 3 days designing the enclosure to print.

![The second design](/images/post/2026-10-02-building-a-plotter-part-2-second-design.png)

This time I said, let's see what the LLMs can do.

So I loaded up a directory with:

* The Makerbase user guide (which includes sizing diagrams)
* The Draw bot assembly instructions
* Some photos of the join point with a ruler included.

I then asked Codex to design the enclosure...

The first design was ugly... sadly I didn't save it.
The main issue was that it didn't think to put the display *above* the PCB.
Instead there was one half of the box just for the display (with empty box underneath) and the other half of the box for the PCB (with empty box above).

So one steer later and we had a reasonable design... just with lots of holes... but it was perfectly functional.

*Spoiler:* For Part 3 I had given Codex a camera so it can see.

I told Codex there was something wrong with the design, but didn't say what specifically, so it took a picture and immediately diagnosed the issue.

Here's What the first version looks like:

![First print](/images/post/2026-10-02-building-a-plotter-part-2-first-print.jpeg)

Here's the photo Codex took:

![The photo of the problem](/images/post/2026-10-02-building-a-plotter-part-2-xy-plotter-bottom-problem.jpg)

Can you see what is wrong?

![Codex finds the problem](/images/post/2026-10-02-building-a-plotter-part-2-codex-finds-the-problem.png)

After some redirects to bevel the display mount and confusion on which side to add the missing holes on, both of which I caught in the 3D viewer, we got this mostly fine print...

![Second print](/images/post/2026-10-02-building-a-plotter-part-2-second-print.png)

I say mostly fine as some of the offsets were wrong and needed tweaking...

So now we end up at the third and final print

![Third print](/images/post/2026-10-02-building-a-plotter-part-2-third-print.png)

All in all I am really happy with this print.

Part 3 will be all about getting the touch screen working and configuring the plotter to actually work!