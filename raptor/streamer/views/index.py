from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404


from ..utility.util import video_setup,getGameRankData,getVideoRank,getStreamerRank,getSeoSetting,getCommonSetting


def index(request):


    #Get Video Rank Data
    request_nums = 8
    if request.user_agent.is_mobile:
        request_nums = 4



    popular_videos = getVideoRank(2, 10, request_nums , 1 , 1)
    for v in popular_videos:
        v = video_setup(v)

    #Get Popular Games
    popular_games = getGameRankData(10,12)

    #Get Popular streamer_ranks
    request_nums_stream = 10
    streamer_ranks = getStreamerRank(1, 10, request_nums_stream, 1)

    #Get Video Rank Data
    recommends = getVideoRank(3, 10, request_nums , 1 , 1)
    for v in recommends:
        v = video_setup(v)

    #Get Popular Games
    popular_games_navi = getGameRankData(10,20)


    seo_settings = getSeoSetting(request)
    common_settings = getCommonSetting(request)

    context = {
        'popular_videos':popular_videos,
        'popular_games': popular_games,
        'streamer_ranks': streamer_ranks,
        'recommends': recommends,
        'seo_settings' : seo_settings,
        'popular_games_navi': popular_games_navi,
        'common_settings' : common_settings,
    }

    return render(request, 'streamer/index.html', context)
