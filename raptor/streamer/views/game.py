from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

#models
from ..models import Youtube_Video
from ..models import Streamer
from ..models import Game

from ..utility.util import video_setup,getGameStreamerRank,getNewVideosWithRating,getRecommendVideos,getMostViewVideos,getGameRankData,getSeoSetting,getCommonSetting

import pprint

def game(request, game_name_sys):

    #Get Game
    game = None
    game_id = None
    results = Game.objects.filter(game_name_sys=game_name_sys, active=1)
    if len(results)!=0:
        game = results[0]
        game_id = game.id
    else:
        raise Http404("404 No Data")

    request_nums = 12
    #if request.user_agent.is_mobile:
    #    request_nums = 4

    #Game STREAMER
    game_streamers= getGameStreamerRank(game_id , 0)
    rank=1;
    for s in game_streamers:
        s.rank = rank
        rank += 1

    #Have to get all stremers to reduce # of querys
    streamer_list = {}
    streamers_all = Streamer.objects.all()
    for s2 in streamers_all:
        streamer_list[s2.id] = s2

    latest_video_lists = getNewVideosWithRating( None ,game_id,request_nums)
    for v in latest_video_lists:
        v = video_setup(v)
        v.streamer = streamer_list[v.streamer_id]

    #Pick newest video
    latest_video = latest_video_lists[0]

    #most view videos
    most_views = getMostViewVideos(None,game_id,request_nums)
    for v in most_views:
        v = video_setup(v)
        v.streamer = streamer_list[v.streamer_id]

    #recommend videos
    recommends = getRecommendVideos(None,game_id,request_nums)
    for v in recommends:
        v = video_setup(v)
        v.streamer = streamer_list[v.streamer_id]

    #Get Popular Games
    popular_games = getGameRankData(10,20)


    seo_settings = getSeoSetting(request)
    common_settings = getCommonSetting(request)

    context = {
        'seo_settings' : seo_settings,
        'game_streamers' : game_streamers,
        'latest_video': latest_video,
        'latest_video_lists':latest_video_lists,
        'recommends' : recommends,
        'most_views' : most_views,
        'game' : game,
        'popular_games': popular_games,
        'common_settings' : common_settings,
    }
    return render(request, 'streamer/game.html', context)
