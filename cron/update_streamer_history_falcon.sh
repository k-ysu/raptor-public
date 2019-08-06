#!/bin/bash

echo $0" : "`date +"%y-%m-%d %T"`
SQL='Insert into streamer_streamer_history select  null,youtube_channel_id,youtube_suscribers,youtube_total_views,youtube_total_videos,twitter_id,twitter_followers,twitter_followings,now(),now(),game_id,id from streamer_streamer where 1;'
mysql -ufake -pfake -h0.0.0.0 fake -e "$SQL"
