
# Project Title



## MYSQL Server

To install it, update the package index on your server if you’ve not done so recently:
```
  sudo apt update
  sudo apt install mysql-server
```
## Configuring MYSQL

```
sudo mysql_secure_installation
```
This will take you through a series of prompts where you can make some changes to your MySQL installation’s security options.
```
Securing the MySQL server deployment.

Connecting to MySQL using a blank password.

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No: Y

There are three levels of password validation policy:

LOW    Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary                  file

Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG:
 2
 Please set the password for root here.

New password:

Re-enter new password:
 ```

## Creating a Dedicated MySQL User and Granting Privileges

access to the root MySQL user:
```
sudo mysql
```
create a new user with a CREATE USER statement. These follow this general syntax:
```
CREATE USER 'sammy'@'localhost' IDENTIFIED 'password'
```
for example:
```
CREATE USER 'arvan'@'%' IDENTIFIED BY 'arvan';
```
fter creating your new user, you can grant them the appropriate privileges.
```
GRANT PRIVILEGE ON database.table TO 'username'@'host';
```
for example:
```
GRANT ALL PRIVILEGES ON *.* TO 'arvan'@'%';
```
it’s good practice to run the FLUSH PRIVILEGES command. This will free up any memory that the server cached as a result of the preceding CREATE USER and GRANT statements:
```
FLUSH PRIVILEGES;
```
to start up mysql service:
```
sudo systemctl start mysql.service
sudo systemctl enable mysql.service
```
## How To Allow Remote Access to MySQL

 This is MySQL’s default setting, but it won’t work for a remote database setup since MySQL must be able to listen for an external IP address where the server can be reached. To enable this, open up your mysqld.cnf file:
 ```
 sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
 ```
change the mysql bind address to:
 you could set this directive to a wildcard IP address, either *, ::, or 0.0.0.0:
Then restart the MySQL service
```
sudo systemctl restart mysql
```
make file in /opt/db-backup/

```
#!/bin/bash
#----------------------------------------
# OPTIONS
#----------------------------------------
USER='root'       # MySQL User
PASSWORD='' # MySQL Password
DAYS_TO_KEEP=5    # 0 to keep forever
GZIP=1            # 1 = Compress
BACKUP_PATH='/opt/db-backup'
#----------------------------------------

# Create the backup folder
if [ ! -d $BACKUP_PATH ]; then
  mkdir -p $BACKUP_PATH
fi

# Get list of database names
databases=`mysql -u $USER -p$PASSWORD -e "SHOW DATABASES;" | tr -d "|" | grep -v Database`

for db in $databases; do

  if [ $db == 'information_schema' ] || [ $db == 'performance_schema' ] || [ $db == 'mysql' ] || [ $db == 'sys' ]; then
    echo "Skipping database: $db"
    continue
  fi
  
  date=$(date -I)
  if [ "$GZIP" -eq 0 ] ; then
    echo "Backing up database: $db without compression"      
    mysqldump -u $USER -p$PASSWORD --databases $db > $BACKUP_PATH/$date-$db.sql
  else
    echo "Backing up database: $db with compression"
    mysqldump -u $USER --databases phonebook | gzip -c > $BACKUP_PATH/$date-$db.gz
  fi
done

# Delete old backups
if [ "$DAYS_TO_KEEP" -gt 0 ] ; then
  echo "Deleting backups older than $DAYS_TO_KEEP days"
  find $BACKUP_PATH/* -mtime +$DAYS_TO_KEEP -exec rm {} \;
fi

```
make cronjob with crontab -e and paste these commands here

```
rsync -rtu --delete /etc/opt/ root@192.168.30.4:/etc/opt/
sh /opt/mysqldump.sh
```
