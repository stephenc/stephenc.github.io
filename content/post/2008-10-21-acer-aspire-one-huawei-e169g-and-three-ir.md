---
title: "Acer Aspire One, Huawei E169G and Three IR"
date: 2008-10-21T00:00:00Z
tags: ["Java", "JavaEE"]
---

One of my co-workers has asked me to post this up.  It's rough and ready, so make of it what you want.

First off, Acer recently pushed an update for better performance with the Huawei USB modems... I'm assuming that you have this update... check if the file `/etc/udev/rules.d/10-Huawei-Datacard.rules` exists.

If that file exists then when you plug in a E169g it will be correctly autodetected without requiring poking about with `usbmodeswitch`... it will bind the three serial ports of the E169G to `/dev/HuaweiMobile-0`, `/dev/HuaweiMobile-1` and `/dev/HuaweiMobile-2`.

OK, so assuming you see these device nodes after plugging in the E169G, the next problem is getting `wvdial` to connect.  Here's the wvdial.conf file I use:

```cfg
[Dialer Defaults]
Init2 = ATZ
Init3 = ATH
Init4 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0
Stupid Mode = 1
Modem Type = USB Modem
ISDN = 0
Phone = *99\#
Modem = /dev/HuaweiMobile-0
Username = username
Password = password
Dial Command = ATDT
Baud = 460800
Init5 = AT+CGDCONT=1,"IP","3ireland.ie"
```

By the way, the username is actually "`username`", and the password is actually "`password`".

That should be enough to get any self-respecting linux freak 90% of the way there.  There was some stuff I had to tweak to get DHCP to populate `resolve.conf` from the pppd connection... and I added the following udev rule as `70-huawei-e169g-dial.rules`

```sh
SUBSYSTEM=="usb" SYSFS{idProduct}=="1001",SYSFS{idVendor}=="12d1",RUN+="/usr/sbin/e169g_dial"
```

And, `/usr/sbin/e169g_dial` is just

```sh
#!/bin/sh
sleep 5
/usr/bin/wvdial 2>&1 > /var/log/wvdial &
```

You might be able to tune down from 5 seconds if you can be bothered... but you need at least some delay