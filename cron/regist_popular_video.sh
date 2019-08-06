#!/bin/bash


echo $0" : "`date +"%y-%m-%d %T"`
source /Projects/venv/raptor/bin/activate
python /Projects/raptor/raptor/manage.py update_streamer_info --non_ready
python /Projects/raptor/raptor/manage.py register_video --new_streamer --is_all_videos 
python /Projects/raptor/raptor/manage.py update_video_info --video_search 3 --info_type 1 --exec
python /Projects/raptor/raptor/manage.py update_video_category
/bin/sh /Projects/raptor/cron/update_streamer_category_latest.sh
