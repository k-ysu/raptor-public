#!/bin/bash

echo $0" : "`date +"%y-%m-%d %T"`
/bin/sh /Projects/raptor/cron/update_streamer_history_falcon.sh
/bin/sh /Projects/raptor/cron/update_youtube_history_falcon.sh

