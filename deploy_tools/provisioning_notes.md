Provisioning a new site
=======================

## Required packages:

* nginx
* python >=3.6
* virtualenv + pip or conda env + conda
* git

E.g. on Ubuntu:

```bash
sudo apt install nginx git python36 python3.6-venv
```

## Nginx Virtual Host config

* See `nginx.template.conf`
* Replace `STIENAME` with, e.g., `staging.my-domain.com`

## Systemd service

* See `gunicorn-systemd.template.service`
* Replace `SITENAME` with, e.g., `staging.my-domain.com`

## Folder structure:
Assume we have a user account at /home/username

```
/home/username
└──sites
   └──SITENAME
      ├──database
      ├──source
      ├──static
      └──virtualenv
```
