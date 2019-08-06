#!/bin/bash

echo $0" : "`date +"%y-%m-%d %T"`
/bin/sh /Projects/raptor/cron/create_video_rank_table.sh
/bin/sh /Projects/raptor/cron/create_straemer_rank_table.sh



