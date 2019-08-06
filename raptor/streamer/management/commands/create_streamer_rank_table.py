# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from django.db import connection
from ...models import Streamer_Rank_Tmp
from ...models import Game
from ...models import Streamer
import warnings


#import modules
import pprint
import datetime


class Command(BaseCommand):


    base_streamer_sql = '''
        select
            id,
            streamer_name,
            game_id,
            gender,
            youtube_channel_created,
            streamer_thumbnail,
            active,
            youtube_suscribers
        from
            streamer_streamer
        where 1
    '''

    streamer_48h_views_sql = '''
 select
 	a.streamer_id as streamer_id,
 	sum(a.view_count_last48h)  as total_view_count_last48h,
 	RANK() OVER ( ORDER BY  sum(a.view_count_last48h) DESC) AS last48h_view_rank,
 	RANK() OVER ( PARTITION BY b.game_id ORDER BY  sum(a.view_count_last48h) DESC) AS last48_game_view_rank,
    avg(total_rank_deviationValue) as avg_deviation
 from
 	streamer_youtube_video_rank as a left join streamer_streamer as b on a.streamer_id=b.id
 where 1 group by a.streamer_id, b.game_id

    '''

    streamer_48h_subscription_sql = '''

        select
            a.streamer_id as streamer_id,
            CASE
            	WHEN count(a.streamer_id)<3 THEN 0
            	ELSE  max(a.youtube_suscribers)-min(a.youtube_suscribers)
           END as 48h_subscription

         from  (
             select     streamer_id,youtube_suscribers,created_at   from streamer_streamer_history   where   1  and    date(created_at)   >= date(now()) - INTERVAL 2 day
         ) as a
         group by  a.streamer_id;
'''

    rename_sql ='''

        RENAME TABLE streamer_streamer_rank TO streamer_streamer_rank_tmp_2,
                     streamer_streamer_rank_tmp TO streamer_streamer_rank,
                     streamer_streamer_rank_tmp_2 TO streamer_streamer_rank_tmp;

    '''


    def handle(self, *args, **options):

        dt_now = datetime.datetime.now()
        print("=======start create_video_table : {}==========".format(dt_now))

        #Filter
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        #Builk list, total_score_list
        streamer_ranks = {}


        #GET Base Data
        print("GET BASE DATA")
        streamer_ranks  = self.getBaseData(streamer_ranks)

        #48h viewCounts
        print("GET last 48h views")
        streamer_ranks = self.getViewsLast48hours(streamer_ranks)

        #48h registNumbers
        print("GET last 48h views")
        streamer_ranks = self.getSubscriptionLast48hours(streamer_ranks)

        #Convert dict to list
        streamer_ranks_list = []
        for key in streamer_ranks.keys():
            temp = streamer_ranks[key]
            streamer_ranks_list.append(temp)

        #Truncate
        print("TRUNCATE Table")
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE streamer_streamer_rank_tmp;")

        #Bulk Update
        print("BULK Update")
        Streamer_Rank_Tmp.objects.bulk_create(streamer_ranks_list)

        #SWAP Table
        print("Swap Table")
        with connection.cursor() as cursor:
            cursor.execute(self.rename_sql)

        print("=======END create_video_table : {}==========".format(dt_now))

    def getViewsLast48hours(self,streamer_ranks):

        video_viewnums = {}

        with connection.cursor() as cursor:
            cursor.execute(self.streamer_48h_views_sql)
            for row in cursor.fetchall():

                s = streamer_ranks[row[0]]
                s.total_view_count_last48h = row[1]
                s.rank_in_total = row[2]
                s.rank_in_game = row[3]
                s.avg_deviation_score = row[4]

        return streamer_ranks



    def getSubscriptionLast48hours(self,streamer_ranks):

        video_viewnums = {}

        with connection.cursor() as cursor:
            cursor.execute(self.streamer_48h_subscription_sql)
            for row in cursor.fetchall():

                s = streamer_ranks[row[0]]
                s.total_subscribe_count_last48h = row[1]
                #print(s.total_subscribe_count_last48h)
                #print(vars(s))

        return streamer_ranks


    def getGameCategory(self):
        game_category = {}
        games = Game.objects.all()
        for g in games:
            game_category[g.id] = g.game_category
        return game_category


    def getBaseData(self,streamer_ranks ):

        game_category = self.getGameCategory()

        with connection.cursor() as cursor:
            cursor.execute(self.base_streamer_sql)
            for row in cursor.fetchall():


                #pprint.pprint(row[3])
                streamer_rank = Streamer_Rank_Tmp()
                streamer_rank.streamer = Streamer(id=row[0])
                streamer_rank.streamer_name = id=row[1]
                streamer_rank.game = Game(id=row[2])
                streamer_rank.game_category = game_category[streamer_rank.game.id]
                streamer_rank.gender = row[3]
                streamer_rank.youtube_channel_created = row[4]
                streamer_rank.streamer_thumbnail = row[5]
                streamer_rank.active = row[6]
                streamer_rank.youtube_suscribers = row[7]

                # Put streamer_rank into dict
                streamer_ranks[streamer_rank.streamer.id] = streamer_rank

        return streamer_ranks
