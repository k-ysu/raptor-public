# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from django.db import connection
from ...models import Youtube_Video
import warnings


#import modules
import pprint
import datetime


class Command(BaseCommand):




    video_30d_views_sql = '''
        select
            a.youtube_video_id as youtube_video_id,
            max(a.viewCount) as max_views,
            min(a.viewCount) as min_views,
            count(*) as count,
            CASE
            	WHEN count(id)<2 THEN max(a.viewCount)
            	ELSE  max(a.viewCount)-min(a.viewCount)
           END as 30d_views

         from  (
            select     id,    youtube_video_id,    viewCount,created_at   from streamer_youtube_history   where     ( date(created_at)=date(now()) OR date(created_at) = date(now()) - INTERVAL 10 day )
         ) as a
         group by  a.youtube_video_id

    '''

    def handle(self, *args, **options):

        dt_now = datetime.datetime.now()
        print("=======start deactivate video : {}==========".format(dt_now))

        #Filter
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        #video ids
        video_ids = []

        #LAST 30D viewCounts
        print("GET last 30d views")
        video_ids = self.getViewsLast30Dviews(video_ids)

        print("SET LOW Flags")
        self.setLowFlags(video_ids)


        print("=======END create_video_table : {}==========".format(dt_now))

    def setLowFlags(self,video_ids):
        videos = Youtube_Video.objects.filter(pk__in=video_ids, is_low_views=False)

        for v in videos:
            print(" Set low view count to this video => {} ".format(v.id))
            v.is_low_views = True
            v.active = False
            v.save()

    def getViewsLast30Dviews(self,video_ids):

        with connection.cursor() as cursor:
            cursor.execute(self.video_30d_views_sql)
            for row in cursor.fetchall():

                    youtube_video_id = row[0]
                    row_count = row[3]
                    view_last30d = row[4]

                    if row_count==2 and view_last30d<50:
                        #print(" Set low view count to this video => {}, {},{} ".format(youtube_video_id,view_last30d,row_count))
                        #print("views,{}".format(view_last30d))
                        video_ids.append(youtube_video_id)

        return video_ids
