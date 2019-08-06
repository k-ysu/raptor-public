#!/bin/bash


echo $0" : "`date +"%y-%m-%d %T"`
source /Projects/venv/raptor/bin/activate
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name fortnite --post_type 1
sleep 3s
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name fortnite --post_type 2
sleep 3s
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name minecraft --post_type 1 
sleep 3s
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name minecraft --post_type 2
sleep 3s
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name knives-out --post_type 1
sleep 3s
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name knives-out --post_type 2
sleep 3s
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name super_mario_maker_2 --post_type 1
sleep 3s
python /Projects/raptor/raptor/manage.py post_new_video_twitter --game_name super_mario_maker_2 --post_type 2

