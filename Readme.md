 Here is my flask boilerplate for a quick start.
 
 ## Getting started 
 
 ```sh
 virtualenv -p python3 ./env
 source env/bin/activate
 pip install -r requirements.txt
 python run.py
 ```

 Todo:

 - [ ] handle when there is no application on the dashboard
 - [ ]
## workflow of normal user
add an app
wait for validation
upload files to ftp server
start the application

+ can see the log output of an application
+ improve the admin
+ mind how to create the virtualenv
+ mind how to issue a pip installation into the virtualenv

firejail options

       --cpu=cpu-number,cpu-number,cpu-number
              Set CPU affinity.

              Example:
              $ firejail --cpu=0,1 handbrake
       --disable-mnt
              Blacklist /mnt, /media, /run/mount and /run/media access.

              Example:
              $ firejail --disable-mnt firefox
       --dns=address
              Set a DNS server for the sandbox. Up to three DNS servers can be defined.  Use this option if you don't trust the DNS setup  on  your
              network.

              Example:
              $ firejail --dns=8.8.8.8 --dns=8.8.4.4 firefox

              Note: this feature is not supported on systemd-resolved setups.
       --hostname=name
      Set sandbox hostname.

      --private options to check

      Example:
      $ firejail --hostname=officepc firefox


https://dev.to/sm0ke/flask-dashboard-open-source-boilerplates-dkg
https://colorlib.com/polygon/gentelella/index2.html

# supervisor
file hierachy

/supervisor
/supervisor/supervisord.conf
/supervisor/supervisord.log
/supervisor/supervisord.pid

/supervisor/programs
/supervisor/programs/user
/supervisor/programs/user/app1.ini

-- to add an app
create app config .ini
REREAD conf
add app into programs

-- to update app after changing the config
update app config .ini

REREAD conf
update app

# reseller offer
A2 hosting
InMotion Hosting