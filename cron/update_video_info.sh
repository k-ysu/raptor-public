#!/bin/bash


echo $0" : "`date +"%y-%m-%d %T"`
source /Projects/venv/raptor/bin/activate
python /Projects/raptor/raptor/manage.py update_video_info  --video_search 1 --info_type 2 --exec 
python /Projects/raptor/raptor/manage.py update_video_info  --video_search 4 --info_type 1 --exec

