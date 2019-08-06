from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

#models
from ..models import Youtube_Video
from ..models import Streamer
from ..models import Game
from ..models import Youtube_Video_Rank
from ..models import Streamer_Rank

from ..utility.util import video_setup,getGameStreamerRank,getRecommendVideos,getNewVideosWithRating,getMostViewVideos,getGameRankData,getSeoSetting,getCommonSetting

import pprint

def streamer(request, streamer_id):

    streamer = None
    results = Streamer.objects.filter(id=streamer_id, active=1)
    if len(results)!=0:
        streamer = results[0]
    else:
        raise Http404("404 No Data")

    results = Streamer_Rank.objects.filter(streamer_id = streamer_id)
    if len(results)!=0:
        streamer_rank = results[0]
    else:
        streamer_rank = None


    #Streamer Game
    game = Game.objects.get(pk=streamer.game_id)

    #Nubmer of videos
    request_nums = 12
    if request.user_agent.is_mobile:
        request_nums = 12

    #new videos
    latest_video_lists = getNewVideosWithRating(streamer_id,None,request_nums)
    for v in latest_video_lists:
        v.streamer = streamer
        v = video_setup(v)

    #Pick newest video
    latest_video = latest_video_lists[0]

    #recommend videos
    recommends = getRecommendVideos(streamer_id,None, request_nums)
    for v in recommends:
        v.streamer = streamer
        v = video_setup(v)

    #most view videos
    most_views = getMostViewVideos(streamer_id,None, request_nums)
    for v in most_views:
        v.streamer = streamer
        v = video_setup(v)

    #Game STREAMER
    game_streamers= getGameStreamerRank(streamer.game_id , streamer_id, 10)

    #Get Popular Games
    popular_games = getGameRankData(10,10)

    #SEO
    seo_settings = getSeoSetting(request)
    common_settings = getCommonSetting(request)



    context = {
        'streamer': streamer ,
        'streamer_rank': streamer_rank,
        'game_streamers' : game_streamers,
        'latest_video': latest_video,
        'latest_video_lists':latest_video_lists,
        'recommends' : recommends,
        'most_views' : most_views,
        'game' : game,
        'popular_games': popular_games,
        'seo_settings' : seo_settings,
        'common_settings' : common_settings,
    }
    return render(request, 'streamer/streamer.html', context)
