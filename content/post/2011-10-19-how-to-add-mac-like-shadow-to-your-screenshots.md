---
title: "How to add Mac-like shadow to your screenshots"
date: 2011-10-19T00:00:00Z
---

Cmd+Shift+4 followed by Space is a lovely way to get a screen shot of a window on an Apple Mac...

In fact here is one such screenshot:

![](/images/post/2011-10-19-screenshot.png)

Notice the nice shadow effect around the screenshot? Ever wanted to add that shadow effect to your non-mac screenshots?

ImageMagick is your friend

```sh
convert NoShadowScreenshot.png \( +clone -background black -shadow 80x20+0+15 \) \
  +swap -background transparent -layers merge +repage WithShadowScreenshot.png
```

There you are, nice equivalent shadow added.

Oh and if you hate the Mac's shadow:

To remove from existing screenshots?

ImageMagick is your friend again

```sh
convert WithShadowScreenshot.png -crop +40+25 -crop -40-55 WithoutShadowScreenshot.png
```

If you get sick of doing that all the time, you can just disable it.

Here’s the command. Just paste this line into your Terminal, and press return.

```sh
defaults write com.apple.screencapture disable-shadow -bool true
```

Then, you’ll need to restart the System’s UI Server, which is the component of the operating system responsible for doing things like taking screenshots and drawing drop shadows. To accomplish this, simply paste this line into the Terminal.

```sh
killall SystemUIServer
```