# Welcome to the NginX!
## What is NginX?

Nginx, pronounced like “engine-ex”, is an open-source web server that, since its initial success as a web server, is now also used as a reverse proxy, HTTP cache, and load balancer.

Some high-profile companies using Nginx include Autodesk, Atlassian, Intuit, T-Mobile, GitLab, DuckDuckGo, Microsoft, IBM, Google, Adobe, Salesforce, VMWare, Xerox, LinkedIn, Cisco, Facebook, Target, Citrix Systems, Twitter, Apple, Intel, and many more (source).

Nginx was originally created by Igor Sysoev, with its first public release in October 2004. Igor initially conceived the software as an answer to the C10k problem, which is a problem regarding the performance issue of handling 10,000 concurrent connections.

Because its roots are in performance optimization under scale, Nginx often outperforms other popular web servers in benchmark tests, especially in situations with static content and/or high concurrent requests, which is why Kinsta uses Nginx to power its hosting.

![](https://minas3.s3.ir-thr-at1.arvanstorage.com/Nginx_logo.svg.png?AWSAccessKeyId=2c76505f-bddc-4f97-9bca-9434b780e56c&Signature=8IvWQMXApLNWV6vmBDoa0wOsO6E%3D&Expires=1646206217)


***
# Install NginX
## Installation
### Prerequisites
Before you begin this guide, you should have a regular, non-root user with sudo privileges configured on your server. You can learn how to configure a regular user account by following our Initial server setup guide for Ubuntu 20.04.

##  Installing Nginx
Because Nginx is available in Ubuntu’s default repositories, it is possible to install it from these repositories using the apt packaging system.

```
sudo apt update
sudo apt upgrade
sudo apt install nginx
```

##  Checking your Web Server
At the end of the installation process, Ubuntu 20.04 starts Nginx. The web server should already be up and running.
```
systemctl status nginx
```
```
Output:
● nginx.service - A high performance web server and a reverse proxy server
Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
Active: active (running) since Fri 2020-04-20 16:08:19 UTC; 3 days ago
Docs: man:nginx(8)
Main PID: 2369 (nginx)
Tasks: 2 (limit: 1153)
Memory: 3.5M
CGroup: /system.slice/nginx.service
        ├─2369 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
        └─2380 nginx: worker process
```
You can access the default Nginx landing page to confirm that the software is running properly by navigating to your server’s IP address. If you do not know your server’s IP address, you can find it by using the icanhazip.com tool, which will give you your public IP address as received from another location on the internet:

```
curl your_server_ip
```
When you have your server’s IP address, enter it into your browser’s address bar:
```
http://your_server_ip
```
![](https://minas3.s3.ir-thr-at1.arvanstorage.com/default_page.png?AWSAccessKeyId=2c76505f-bddc-4f97-9bca-9434b780e56c&Signature=qDsqy1tsd92G2Im6T93hTfYOGVY%3D&Expires=1646206349)


## Managing the Nginx Process
Now that you have your web server up and running, let’s review some basic management commands.
To stop your web server, type:
```
sudo systemctl stop nginx
sudo systemctl start nginx
sudo systemctl restart nginx
sudo systemctl reload nginx
sudo systemctl disable nginx
sudo systemctl enable nginx
```
***
# Configuration
## nginx.conf

Now that Nginx has successfully been installed it’s time to perform some basic configuration. Out-of-the-box Nginx is pretty well optimized, but there are a few basic adjustments to make. However, before opening the configuration file, you need to determine your server’s CPU core count and the open file limit.

Enter the following command to get the number of CPU cores your server has available. Take note of the number as we’ll use it in a minute:

```
grep processor /proc/cpuinfo | wc -l
```
Run the following to get your server’s open file limit and take note, we’ll need it as well:
```
ulimit -n
```
Next, open the Nginx configuration file, which can be found at /etc/nginx/nginx.conf:
```
sudo nano /etc/nginx/nginx.conf
```
I’m not going to list every configuration directive but I am going to briefly mention those that you should change:
```
worker_processes 1;
worker_connections 1024;
multi_accept on;
keepalive_timeout 65;
server_tokens off;
client_max_body_size 64;
gzip_proxied any;
gzip_comp_level 5;
```
That’s the basic Nginx configuration dealt with. Hit CTRL + X followed by Y to save the changes.
***
# self signed SSL certificate
## SSL/TLS
The SSL/TLS protocol is about security and authentication. It allows for the encryption of data communications over open networks, safeguarding against tampering and interception by malicious actors. In addition, the use of SSL certificates authenticates communicating parties, creating a trust environment. Security and authentication are the building blocks of successful enterprises in the digital world.
# Self-Signed Certificate?
Another strategy is to issue self-signed SSL certificates. A self-signed certificate is one that is not signed by a CA at all – neither private nor public. In this case, the certificate is signed with its own private key, instead of requesting it from a public or a private CA.

Self-signed certificates offer some advantages when used in internal networks and software development phases, however, they can also create several risks without proper visibility and control
***
# Creating an OpenSSL configuration
Let's start with this important section. We need to create a configuration file for OpenSSL by running the command in the terminal:
```
nano /tmp/openssl.cnf
```
Copy and paste the following prepared configuration into a new file, where DNS.1 is the name of your server (specify DNS.2 if you need support for subdomains):
```
[req]
default_bits = 2048
default_keyfile = privkey.pem
distinguished_name = req_distinguished_name
x509_extensions = v3_ca # The extensions to add to the self-signed cert
[req_distinguished_name]
countryName = Country Name (2 letter code)
countryName_default = US
stateOrProvinceName = State or Province Name (full name)
stateOrProvinceName_default = New York
localityName = Locality Name (eg, city)
localityName_default = Rochester
organizationName = Organization Name (eg, company)
organizationName_default = Localhost CA
organizationalUnitName = Organizational Unit Name (eg, section)
organizationalUnitName_default = Development
commonName = Common Name (e.g. server FQDN or YOUR name)
commonName_default = localhost
commonName_max = 64
[v3_ca]
subjectAltName = @alt_names
[alt_names]
DNS.1 = localhost
# Support subdomains
#DNS.2 = *.domain.local
```
# Generate private key and certificate signing request
A private key and certificate signing request are required to create an SSL certificate. These can be generated with a few simple commands.

When the openssl req command asks for a “challenge password”, just press return, leaving the password empty. This password is used by Certificate Authorities to authenticate the certificate owner when they want to revoke their certificate.
```
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/ssl/private/localhost.key -out /etc/ssl/certs/localhost.crt -config /tmp/openssl.cnf
```
# Configuring Nginx to use SSL
Let's enable SSL in the Nginx server configuration. We will specify listening on port 443 (HTTPS) and the path to the certificate and private key files. Edit the server configuration file /etc/nginx/sites-available/default:
```
ssl_certificate /etc/ssl/certs/localhost.crt;
ssl_certificate_key /etc/ssl/private/localhost.key;
```
For more information:
* [self-signed SSL certificate](https://develike.com/en/articles/adding-a-trusted-self-signed-ssl-certificate-to-nginx-on-debian-ubuntu)

# ignore invalid and self signed ssl connection errors with curl
You can add insecure option to your $HOME/.curlrc file:
```
vi $HOME/.curlrc
```
Append the following:
```
insecure
```
Let's add the generated SSL certificate to the database using the certutil utility by running the command in the terminal:
```
certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n localhost.crt -i /etc/ssl/certs/localhost.crt
```
***
# Setting Up Server Blocks
## Server Blocks
When using the Nginx web server, server blocks (similar to virtual hosts in Apache) can be used to encapsulate configuration details and host more than one domain from a single server. We will set up a domain called _your_domain_, but you should replace this with your own domain name.

## serving static contents
Nginx on Ubuntu 20.04 has one server block enabled by default that is configured to serve documents out of a directory at /var/www/html. While this works well for a single site, it can become unwieldy if you are hosting multiple sites. Instead of modifying /var/www/html, let’s create a directory structure within /var/www for our your_domain site, leaving /var/www/html in place as the default directory to be served if a client request doesn’t match any other sites.

Create the directory for your_domain as follows, using the -p flag to create any necessary parent directories:
```
sudo mkdir -p /var/www/your_domain/html
sudo chmod -R 755 /var/www/your_domain
```
Next, create a sample index.html page using nano or your favorite editor:

`nano /var/www/your_domain/html/index.html`

Inside, add the following sample HTML:
```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to Google!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to Google!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```
In order for Nginx to serve this content, it’s necessary to create a server block with the correct directives. Instead of modifying the default configuration file directly, let’s make a new one at /etc/nginx/sites-available/your_domain:

`sudo nano /etc/nginx/sites-available/your_domain`
Paste in the following configuration block, which is similar to the default, but updated for our new directory and domain name:

```
# Default server configuration
server {
        listen 80;
        listen [::]:80;
        server_name google.com www.google.com;
        return 301 https://$host$request_uri;
}
        # SSL configuration
server {
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name google.com www.google.com;

        # Self signed certifacte
        ssl_certificate /etc/ssl/certs/google-selfsigned.crt;
        ssl_certificate_key /etc/ssl/private/google-selfsigned.key;
        # include snippets/snakeoil.conf;
        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index01.html index.htm index.nginx-debian.html;


        location / {
                # First attempt to serve request as file,
                try_files $uri $uri/ =404;
        }
```
## Sites-available and Sites-enables

Next, let’s enable the file by creating a link from it to the sites-enabled directory, which Nginx reads from during startup:

* `sudo ln -s /etc/nginx/sites-available/your_domain /etc/nginx/sites-enabled/`

> Note: Nginx uses a common practice called symbolic links, or symlinks, to track which of your server blocks are enabled. Creating a symlink is like creating a shortcut on disk, so that you could later delete the shortcut from the sites-enabled directory while keeping the server block in sites-available if you wanted to enable it.

## Test NginX

Next, test to make sure that there are no syntax errors in any of your Nginx files:

* `sudo nginx -t`

If there aren’t any problems, restart Nginx to enable your changes:
* `sudo systemctl restart nginx`

***
# Wordpress (CMS)
## Introduction
WordPress, one of the most popular content management systems (CMS) on the internet currently, allows users to set up flexible blogs and websites using a MySQL backend with PHP processing. WordPress has seen an incredible adoption rate among new and experienced engineers alike, and is a great choice for getting a website up and running efficiently. After an initial setup, almost all administration for WordPress websites can be done through its graphical interface these features and more make WordPress a great choice for websites built to scale.

## Creating a MySQL Database and User for WordPress

### Install MYSQL
* `sudo apt install mysql-server`
* `mysql --version`
* `sudo mysql_secure_installation`
* `sudo mysql_secure_installation`
```
There are three levels of password validation policy:
LOW Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary file
Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 1
Please set the password for root here.
New password:
Re-enter new password:
```
WordPress uses MySQL to manage and store site and user information. Although you already have MySQL installed, let’s create a database and a user for WordPress to use.

* `mysql -u root -p`
* `Mysql> CREATE DATABASE wordpress;`
* `Mysql> CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';`
* `Mysql> GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';`
* `Mysql> FLUSH PRIVILEGES;`
* `Mysql> exit;`

For more information:

* [MYSQL](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql)

### Installing Additional PHP Extensions
When setting up the LEMP stack, it required a very minimal set of extensions to get PHP to communicate with MySQL. WordPress and many of its plugins leverage additional PHP extensions, and you’ll use a few more in this tutorial.

Let’s download and install some of the most popular PHP extensions for use with WordPress by typing:

* `sudo apt update`
* `Sudo apt install php-fpm php-mysql`
* `Php --version`

When you are finished installing the extensions, restart the PHP-FPM process so that the running PHP processor can leverage the newly installed features:

* `sudo systemctl restart php7.4-fpm`

### Downloading WordPress
Now that your server software is configured, let’s download and set up WordPress. For security reasons, it is always recommended to get the latest version of WordPress directly from the project’s website.

Change into a writable directory and then download the compressed release by typing:

* `Sudo wget https://wordpress.org/latest.tar.gz`
* `Sudo tar –xzfv latest.tar.gz`

You will be moving these files into our document root momentarily, but before you do, let’s copy over the sample configuration file to the filename that WordPress actually reads:

* `cp /tmp/wordpress/wp-config-sample.php /tmp/wordpress/wp-config.php`
* `sudo nano /var/www/wordpress/wp-config.php`

The other change you should make is to set the method that WordPress uses to write to the filesystem. Since you’ve given the web server permission to write where it needs to, you can explicitly set the filesystem method to “direct”. Failure to set this with our current settings would result in WordPress prompting for FTP credentials when we perform some actions. Add this setting below the database connection settings, or anywhere else in the file:

```
/** The name of the database for WordPress */
* `define('DB_NAME', 'wpdb');`

/** MySQL database username */
* `define('DB_USER', 'wpuser');`

/** MySQL database password */
* `define('DB_PASSWORD', 'securepassword');`
```
Next, let’s make some changes to the main WordPress configuration file.
When you open the file, you’ll start by adjusting some secret keys to provide some security for our installation. WordPress provides a secure generator for these values so that you don’t have to come up with values on your own. These are only used internally, so it won’t hurt usability to have complex, secure values here.

To grab secure values from the WordPress secret key generator, type:
* `curl -s https://api.wordpress.org/secret-key/1.1/salt/`

Find the section that contains the dummy values for those settings.
Delete those lines and paste in the values you copied from the command line:

```
define('AUTH_KEY',         't|+6Q:::%gk|WytBVp-&RM)y6_cnRPR)T8lmCH`V#nKCI7+T&>fJ@UXA^p:@m@ I');
define('SECURE_AUTH_KEY',  'bz!L:w+b[u3 EPb+S8Xlg(Mm0Hab3#3X3k E*z4EKg-~hF05#RuB Nn8r)y}fE-*');
define('LOGGED_IN_KEY',    '$U&+B.=cx9VY@fU~uRFy=I+H}EqwG*2x8Q+BL!{L&+#Sm7PQd>e!Z>iq5~|;<e}]');
define('NONCE_KEY',        'D)Q5,a;v|G>lZ+~,$%Xp8KK11igveg%neBI G9dwVD%eT-X/VJA1:vZ>pr<NE#[@');
define('AUTH_SALT',        'gd0b=4D1Sz7VoBp;8t4+e+M~O[965{+*y/bPu}3|@_[>2{+soc3-E5FIi6*U)}ef');
define('SECURE_AUTH_SALT', 'p<.1UDiX;:-4]@+</e?e5%G6c-L*;PIOIPU[.q1}c+c673c2 !2}QlEq h`jHz(<');
define('LOGGED_IN_SALT',   'o{*S@UlE}Te1xF+;4EBwSd14E`$[%|(P//w9}+9~]HxY|2 QR1k1>N|[gwre!MS<');
define('NONCE_SALT',       'vrc]FgF]&-1w-18/-I|e)Dy?XS$ 0[r)7pP7PA^*qOR{+C$`60>]S@i>PL>r$a3F');
```
Save and close the file when you’re done.

In order for Nginx to serve this content, it’s necessary to create a server block with the correct directives. Instead of modifying the default configuration file directly, let’s make a new one at /etc/nginx/sites-available/your_domain:

* `sudo nano /etc/nginx/sites-available/your_domain`

Paste in the following configuration block, which is similar to the default, but updated for our new directory and domain name:
```
# Default server configuration
server {
        listen 80;
        listen [::]:80;
        server_name yahoo.com www.yahoo.com;
        return 301 https://$host$request_uri;
}
        # SSL configuration
server {
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
        server_name yahoo.com www.yahoo.com;

        # Self signed certs generated by the ssl-cert package
        ssl_certificate /etc/ssl/certs/yahoo.crt;
        ssl_certificate_key /etc/ssl/private/yahoo.key;
        # include snippets/snakeoil.conf;

        root /var/www/wordpress;

        # Add index.php to the list if you are using PHP
        index index.php index.html index.htm index.nginx-debian.html;


        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }

        # pass PHP scripts to FastCGI server
        location ~ \.php$ {
                include snippets/fastcgi-php.conf;

        #       # With php-fpm (or other unix sockets):
                fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        #       # With php-cgi (or other tcp sockets):
        #       fastcgi_pass 127.0.0.1:9000;
        }
}
```
### Completing the Installation Through the Web Interface
Now that the server configuration is complete, you can finish up the installation through WordPress’ web interface.

In your web browser, navigate to your server’s domain name or public IP address:
* `http://server_domain_or_IP/wordpress`

# Google.com/phonebook
# NGINX Reverse Proxy
Configure NGINX as a reverse proxy for HTTP and other protocols, with support for modifying request headers and fine-tuned buffering of responses.

This article describes the basic configuration of a proxy server. You will learn how to pass a request from NGINX to proxied servers over different protocols, modify client request headers that are sent to the proxied server, and configure buffering of responses coming from the proxied servers.

## Basic HTTP Proxy Pass

The most straight-forward type of proxy involves handing off a request to a single server that can communicate using http. This type of proxy is known as a generic “proxy pass” and is handled by the aptly named proxy_pass directive.

The proxy_pass directive is mainly found in location contexts. When a request matches a location with a proxy_pass directive inside, the request is forwarded to the URL given by the directive.
Let’s take a look at an example:
```
# Default server configuration
server {
        listen 80;
        listen [::]:80;
        server_name google.com www.google.com;
        return 301 https://$host$request_uri;
}

        # SSL configuration
server {
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name google.com www.google.com;

        # Self signed certs generated by the ssl-cert package
        ssl_certificate /etc/ssl/certs/google.crt;
        ssl_certificate_key /etc/ssl/private/google.key;

        # include snippets/snakeoil.conf;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index01.html index.htm index.nginx-debian.html;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }

        location /phonebook {
                  proxy_set_header HOST $host;
                  #proxy_set_header X-Forwarded-Proto $scheme;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_pass http://192.168.0.129:18080/;
        }

}
```
For more information:
[NGINX Reverse Proxy](https://www.digitalocean.com/community/tutorials/understanding-nginx-http-proxying-load-balancing-buffering-and-caching)

***
# Iptables
# What is iptables? 
iptables is a command line interface used to set up and maintain tables for the Netfilter firewall for IPv4, included in the Linux kernel. The firewall matches packets with rules defined in these tables and then takes the specified action on a possible match.

Tables is the name for a set of chains.
Chain is a collection of rules.
Rule is condition used to match packet.
Target is action taken when a possible rule matches. Examples of the target are ACCEPT, DROP, QUEUE.
Policy is the default action taken in case of no match with the inbuilt chains and can be ACCEPT or DROP.
Syntax:

* `iptables --table TABLE -A/-C/-D... CHAIN rule --jump Target`
* `sudo apt-get install iptables`
* `sudo iptables -L -v`
* `sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT`
* `sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT`
* `sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT`
* `sudo iptables -A INPUT -j DROP`

# make iptables persistent after reboot
Experienced Linux administrators likely know the frustration and pain that comes with a system reboot completely wiping a system’s iptables rules. That is because iptables rules, by default, will not persist after a reboot. After configuring your system’s iptables rules, there is one more important step thay you must do in order to make sure the rules are still there after a reboot.

* `sudo apt install iptables-persistent`
* `sudo iptables-save > /etc/iptables/rules.v4 `
* `sudo ip6tables-save > /etc/iptables/rules.v6`

You can then make sure that the service is running with the following command:
* `sudo systemctl status iptables`
