#!/bin/bash

echo $0" : "`date +"%y-%m-%d %T"`
source /Projects/venv/raptor/bin/activate
python -W ignore /Projects/raptor/raptor/manage.py update_streamer_cateogry_latest


