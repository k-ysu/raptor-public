#!/bin/bash

echo $0" : "`date +"%y-%m-%d %T"`
/bin/sh /Projects/raptor/cron/regist_new_video.sh 
/bin/sh /Projects/raptor/cron/create_video_rank_table.sh
