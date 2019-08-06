# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from ...models import Log_History
import pprint
import datetime



class Command(BaseCommand):
    help = '--streamer_id [id] : update specific streamer info'

    def add_arguments(self, parser):
            parser.add_argument('--log' , required=True , help = '--log : path to log file ')
            parser.add_argument('--subject' , required=True , help = '--subject : subject for log' )


    def handle(self, *args, **options):

            dt_now = datetime.datetime.now()
            print("=======start Create Log history : {}==========".format(dt_now))

            #ARGS
            log_path = options['log']
            subject = options['subject']

            #file open
            print(" LOG FIle : {}".format(log_path))
            print(" Subject : {}".format(subject))

            log_data = open( log_path , "r")
            contents = log_data.read()

            #pprint.pprint(row[3])
            log_history = Log_History()
            log_history.subjecdt = subject
            log_history.log_history = contents
            log_history.save()

            print("=======End Create Log history : {}==========".format(dt_now))
