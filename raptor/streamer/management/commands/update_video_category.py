# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from ...models import Youtube_Video, Game_Tag

#import modules
import pprint
import datetime



class Command(BaseCommand):
    help = '--youtube_video_org_id [id] : update or create specific video info '
    MOBILE_TAG = ['mobile','スマホ','モバイル']
    GAME_DICT = {}
    GAME_CATEGORY_OTHERES = 1
    GAME_CATEGORY_PUBG_PC = 2
    GAME_CATEGORY_PUBG_MOBILE = 5
    GAME_CATEGORY_FORTNITE_PC = 4
    GAME_CATEGORY_FORTNITE_MOBILE = 18

    def add_arguments(self, parser):
            parser.add_argument('--youtube_video_org_id')
            parser.add_argument('--all', action='store_true')

    def handle(self, *args, **options):

            dt_now = datetime.datetime.now()
            print("=======start video category_update : {}==========".format(dt_now))

            youtube_video_org_id = options['youtube_video_org_id']
            is_all = options['all']

            #Get Game_Tag
            game_tags = Game_Tag.objects.all().order_by('priority')

            #Create Game Tag Dict
            for tag in game_tags:
                self.GAME_DICT[tag.game_tag.lower()] = tag.game_id

            #list of streamer objects
            videos = []

            #get all objects
            if youtube_video_org_id is not None:

                videos = Youtube_Video.objects.extra(where=[ "youtube_video_org_id = '{}'".format(youtube_video_org_id) ])


            elif is_all is True:

                where_state = " active = True AND ( is_ready = FALSE OR game_id = 1 ) "
                videos = Youtube_Video.objects.extra(where=[ where_state ]).order_by('id');

            else:

                where_state = " active = True AND is_ready = FALSE"
                videos = Youtube_Video.objects.extra(where=[ where_state ]).order_by('id');



            for v in videos:


                #deactivate
                if v.video_title is None:
                    v.active = False
                    v.save()
                    continue


                #set update_game_id to othres
                update_game_id = self.GAME_CATEGORY_OTHERES
                print("video_id:{},youtube_video_org_id:{}".format(v.id, v.youtube_video_org_id))

                #Get category id from game title
                update_game_id = self.get_category_from_title(v.video_title)

                #if game id is still GAME_CATEGORY_OTHERES, check tags
                if update_game_id == self.GAME_CATEGORY_OTHERES and v.youtube_tag is not None:
                    update_game_id = self.get_category_from_title(v.youtube_tag)

                print("GAME Category Update => {},{}".format(update_game_id,v.video_title))
                v.game_id = update_game_id;
                v.is_ready = True
                v.save()

    def get_category_from_title(self, str):

        #set up
        #print(str)
        title = str.lower()
        update_game_id = self.GAME_CATEGORY_OTHERES
        mobile_array = self.MOBILE_TAG
        game_dict = self.GAME_DICT

        #is mobile
        is_mobile = False
        for m_tag in mobile_array:
            if title.find(m_tag) >=0:
                is_mobile = True

        for g_tag, g_id in game_dict.items():

            #print('----id:{},tag:{}'.format(g_id,g_tag))
            if title.find(g_tag)>=0:

                update_game_id = g_id

                # IF game_id equal PUBG and is_mobile true, game_id is PUBG Mobile
                if update_game_id == self.GAME_CATEGORY_PUBG_PC and is_mobile == True:
                    update_game_id = self.GAME_CATEGORY_PUBG_MOBILE

                # IF game_id equal PUBG and is_mobile true, game_id is PUBG Mobile
                if update_game_id == self.GAME_CATEGORY_FORTNITE_PC and is_mobile == True:
                    update_game_id = self.GAME_CATEGORY_FORTNITE_MOBILE

                break

        return update_game_id
