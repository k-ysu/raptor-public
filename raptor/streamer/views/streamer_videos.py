from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.utils.translation import gettext as _

#models
from ..models import Youtube_Video
from ..models import Youtube_Video_Rank
from ..models import Streamer
from ..models import Game

from ..utility.util import video_setup,getGameStreamerRank,getRecommendVideos,getNewVideosWithRating,getMostViewVideos,getGameRankData,getSeoSetting,getCommonSetting

import pprint

def streamer_videos(request, streamer_id, sort):


    #Sort ID Map
    sort_id = None
    if sort == 'new':
        sort_id = 1
    elif sort == 'recommend':
        sort_id = 2
    elif sort == 'popular':
        sort_id = 3
    else:
        raise Http404("404 No Data")


    if Streamer.objects.filter(id=streamer_id, active=1).exists():
        streamer = Streamer.objects.get(pk=streamer_id)

        #Streamer Game
        game = Game.objects.get(pk=streamer.game_id)

        videos = []
        str = ""
        request_nums=60

        #new videos
        if sort_id == 1:
            videos = getNewVideosWithRating(streamer_id, None,request_nums)
            str = _('New Videos')

        #おすすめ
        elif sort_id == 2:
            videos = getRecommendVideos(streamer_id, None, request_nums)
            str = _('Reommend Videos(Top Rate)')

        #殿堂入り
        else:
            videos = getMostViewVideos(streamer_id,None, request_nums)
            str = _('Popular Videos(Top Views)')

        for v in videos:
            v.streamer = streamer
            v = video_setup(v)

        #Game STREAMER
        game_streamers= getGameStreamerRank(streamer.game_id , streamer_id)

        #Get Popular Games
        popular_games = getGameRankData(10,10)

        #SEO
        seo_settings = getSeoSetting(request)
        common_settings = getCommonSetting(request)


        context = {
            'streamer': streamer ,
            'videos' : videos,
            'h1_str' : str,
            'sort_id':sort_id,
            'game' : game,
            'game_streamers':game_streamers,
            'popular_games': popular_games,
            'seo_settings':seo_settings,
            'common_settings' : common_settings,

        }
        return render(request, 'streamer/streamer_videos.html', context)
    else:
        raise Http404("404 No Data")
