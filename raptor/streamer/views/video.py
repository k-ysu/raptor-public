from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

#models
from ..models import Youtube_Video
from ..models import Youtube_Video_Rank
from ..models import Streamer
from ..models import Game

from ..utility.util import video_setup, getGameStreamerRank, getRecommendVideos, getNewVideosWithRating, getGameRankData,getSeoSetting,getCommonSetting


def video(request, video_id):


    #Get Video
    video = None
    results = Youtube_Video.objects.filter(id = video_id, active=True)
    if len(results)!=0:
        video = results[0]
    else:
        common_settings = getCommonSetting(request)
        seo_settings = getSeoSetting(request)
        context = { 'common_settings' : common_settings, 'seo_settings' : seo_settings }
        return render(request, 'streamer/error.html', context, status=404)

    #Get Video Rank Info
    results = Youtube_Video_Rank.objects.filter(youtube_video_id = video_id)
    if len(results)!=0:
        video_rank = results[0]
        video.total_rank_deviationValue =  video_rank.total_rank_deviationValue
    else:
        streamer_rank = None

    #Video Setup
    video = video_setup(video)

    #Other needed objects
    streamer = Streamer.objects.get(pk=video.streamer_id)
    game = Game.objects.get(pk=video.game_id)

    #Game STREAMER
    game_streamers= getGameStreamerRank(video.game_id , streamer.id , 10)

    #Latest Videos
    video_lists = []
    results = getNewVideosWithRating(video.streamer_id,None,4)
    for v in results:
        v.streamer = streamer
        v = video_setup(v)
        video_lists.append(v)

    #Recommend
    results = getRecommendVideos(video.streamer_id,None, 12)
    for v in results:
        v.streamer = streamer
        v = video_setup(v)
        video_lists.append(v)

    #Get Popular Games
    popular_games = getGameRankData(10,10)

    #Get Popular Games
    popular_games_20 = getGameRankData(10,20)

    #SEO
    seo_settings = getSeoSetting(request)
    common_settings = getCommonSetting(request)


    context = {
        'video': video,
        'streamer': streamer,
        'rating_list':video.rating_list,
        'recommends':video_lists,
        'game':game,
        'game_streamers':game_streamers,
        'popular_games': popular_games,
        'seo_settings': seo_settings,
        'popular_games_20' : popular_games_20,
        'common_settings' : common_settings,
    }
    return render(request, 'streamer/video.html', context)
