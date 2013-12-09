VAR_DIRS := var
VAR_DIRS := ${VAR_DIRS} var/www var/www/static
VAR_DIRS := ${VAR_DIRS} var/www/media var/www/media/uploads
VAR_DIRS := ${VAR_DIRS} var/cache var/logs

all: production
production: permissions venv
staging: permissions venv
development: var_dirs venv

permissions: var_dirs
	sudo chown -R www-data ${VAR_DIRS}
	sudo chgrp -R staff ${VAR_DIRS}
	sudo chmod -R u+rw-x,g+rw-x,o-rwx ${VAR_DIRS}
	sudo chmod -R u+X,g+sX ${VAR_DIRS}


var_dirs: | ${VAR_DIRS}

${VAR_DIRS}:
	mkdir -p $@

venv: requirements.txt
	virtualenv venv
	venv/bin/pip install -r requirements.txt
	touch venv

.PHONY: var_dirs permissions virtualenv production staging development
