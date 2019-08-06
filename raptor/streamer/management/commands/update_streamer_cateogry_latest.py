# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from ...models import Youtube_Video
from ...models import Streamer

#import modules
import pprint
import datetime



class Command(BaseCommand):
    help = '--streamer_id [id] : update or create specific streamer info '

    def add_arguments(self, parser):
            parser.add_argument('--streamer_id')

    def handle(self, *args, **options):

            #Start
            dt_now = datetime.datetime.now()
            print("=======start streamer category_latest_update : {}==========".format(dt_now))

            #SQL creation
            streamer_id = options['streamer_id']
            sql = "SELECT 1 as id, streamer_id, game_id, count(*) as num, MAX(youtube_created_at) as latest_update "
            sql += " FROM streamer_youtube_video "
            sql += " WHERE  DATEDIFF(current_date,youtube_created_at)<=60 "
            if streamer_id is not None:
                sql += " AND streamer_id = {} ".format(streamer_id)
            sql += " GROUP BY streamer_id,game_id"

            #Exectute
            results = Youtube_Video.objects.raw (sql)

            #Manipulate
            streamer_cateogry_latest = {}
            for r in results:
                print("streamer_id : {}, game_id : {}, number : {} , latest : {} ".format(r.streamer_id,r.game_id,r.num,r.latest_update) )

                r_streamer_id = r.streamer_id

                if r_streamer_id not in streamer_cateogry_latest:
                    streamer_cateogry_latest[r_streamer_id] = {}
                    streamer_cateogry_latest[r_streamer_id]['game_id'] = 0
                    streamer_cateogry_latest[r_streamer_id]['total'] = 0
                    streamer_cateogry_latest[r_streamer_id]['num'] = 0

                if r.num >= streamer_cateogry_latest[r_streamer_id]['num']:
                    streamer_cateogry_latest[r_streamer_id]['game_id'] = r.game_id
                    streamer_cateogry_latest[r_streamer_id]['num'] = r.num

                if 'latest_update' not in streamer_cateogry_latest[r_streamer_id]:
                    streamer_cateogry_latest[r_streamer_id]['latest_update'] = r.latest_update
                elif r.latest_update >= streamer_cateogry_latest[r_streamer_id]['latest_update']:
                    streamer_cateogry_latest[r_streamer_id]['latest_update'] = r.latest_update

                streamer_cateogry_latest[r_streamer_id]['total'] += r.num


            #Update Streamer
            for key,value in streamer_cateogry_latest.items():

                #get stremaer
                streamer_obj = Streamer.objects.get(pk=key)
                if streamer_obj is None:
                    break

                #if specific category video # is more than 50% of youtube_total_views
                update_category = 1
                if value['num']/value['total'] >= 0.5:
                    update_category = value['game_id']

                streamer_obj.game_id = update_category
                streamer_obj.last_youtube_uploaded = value['latest_update']


                try:

                    streamer_obj.save()

                except Exception as e:
                    print('=======================ERROR START : update_streamer_category_latest=======================')
                    dt_error_now = datetime.datetime.now()
                    print('{} : Video Update, Streamer_id => {} , YoutubeVideoId => {}'.format(dt_error_now,streamer_obj.streamer_name))
                    tb = sys.exc_info()[2]
                    print("message:{0}".format(e.with_traceback(tb)))
                    print('=======================ERROR END=======================')
