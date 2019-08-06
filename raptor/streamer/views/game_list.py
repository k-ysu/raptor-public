from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

#models
from ..models import Youtube_Video
from ..models import Streamer
from ..models import Game


#utility
import pprint
from ..utility.util import getGameRankData,getSeoSetting,getCommonSetting
#from ..utility.util import video_setup,getGameStreamerRank,getNewVideosWithRating,getRecommendVideos,getMostViewVideos


def game_list(request, sort_id):

    if sort_id not in [1,2,3,10]:
        raise Http404("404 Invalid Sort Id")

    game_rank = getGameRankData(sort_id , None)
    seo_settings = getSeoSetting(request);
    common_settings = getCommonSetting(request);

    #Get Popular Games
    popular_games_navi = getGameRankData(10,20)

    context = {
        'sort_id':sort_id,
        'game_rank':game_rank,
        'seo_settings' : seo_settings,
        'popular_games_navi' : popular_games_navi,
        'common_settings' : common_settings,
    }

    return render(request, 'streamer/game_list.html', context)
