---
title: "HowTo: CentOS 5, Apache 2.2, Subversion 1.5 with ActiveDirectory Authentication"
date: 2008-11-28T00:00:00Z
---

Here's my step by step:

1. Install CentOS 5.2
2. Configure Network and Proxies as needed
    
    I usually create a login script: 

    `/etc/profile.d/login.sh` as follows:

    ```sh
    function set_proxies() { 
    	 local s 
    	 PROXY_ADDR="http://proxy.example.com:8000/" 
    	 for s in HTTP HTTPS FTP GOPHER NEWSPOST NEWSREPLY\
    	          NEWS NNTP SNEWSPOST SNEWSREPLY SNEWS\
    	          WAIS FINGER CSO; do
    	     export ${s}_PROXY=${PROXY_ADDR}
    	 done
    	 for s in http https ftp; do
    	     export ${s}_proxy=${PROXY_ADDR} 
    	 done
  	}

  	set_proxies
  	```

3. I installed from the DVD, so `yum update` to ensure everything is up-to-date.
4. Get my `mod_authn_sasl` rpm:

     ```sh 
     wget http://www.one-dash.com/blog/mod_authn_sasl-1.0.2-3.i386.rpm
     ```

5. Install it (this should pull down the):

     ```sh
     yum --nogpgcheck localinstall mod_authn_sasl-1.0.2-3.i386.rpm
     ```

6. Get my `sasl-magic-config` script:

     ```sh
     wget http://www.one-dash.com/blog/system-saslauthd-active-directory-config.sh
     dos2unix system-saslauthd-active-directory-config.sh
     ```

7. Run the script:

     ```sh
     sh system-saslauthd-active-directory-config.sh example.com
     ```

8. Change the security level:

     ```sh 
     system-config-securitylevel-tui
     ```

     Set SELinux to Permissive, Customize and enable WWW and Secure WWW on the firewall

9. Create the sasl2 configuration for apache:

     ```sh
     echo "pwcheck_method:saslauthd" > /usr/lib/sasl2/apache-httpd.conf
     ```

10. Now we need to install Subversion 1.5.2:

     ```sh
     wget http://summersoft.fay.ar.us/pub/subversion/1.5.2/rhel-5/i386/subversion-1.5.2-1.i386.rpm
     wget http://summersoft.fay.ar.us/pub/subversion/1.5.2/rhel-5/i386/neon-0.27.2-1.i386.rpm
     wget http://summersoft.fay.ar.us/pub/subversion/1.5.2/rhel-5/i386/mod_dav_svn-1.5.2-1.i386.rpm
     yum install perl-URI
     rpm -i neon-0.27.2-1.i386.rpm 
     rpm -i subversion-1.5.2-1.i386.rpm
     rpm -i mod_dav_svn-1.5.2-1.i386.rpm
     ```

 11. Next modify the apache conf file for our subversion repositories: `/etc/httpd/conf.d/subversion.conf`

     ```
     # Needed to do Subversion Apache server.
     LoadModule dav_svn_module     modules/mod_dav_svn.so

     # Only needed if you decide to do "per-directory" access control.
     #LoadModule authz_svn_module   modules/mod_authz_svn.so

     <Location /svn>
       DAV svn 
       SVNParentPath /var/www/svn 

       <IfModule mod_authn_sasl.c>

         # Limit write permission to list of valid users.    
         <LimitExcept GET PROPFIND OPTIONS REPORT>       
           # Require SSL connection for password protection.       
           # SSLRequireSSL       
           AuthType Basic       
           AuthName "EXAMPLE"       
           AuthBasicProvider sasl       
           AuthSaslPwcheckMethod saslauthd auxprop       
           AuthSaslAppname apache-httpd       
           AuthSaslRealm example       
           Require valid-user    
         </LimitExcept> 

       </IfModule>

     </Location>
     ```

12. Next, create the subversion projects root and restart Apache:

     ```sh
     mkdir /var/www/svn
     chown -R apache.apache /var/www/svn
     service httpd restart
     ```

13. At this point you can now create a test repository:

     ```sh
     svnadmin create /var/www/svn/test
     chown -R apache.apache /var/www/svn/test
     ```

14. Let's test if subversion is working:

     ```sh
     svn info http://localhost/svn/test
     svn mkdir --username myWindowsUsername --message "a test commit" http://localhost/svn/test/trunk
     ```

15. At this point we should have subversion up and running.