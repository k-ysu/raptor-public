from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.utils.translation import gettext as _

#models
from ..models import Streamer
from ..models import Game


#utility
import pprint
from ..utility.util import getGameRankData,getStreamerRank,getVideoRank,video_setup, getGameRankData, getSeoSetting,getCommonSetting
#from ..utility.util import video_setup,getGameStreamerRank,getNewVideosWithRating,getRecommendVideos,getMostViewVideos


def ranking(request, type, sort_id, category,page):


    if type == 'streamer':

        if sort_id not in ['all','growing','subscriber']:
            raise Http404("404 Invalid Sort Id")

        if category not in ['all','male','female']:
            raise Http404("404 Invalid Catgory")

        context = streamerRank(request, sort_id, category, page)
        return render(request, 'streamer/ranking_streamer.html', context)

    elif type == 'video':

        if sort_id not in ['all','toprate','new','views']:
            raise Http404("404 Invalid Sort Id")

        if category not in ['all','pc','mobile','console']:
            raise Http404("404 Invalid Catgory")


        context = videoRank(request, sort_id, category , page)
        return render(request, 'streamer/ranking_video.html', context)
    else:
        raise Http404("404 Invalid Type")



def streamerRank(request, sort_id, category, page):

    #sort_id
    sort_id_list = {
        'all' : 1,
        'growing' : 2,
        'subscriber' : 3,
    }
    sord_id_int = sort_id_list[sort_id]

    #sort_id
    category_id_list = {
        'all' : 10,
        'male' : 1,
        'female' : 2,
    }
    category_id = category_id_list[category]

    #h1 title
    h1_sort = {
        1: _('Total Views'),
        2: _('Growing'),
        3: _('Total Subscriber'),
    }
    h1_category = {
        10: "",
        1: _('Male '),
        2: _('Female '),
    }
    h1_streamer_title = {
        1: _('Game Streamer '),
        2: _('Game Streamer '),
        3: _('Game Streamer '),
    }


    h1_sort = h1_sort[sord_id_int]
    h1_streamer_title = h1_streamer_title[sord_id_int]
    h1_category = h1_category[category_id]

    #Get Streamer Rank Data
    results_per_page = 100
    streamer_ranks = getStreamerRank(sord_id_int, category_id, results_per_page, page)

    #Get Popular Games
    popular_games = getGameRankData(10,20)

    #Rank Start
    rank_start = results_per_page * (page - 1)

    #seo_settings
    seo_settings = getSeoSetting(request)
    common_settings = getCommonSetting(request)


    context = {
        'sort_id' : sort_id,
        'h1_sort' : h1_sort,
        'h1_streamer_title' : h1_streamer_title,
        'category' : category,
        'h1_category' : h1_category,
        'streamer_ranks' : streamer_ranks,
        'popular_games': popular_games,
        'rank_start': rank_start,
        'seo_settings': seo_settings,
        'common_settings': common_settings,
    }

    return context



def videoRank(request, sort_id, category , page):


    #sort_id
    sort_id_list = {
        'all' : 2,
        'toprate' : 3,
        'new' : 1,
        'views' : 4,
    }
    sord_id_int = sort_id_list[sort_id]

    #sort_id
    category_id_list = {
        'all' : 10,
        'pc' : 1,
        'mobile' : 2,
        'console' : 3,
    }
    category_id = category_id_list[category]



    #h1 title
    h1_sort = {
        1: _('New'),
        2: _('Total Views last 48hour'),
        3: _('Top Rate'),
        4: _('Total Views'),
    }

    h1_category = {
        10: "",
        1: "PC ",
        2: _('Mobile '),
        3: _('Console '),
    }

    h1_sort = h1_sort[sord_id_int]
    h1_category = h1_category[category_id]

    #Get Streamer Rank Data
    exlude_game_id=1
    video_ranks = getVideoRank(sord_id_int, category_id, 100 , page ,exlude_game_id )
    for v in video_ranks:
        v = video_setup(v)

    #Get Popular Games
    popular_games = getGameRankData(10,20)

    #seo_settings
    seo_settings = getSeoSetting(request)
    common_settings = getCommonSetting(request)

    context = {
        'sort_id' : sort_id,
        'category' : category,
        'h1_sort' : h1_sort,
        'h1_category' : h1_category,
        'video_ranks' : video_ranks,
        'popular_games': popular_games,
        'seo_settings': seo_settings,
        'common_settings' : common_settings,
    }

    return context
