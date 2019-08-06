#!/bin/bash

echo $0" : "`date +"%y-%m-%d %T"`
SQL='Insert into streamer_youtube_history  select null,viewCount,likeCount,dislikeCount,favoriteCount,commentCount,youtube_created_at,now(),now(),game_id,streamer_id,id from streamer_youtube_video where active=True and is_ready=True'
mysql -ufake -pfake -h0.0.0.0 fake -e "$SQL"
