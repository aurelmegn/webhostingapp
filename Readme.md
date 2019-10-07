 Here is my flask boilerplate for a quick start.
 
## Getting started 
 
 ```sh
 virtualenv -p python3 ./env
 source env/bin/activate
 pip install -r requirements.txt
 python run.py
 ```

 Todo:

- [ ] handle when there   is no application on the dashboard
- [ ] when the user create an app, notifications for setiing up the entry point, ftp dir, and other essentials information should be created
- [ ] add history log to the app actions
- [ ] show the last executed action and the time it was executed on app display
- [ ] figure out how to create the virtualenv of different version
- [ ] animation on click on execute command
- [ ] remove the directory of the app when issueing a command (by the client)
 todo for dashboard:

## workflow of normal user
add an app
wait for validation
upload files to ftp server
start the application

+ can see the log output of an application
+ improve the admin
+ mind how to create the virtualenv
+ mind how to issue a pip installation into the virtualenv
+ use svelte js framework for animations of the page and js dom manipulaction

https://dev.to/sm0ke/flask-dashboard-open-source-boilerplates-dkg
https://colorlib.com/polygon/gentelella/index2.html

## supervisor
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

## reseller offer
A2 hosting
InMotion Hosting
