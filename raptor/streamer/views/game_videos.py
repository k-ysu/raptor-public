from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.utils.translation import gettext as _

#models
from ..models import Youtube_Video
from ..models import Streamer
from ..models import Game

from ..utility.util import video_setup,getGameStreamerRank,getNewVideosWithRating,getRecommendVideos,getMostViewVideos,getGameRankData,getSeoSetting,getCommonSetting

import pprint

def game_videos(request, game_name_sys, sort):


    #Get Game
    game = None
    results = Game.objects.filter(game_name_sys=game_name_sys)
    if len(results)!=0:
        game = results[0]
        game_id = game.id
    else:
        raise Http404("404 No Data")

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

    videos = []
    str = ""
    request_nums=60


    #Game STREAMER
    game_streamers= getGameStreamerRank(game_id , 0)

    #Have to get all stremers to reduce # of querys
    streamer_list = {}
    streamers_all = Streamer.objects.all()
    for s2 in streamers_all:
        streamer_list[s2.id] = s2


    #new videos
    if sort_id == 1:
        videos = getNewVideosWithRating( None ,game_id,request_nums)
        str = _('New Videos')

    #おすすめ
    elif sort_id == 2:
        videos = getRecommendVideos(None,game_id,request_nums)
        str = _('Reommend Videos(Top Rate)')

    #殿堂入り
    else:
        videos = getMostViewVideos(None,game_id,request_nums)
        str = _('Popular Videos(Top Views)')

    for v in videos:
        v = video_setup(v)
        v.streamer = streamer_list[v.streamer_id]

    #Get Popular Games
    popular_games = getGameRankData(10,10)

    seo_settings = getSeoSetting(request)
    common_settings = getCommonSetting(request)

    context = {
        'seo_settings' : seo_settings,
        'videos' : videos,
        'h1_str' : str,
        'sort_id':sort_id,
        'game' : game,
        'game_streamers' : game_streamers,
        'popular_games': popular_games,
        'common_settings' : common_settings,

    }

    return render(request, 'streamer/game_videos.html', context)
