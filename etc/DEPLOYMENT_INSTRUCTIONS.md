### Deployment instructions on Linux virtual machine

These instructions apply to any linux virtual machine (including Azure)

- Files stored in this directory are config files intended to be copied onto the virtual machine.
- All commands assume you have SSH'ed into the virtual machine and have command line access.


#### Install `Nginx`

Nginx is a web server. It directs requests from the internet (on port 80 for http:// traffic or port 443 for https:// traffic) to services running on the virtual machine.

We want to direct http requests to our Django service

1. run `sudo apt-get install nginx` to install nginx
2. copy the contents of the file `etc/nginx/sites-enabled/safeguard_nginx_config.conf` to the location `etc/nginx/sites-enabled/safeguard_nginx_config.conf` on the virtual machine
3. run `sudo service nginx restart`

#### Install `Supervisor`

'Supervisor' is a process manager.
We want to configure it to start the openfisca process when the virtual machine boots up.

1. run `sudo apt-get install supervisor`
2. copy the contents of the file `etc/supervisor/conf.d/safeguard_supervisor_config.conf` to the location `etc/supervisor/conf.d/safeguard_supervisor_config.conf` on the virtual machine
   - Pay attention to the `directory` and `command` in this config file. They should point to the directory which contains the virtual environment and the Django application bundle.
3. run `sudo supervisorctl reread`
4. run `sudo supervisorctl rerestart`
