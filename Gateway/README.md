
# Gateway Server


make password for user:

```
sudo su -
passwd
```
update and upgrade:
```
sudo su - # change user to root
apt update
apt upgrade -y
reboot
```
##set DNS
install resolvconf:
```
$ sudo apt update
$ sudo apt install resolvconf
```
to enable resolvconf service automaticlly
```
$ sudo systemctl start resolvconf.service
$ sudo systemctl enable resolvconf.service
```
put dns in this file:
```
$ vi /etc/resolvconf/resolv.conf.d/head
```
nameserver 1.1.1.1
nameserver 8.8.8.8
nameserver 3.3.3.3
nameserver 4.2.2.4

and then use this comand:
```
$ sudo systemctl restart resolvconf.service
$ sudo systemctl restart systemd-resolved.service
```
##Ip addresses

This server should have 3 interfaces (in accordance with the issue of one public IP and two private IPs); public IP that is given to server when it was created by Cloud-Init. In order to creating the private IP, we need to build a private network (LAN) through the ArvanCloud Panel. Click links to get acquainted with private network and IP addresses.
- [Private network](https://www.arvancloud.com/help/fa/article/360033968754-%D8%B4%D8%A8%DA%A9%D9%87-%D8%AE%D8%B5%D9%88%D8%B5%DB%8C-%DA%86%DB%8C%D8%B3%D8%AA-%D9%88-%DA%86%D9%87-%DA%A9%D8%A7%D8%B1%D8%A8%D8%B1%D8%AF%DB%8C-%D8%AF%D8%A7%D8%B1%D8%AF%D8%9F)
- [Ip Private](https://www.arvancloud.com/help/fa/article/360013105580-Private-IP-%DA%86%DB%8C%D8%B3%D8%AA%D8%9F)

```
cd /etc/netplan
cp 10-cloud-init.yaml 10-cloud-init.yaml.bak
vim 50-cloud-init.yaml
```
change 50-cloud-init.yaml

```
network:
    version: 2
    ethernets:
        eth0:
            dhcp4: true
            match:
                macaddress: fa:16:3e:90:40:43
            mtu: 1500
            set-name: eth0
        eth1:
            dhcp4: no
            addresses:
            - 192.168.0.232/24
            match:
                macaddress: fa:16:3e:c3:cf:3c
            mtu: 1442
            nameservers:
                addresses:
                - 8.8.8.8
                - 1.1.1.1
                search: []
            set-name: eth1
        eth2:
            dhcp4: no
            addresses:
            - 192.168.1.155/24
            match:
                macaddress: fa:16:3e:11:e6:97
            mtu: 1442
            nameservers:
                addresses:
                - 8.8.8.8
                - 1.1.1.1
                search: []
            set-name: eth2

```
use this to save file:
```
netplan apply
```
## Configure IP forwarding

open the configuration file:
```
sudo vim /etc/sysctl.conf 
```
Find and uncomment the following line
```
net.ipv4.ip_forward=1
```
then
```
sestemctl -p
```
Add a NAT forwarding rule to iptables:
```
iptables -t filter -A FORWARD -i eth2 -o eth0 -j ACCEPT
iptables -t filter -A FORWARD -i eth0 -o eth2 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE 
```
```
iptables -t filter -A FORWARD -i eth1 -o eth0 -j ACCEPT
iptables -t filter -A FORWARD -i eth0 -o eth1 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```
## port forwarding

```
iptables -t nat -I PREROUTING -p tcp -d 188.121.108.80 --dport 3306 -j DNAT --to-destination 192.168.1.204:3306
iptables -t nat -I POSTROUTING -p tcp -d 192.168.0.0/24 -j SNAT --to-source 192.168.0.232
iptables -t nat -I POSTROUTING -p tcp -d 192.168.1.0/24 -j SNAT --to-source 192.168.1.155
```

## backup to ArvanCloud

```
sudo apt-get install s3cmd
```
```
./s3cmd --configure
```
```
Access Key: <ACCESS_KEY>
Secret Key: <SECRET_KEY>
Default Region [US]: # NOTHING
S3 Endpoint [s3.amazonaws.com]: s3.ir-thr-at1.arvanstorage.com # YOUR STORAGE URL
DNS-style bucket+hostname:port template for accessing a bucket [%(bucket)s.s3.amazonaws.com]: %(bucket).s3.ir-thr-at1.arvanstorage.com
Encryption password: # NOTHING
Path to GPG program [/usr/bin/gpg]: # NOTHING
Use HTTPS protocol [Yes]: Yes
HTTP Proxy server name: # NOTHING
...
Test access with supplied credentials? [Y/n] Y
Please wait, attempting to list all buckets...
Success. Your access key and secret key worked fine :-)

Now verifying that encryption works...
Success. Encryption and decryption worked fine :-)

Save settings? [y/N] y
Configuration saved to '/root/.s3cfg'
```

check s3cmd
```
s3cmd -c /root/.s3cfg sync /opt/db-backup/ --preserve --delete-removed s3://bokharafirstproject
```