#!/bin/bash


echo $0" : "`date +"%y-%m-%d %T"`
source /Projects/venv/raptor/bin/activate
python /Projects/raptor/raptor/manage.py create_log_history --log /Projects/log/cron.log --subject CRON_LOG
python /Projects/raptor/raptor/manage.py create_log_history --log /Projects/log/cron_error.log --subject CRON_ERROR_LOG
python /Projects/raptor/raptor/manage.py create_log_history --log /Projects/log/nginx_error.log --subject NGINX_ERROR_LOG
