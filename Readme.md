 Here is my flask boilerplate for a quick start.
 
## Getting started 
 
 ```sh
 virtualenv -p python3 ./env
 source env/bin/activate
 pipenv install

 adduser --system --shell /bin/bash --disabled-login hosting 
 
 addgroup hosting
 
 mkdir -p /var/www/hosting/nginx/{sites-enabled, ftpfiles, supervisor, conf_templates, repo, code, log}

 chown hosting:hosting /var/www/hosting -R
 
 setfacl -dR -m u:hosting:rwX, g:hosting:rwX /var/www/hosting
 
 setfacl -R -m u:hosting:rwX, g:hosting:rwX /var/www/hosting

 cp /var/www/hosting/code/supervisor/* /var/www/hosting/supervisor/

 in nginx.conf >> include /var/www/nginx/sites-enabled/*;

 run nginx_root_process.py to activate the nginx hup signal sending
 su
 /venv/python nginx_root_process.py

 run thread based workers
	
 # in production, run
 pipenv lock
 pipenv install --ignore-pipfile

 python run.py
 ```

 todo for dashboard:

## Attention
before serving request, start supervisor
to support php serving and plugin with uwsgi install php-embeded
install python-dev 

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
