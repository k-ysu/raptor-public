# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from django.db import connection
from ...models import Youtube_Video
from ...models import Youtube_Video_Rank
from ...models import Youtube_Video_Rank_Tmp
from ...models import Game
from ...models import Streamer
import warnings
import sys

#import modules
import pprint
import datetime
import numpy as np


class Command(BaseCommand):

    present_word = [
        'プレゼント',
        '万円分',
        '無料で',
        'プレゼント'
    ]

    like_rate_sql = '''
        SELECT
            id,
            streamer_id,
            game_id,
            video_title,
            video_thumbnail_medium,
            viewCount,
            likeCount,
            dislikeCount,
            youtube_created_at,
            active,
            likeCount/(viewCount+1) as view_like_rate,
            RANK() OVER (ORDER BY  likeCount/(viewCount+1) DESC) AS view_like_rank,
            likeCount/(likeCount+dislikeCount+1) as like_dislike_rate,
            RANK() OVER (ORDER BY  likeCount/(likeCount+dislikeCount+1) DESC) AS like_dislike_rank
        FROM streamer_youtube_video
        where  active = True


    '''

    view_last_48h_sql = '''
        select
            a.youtube_video_id as youtube_video_id,
            CASE
                WHEN date(max(a.youtube_created_at))  >= date('{}')  - INTERVAL 2 day  THEN max(a.viewCount)
            	ELSE  max(a.viewCount)-min(a.viewCount)
           END as 48h_views

         from  (
            select     id,    youtube_video_id,    viewCount,created_at,youtube_created_at   from streamer_youtube_history   where   streamer_id = {}  and date(created_at)   >= date('{}') - INTERVAL 2 day
         ) as a
         group by  a.youtube_video_id
    '''

    rename_sql ='''

        RENAME TABLE streamer_youtube_video_rank TO streamer_youtube_video_rank_tmp_2,
                     streamer_youtube_video_rank_tmp TO streamer_youtube_video_rank,
                     streamer_youtube_video_rank_tmp_2 TO streamer_youtube_video_rank_tmp;

    '''


    def handle(self, *args, **options):

        dt_now = datetime.datetime.now()
        print("=======start create_video_table : {}==========".format(dt_now))

        #Filter
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        #Truncate First
        print("TRUNCATE Table")
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE streamer_youtube_video_rank_tmp;")

        #Get Rank value
        view_like_rank = {}
        like_dislike_rank = {}
        scores = []
        with connection.cursor() as cursor:
            exec_sql =  self.like_rate_sql + ' order by id '
            cursor.execute(self.like_rate_sql)
            for row in cursor.fetchall():
                view_like_rank[row[0]] = row[11]
                like_dislike_rank[row[0]] = row[13]
                total_scores = row[11] + row[13]
                scores.append(total_scores)

        #Streamer Loop ( All update take much time, connection will be gone, break it into sreamer loop )
        streamers = Streamer.objects.all();
        #streamers = Streamer.objects.filter(id=118)
        for streamer in streamers:

            #Builk list, total_score_list
            youtube_ranks = []

            print("====Create Rank table : {}====".format(streamer.streamer_name))

            #GET Base Data
            print("GET BASE DATA")
            youtube_ranks = self.getBaseData(youtube_ranks, scores, streamer, view_like_rank, like_dislike_rank)

            #Calc Diviation Value
            print("CALC Diviation Value")
            youtube_ranks = self.calcDiviationValue(youtube_ranks, scores)

            #48h viewCounts
            print("GET last 48h views")
            youtube_ranks = self.getViewsLast48hours(youtube_ranks, streamer)

            #Bulk Update
            print("BULK Update")


            try:

                Youtube_Video_Rank_Tmp.objects.bulk_create(youtube_ranks)

            except Exception as e:


                print('=======================ERROR START=======================')
                dt_error_now = datetime.datetime.now()
                print('{} : Video Update, ID => {} , Streamer Name => {}'.format(dt_error_now,streamer.id, streamer.streamer_name))
                tb = sys.exc_info()[2]
                print("message:{0}".format(e.with_traceback(tb)))
                print('Deactive this video => {}'.format(streamer.id))
                print('=======================ERROR END=======================')



            del youtube_ranks

        #SWAP Table
        print("Swap Table")
        with connection.cursor() as cursor:
            cursor.execute(self.rename_sql)

        print("=======END create_video_table : {}==========".format(dt_now))

    def getViewsLast48hours(self,youtube_ranks, streamer):

        video_viewnums = {}
        max_date = None
        with connection.cursor() as cursor:
            cursor.execute( " select max(created_at) from streamer_youtube_history " )
            for row in cursor.fetchall():
                max_date = row[0]

        with connection.cursor() as cursor:
            cursor.execute(self.view_last_48h_sql.format(max_date,streamer.id,max_date))
            for row in cursor.fetchall():
                video_viewnums[row[0]] = row[1]

        for v in youtube_ranks:
            if v.youtube_video.id in video_viewnums.keys():
                v.view_count_last48h = video_viewnums[v.youtube_video.id]
            else:
                v.view_count_last48h = 0

        return youtube_ranks


    def calcDiviationValue(self,youtube_ranks,scores):

        #pprint.pprint(scores)

        np_scores = np.array(scores)

        #Average
        mean = np.mean(np_scores)

        #Standard Deviation
        std = np.std(np_scores)

        for v in youtube_ranks:
            #print(v.total_rank)
            deviation = (v.total_rank - mean) / std
            deviation_value = 50 + deviation * 10
            deviation_value = 100 - deviation_value

            if deviation_value<0:
                deviation_value = 0
            if deviation_value>100:
                deviation_value = 100

            v.total_rank_deviationValue = deviation_value

            #print(vars(v))
            #print("avg => {}, score =>{}, deviation value =>{}".format(mean, v.total_rank, deviation_value))

        return youtube_ranks

    def getGameCategory(self):
        game_category = {}
        game_icon = {}
        game_name_sys = {}
        games = Game.objects.all()
        for g in games:
            game_category[g.id] = g.game_category
            game_icon[g.id] = g.game_icon
            game_name_sys[g.id] = g.game_name_sys
        return game_category, game_icon, game_name_sys


    def getBaseData(self,youtube_ranks,scores,streamer,view_like_rank, like_dislike_rank):

        game_category, game_icon, game_name_sys = self.getGameCategory()

        with connection.cursor() as cursor:

            baes_sql = self.like_rate_sql
            exec_sql = baes_sql + ' and streamer_id = {} '.format(streamer.id)
            cursor.execute(exec_sql)
            for row in cursor.fetchall():

                #pprint.pprint(row)
                #pprint.pprint(row[0])
                video_rank = Youtube_Video_Rank_Tmp()
                video_rank.youtube_video = Youtube_Video(id=row[0])
                video_rank.streamer = Streamer(id=row[1])
                video_rank.game = Game(id=row[2])
                video_rank.game_category = game_category[video_rank.game.id]
                video_rank.game_icon = game_icon[video_rank.game.id]
                video_rank.game_name_sys = game_name_sys[video_rank.game.id]
                video_rank.video_title = row[3]
                video_rank.video_thumbnail_medium = row[4]
                video_rank.viewCount = row[5]
                video_rank.likeCount = row[6]
                video_rank.dislikeCount = row[7]
                video_rank.youtube_created_at = row[8]
                video_rank.active =  row[9]
                video_rank.view_like_rate = row[10]
                video_rank.view_like_rank = view_like_rank[row[0]]
                video_rank.like_dislike_rate = row[12]
                video_rank.like_dislike_rank = like_dislike_rank[row[0]]
                video_rank.total_rank = video_rank.view_like_rank + video_rank.like_dislike_rank

                #streamer
                #streamer = streamer_dict[video_rank.streamer.id]
                video_rank.streamer_thumbnail = streamer.streamer_thumbnail
                video_rank.streamer_name = streamer.streamer_name

                if video_rank.view_like_rate > 1:
                    video_rank.view_like_rate = 1

                if video_rank.like_dislike_rate > 1:
                    video_rank.like_dislike_rate = 1

                #pprint.pprint(video_rank.youtube_video.id)

                #Check whether title is present word. it is not good video
                video_rank.is_video_title_present = False
                for word in self.present_word:
                    if word in video_rank.video_title:
                        video_rank.is_video_title_present = True


                #print(vars(video_rank))
                youtube_ranks.append(video_rank)


        return youtube_ranks
