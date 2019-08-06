#!/bin/bash

echo $0" : "`date +"%y-%m-%d %T"`
#/bin/sh /Projects/raptor/cron/regist_popular_video.sh
#python /Projects/raptor/raptor/manage.py update_video_info --video_search 3 --info_type 1 --exec
/bin/sh /Projects/raptor/cron/set_low_views.sh
/bin/sh /Projects/raptor/cron/update_video_info.sh
/bin/sh /Projects/raptor/cron/update_video_category.sh
/bin/sh /Projects/raptor/cron/update_streamer_category_latest.sh
/bin/sh /Projects/raptor/cron/ping_google.sh
