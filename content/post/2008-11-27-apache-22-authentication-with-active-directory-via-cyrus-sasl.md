---
title: "Apache 2.2 Authentication with Active Directory via Cyrus SASL"
date: 2008-11-27T00:00:00Z
---

Here is my version of the holy grail, i.e.

> Authentication for Apache HTTPD against Active Directory.

This is not the only way to skin this cat, for example you could also use [Sander Marechal's technique](http://www.jejik.com/articles/2007/06/apache_and_subversion_authentication_with_microsoft_active_directory/) (which uses [mod_authnz_ldap](http://httpd.apache.org/docs/2.2/mod/mod_authnz_ldap.html)). However, my problem with Sander's technique is that you need to have an account in Active Directory which you will use to bind to the LDAP server.  That means that the accound password has to be stored in a plain-text file on the Apache server, and if the password expires everything breaks until you go fix the password.

I want as near to zero maintenance as possible, running on CentOS 5.2 with minimal custom work - so that I don't have to maintain it when it does break.

I have previously configured Kerberos to authenicate against Active Directory, so my first attempt was with [mod_auth_kerb](http://modauthkerb.sourceforge.net/).  That worked... but very slowly... trying to an empty access Subversion repository took over 2 minutes.  The problem being that successful authentication was not being cached.

Then I tried using [mod_perl](http://perl.apache.org/) and the [Authen::Simple::ActiveDirectory](http://search.cpan.org/%7Echansen/Authen-Simple-LDAP-0.2/lib/Authen/Simple/ActiveDirectory.pm) reasoning that I could always hack caching once in perl... but getting that lot installed on a CentOS 5.2 from RPMs was an exercise in tears.

So, anyway, I found out that [Cyrus SASL](http://asg.web.cmu.edu/sasl/sasl-library.html) supports two modes of LDAP authentication:

> The bind method uses the LDAP bind facility to verify the password.  The bind method is not available when ldap_use_sasl is turned on.  In that case saslauthd will use fastbind.
>
> 'bind' is the default auth method. When ldap_use_sasl is enabled, 'fastbind' is the default.
>
> The custom method uses userPassword attribute to verify the password. Suppored hashes: crypt, md5, smd5, sha and ssha.  Cleartext is supported as well.
> 
> The fastbind method (when 'ldap_use_sasl: no') does away with the search and an extra anonymous bind in auth_bind, but makes two assumptions:  
> 1. Expanding the ldap_filter expression gives the user's fully-qualified DN  
> 2. There is no cost to staying bound as a named user

So bind is pretty much the same technique as that used by [mod_authnz_ldap](http://httpd.apache.org/docs/2.2/mod/mod_authnz_ldap.html), and (as ActiveDirectory does not support - at my company at least - anonymous bind) is ruled out of the running.

"fastbind" sounds exactly like what I want... ok and saslauthd can be configured to cache authentication, so none of the performance hit of [mod_auth_kerb](http://modauthkerb.sourceforge.net/).  All we need is a way to tie this into Apache.

So, enter [mod_authn_sasl](http://mod-authn-sasl.sourceforge.net/) which does just that.

First, we need to create an RPM, so I did a quick

```sh 
sudo yum install httpd-devel rpmbuild mock
sudo
echo "%_topdir %(echo $HOME)/rpmbuild" > ~/.rpmmacros
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
```

I added my account to the `mock` group, logged out and in again for the group membership to be recognised and I was ready to go.  This was my first experience playing with [mock](http://fedoraproject.org/wiki/Projects/Mock), but it was lovely, especially as CentOS has its own version.

I pre-primed my mock environments for `i386` and `x86_64` as I need RPMs for both of these:

```sh
mock -r centos-5-i386 init
mock -r centos-5-x86_64 init
```

Then I downloaded [mod_authn_sasl-1.0.2.tar.bz2](http://superb-east.dl.sourceforge.net/sourceforge/mod-authn-sasl/mod_authn_sasl-1.0.2.tar.bz2) and started writing my spec file.

You can download the RPC spec: [mod_authn_sasl.spec](http://www.one-dash.com/blog/mod_authn_sasl.spec) and the apache config file: [mod_authn_sasl.conf](http://www.one-dash.com/blog/mod_authn_sasl.conf).

I put [mod_authn_sasl-1.0.2.tar.bz2](http://superb-east.dl.sourceforge.net/sourceforge/mod-authn-sasl/mod_authn_sasl-1.0.2.tar.bz2) and [mod_authn_sasl.conf](http://www.one-dash.com/blog/mod_authn_sasl.conf) in the `~/rpmbuild/SOURCES` and then running

```sh
rpmbuild -ba mod_authn_sasl.spec
```

produced [my source RPM](http://www.one-dash.com/blog/mod_authn_sasl-1.0.2-4.src.rpm), then I used mock to create the two binary RPMs that I needed:

```sh
mock -r centos-5-i386 ~/rpmbuild/SRPMS/mod_authn_sasl-1.0.2-4.src.rpm
mock -r centos-5-x86_64 ~/rpmbuild/SRPMS/mod_authn_sasl-1.0.2-4.src.rpm
```

The rpms built from the mock environments end up in `/var/lib/mock/centos-5-i386/result`  and `/var/lib/mock/centos-5-x86_64/result`. If you want to be lazy and trust my binaries here they are:

* [mod_authn_sasl-1.0.2-4.i386.rpm](http://www.one-dash.com/blog/mod_authn_sasl-1.0.2-4.i386.rpm)
* [mod_authn_sasl-1.0.2-4.x86_64.rpm](http://www.one-dash.com/blog/mod_authn_sasl-1.0.2-4.x86_64.rpm)

Now all we need to do is configure everything.

've written [this shell script](http://www.one-dash.com/blog/system-saslauthd-active-directory-config.sh) to simplify configuring saslauthd for most good deployments of Active Directory, i.e. where there are `SRV` records for the domain in your DNS server.  You need to run it as root.  It looks up the `SRV` records for the domain name you provide, and creates `/etc/saslauthd.conf` from them, assuming that the Active Directory domain name is the first word of your DNS name converted to uppercase.  So for example, if your Active Directory is set up correctly, and you can login to windows as either `EXAMPLE\joebloggs` or `jbloggs@example.foo.com` then you would run

```sh
sh system-saslauthd-active-directory-config.sh example.foo.com
```

And that *should* setup `saslauthd` for you.  You can test this using the `testsaslauthd` program.

Then all you need to do is secure the appropriate locations in apache, e.g. by adding the following to your VirtualHost configuration:

```
<Location /private>
  AuthSaslPwcheckMethod saslauthd
  AuthSaslAppname httpd
  AuthSaslRealm example
  AuthType basic
  AuthBasicProvider sasl
  AuthBasicAuthoritative On
  AuthName "sasl@example.com"
  require valid-user
</Location>
```

And define the SASL application provider for the `AuthSaslAppname` you specified, e.g. for the above configuration you need to create `/usr/lib/sasl2/httpd.conf` with the contents:

```
pwcheck_method:saslauthd
```

That's it.  You should be done.

**Updated Friday 28th November 2008:** I noticed that the spec file I had provided did not have the correct `Requires` and `BuildRequires`. I have fixed this and now I have posted updated rpms (these are `1.0.2-4`) with the correct requires to help with a minimal install