import pprint
import datetime
from pytz import timezone
from ..models import Game
from ..models import Streamer
from ..models import Streamer_Rank
from ..models import Youtube_Video_Rank
from ..models import Youtube_Video
from ..models import Game_Tag
from django.db import connection
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.cache import cache


def getCommonSetting(request):

    common_settings = {
        'server_config' : settings.SERVER_CONF,
        'server_service' : settings.SERVER_SERVICE,
    }

    return common_settings


def getSeoSetting(request):

    seo_settings = {
        'website' : _('CoreGameTV(Video Platform for gamers)'),
        'og_top_type' : 'website',
        'og_type' : 'article',
    }

    return seo_settings

def getVideoRank(sort_id, category, request_nums , page , exlude_game=None, target_game=None):

    sort = {
        1 : '-youtube_created_at',
        2 : '-view_count_last48h',
        3 : '-total_rank_deviationValue',
        4 : '-viewCount'
    }

    where_sql = " active = True "

    if category in [ Game.CATEGORY_PC, Game.CATEGORY_MOBILE,Game.CATEGORY_CONSOLE]:
        where_sql += " AND game_category = {} ".format(category)

    if sort_id == 3:
        where_sql += " AND view_count_last48h>=100 AND date(youtube_created_at) < date(now()) - INTERVAL 7 day "

    if exlude_game is not None:
        where_sql += " AND game_id != {}".format(exlude_game)

    if target_game is not None:
        where_sql += " AND game_id = {}".format(exlude_game)



    video_results = Youtube_Video_Rank.objects.extra(where=[ where_sql ]).order_by(sort[sort_id])
    paginator = Paginator(video_results, request_nums)
    videos = paginator.get_page(page)

    return videos



def getStreamerRank(sort_id, category, request_nums, page):

    sort = {
        1 : '-total_view_count_last48h',
        2 : '-total_subscribe_count_last48h',
        3 : '-youtube_suscribers',
    }

    #Get All Gams
    games_dict = {}
    all_games = Game.objects.all()
    for g in all_games:
        games_dict[g.id] = g

    streamer_results = []
    if category in [ Streamer.GENDER_MALE, Streamer.GENDER_FEMALE ]:
        streamer_results = Streamer_Rank.objects.filter(gender = category ).order_by(sort[sort_id])
    else:
        streamer_results = Streamer_Rank.objects.all().order_by(sort[sort_id])

    #Pager
    paginator = Paginator(streamer_results, request_nums)
    streamer_ranks = paginator.get_page(page)

    #Setup Game
    for s in streamer_ranks:
        s.game = games_dict[s.game_id]


    #streamer_ranks = Streamer_Rank.objects.filter(game_id = game_id ).exclude(id=exclue_streamer_id).order_by('-total_view_count_last48h')
    return streamer_ranks


def getGameRankData(sort_id , request_nums):

    #Get All Gams
    games_dict = {}
    all_games = Game.objects.all()
    for g in all_games:
        games_dict[g.id] = g


    #Game List order by 48h views
    sql = '''

        select
            game_id,
            sum(view_count_last48h)
        from
            streamer_youtube_video_rank
        where
            game_id !=1 AND active = True
    '''

    if sort_id is not 10:
        sql += ' AND game_category = {} '.format(sort_id)

    sql += 'GROUP by game_id HAVING (sum(view_count_last48h))>=10000  ORDER BY sum(view_count_last48h) desc'

    if request_nums is not None:
        sql += ' limit {} '.format(request_nums)

    #print(sql)

    game_rank = {}
    rank = 1;
    with connection.cursor() as cursor:
        cursor.execute(sql)
        for row in cursor.fetchall():
            game = games_dict[row[0]]
            game.last_48h_views = row[1]
            game_rank[rank] =game
            rank += 1

    return game_rank

def getNewVideosWithRating(streamer_id, game_id, request_nums ):

    #get new videos and create query

    if streamer_id is not None:
        videos = Youtube_Video.objects.filter(streamer_id = streamer_id , active = True).order_by('-youtube_created_at')[:request_nums]
    elif game_id is not None:
        videos = Youtube_Video.objects.filter(game_id = game_id , active = True).order_by('-youtube_created_at')[:request_nums]
    else:
        videos = Youtube_Video.objects.filter(active = True).order_by('-youtube_created_at')[:request_nums]

    where_sql = " active = 1 and youtube_video_id in (0"
    for v in videos:
         where_sql += ',{}'.format(v.id)
    where_sql += ',0)'


    #get rating
    deviation = {}
    #print(where_sql)
    rank_videos = Youtube_Video_Rank.objects.extra(where=[ where_sql ])
    for v2 in rank_videos:
        deviation[v2.youtube_video_id] = v2.total_rank_deviationValue

    #set deviation
    for v3 in videos:
        if v3.id in deviation:
            v3.total_rank_deviationValue = deviation[v3.id]

    return videos


def getRecommendVideos(streamer_id, game_id,request_nums ):

    format_str = None
    if streamer_id is not None:
        pre_sql = 'streamer_id = {} '
        format_str = streamer_id
    elif game_id is not None:
        pre_sql = 'game_id = {} '
        format_str = game_id
    else:
        pre_sql = ' {} '
        format_str = 1

    where_sql = pre_sql + ' AND view_count_last48h>=100 AND date(youtube_created_at) < date(now()) - INTERVAL 7 day AND active = True'


    videos = Youtube_Video_Rank.objects.extra(where=[ where_sql.format(format_str) ]).order_by('-total_rank_deviationValue')[:request_nums]
    if len(videos)<request_nums:
        where_sql = pre_sql
        videos = Youtube_Video_Rank.objects.extra(where=[ where_sql.format(format_str) ]).order_by('-total_rank_deviationValue')[:request_nums]

    return videos

def getMostViewVideos(streamer_id, game_id,request_nums):


    if streamer_id is not None:
        videos = Youtube_Video_Rank.objects.filter(streamer_id = streamer_id , active = True).order_by('-viewCount')[:request_nums]
    elif game_id is not None:
        videos = Youtube_Video_Rank.objects.filter(game_id = game_id, active = True).order_by('-viewCount')[:request_nums]
    else:
        videos = Youtube_Video_Rank.objects.filter(active = True).order_by('-viewCount')[:request_nums]

    return videos


def getGameStreamerRank(game_id ,exclue_streamer_id, request_nums=10000,):

    streamer_ranks = Streamer_Rank.objects.filter(game_id = game_id ).exclude(id=exclue_streamer_id).order_by('-total_view_count_last48h')[:request_nums]
    return streamer_ranks

def video_setup(v):


    if hasattr(v, 'total_rank_deviationValue'):
        v.rating = round(v.total_rank_deviationValue/70 * 5,2)
    else:
        v.rating = 0

    if v.__class__.__name__ == 'Youtube_Video':
        v.video_link_id = v.id
    elif v.__class__.__name__ == 'Youtube_Video_Rank':
        v.video_link_id = v.youtube_video_id

    v.rating_list = get_rating_path(v.rating)
    v.published_before = get_time_before(v.youtube_created_at)
    v.num_str = num_compression(v.viewCount)
    return v

def num_compression(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    #num = int(num)
    str =  '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
    #str = "{}{}".format(num,['', 'K', 'M', 'G', 'T', 'P'][magnitude])
    return str

def get_time_before(target_date_jst):
    #today = datetime.datetime.now()
    today = datetime.datetime.now(timezone('Asia/Tokyo'))
    today_timestamp = today.timestamp()
    target_timestamp = target_date_jst.timestamp()
    time_diff = today_timestamp-target_timestamp

    str = ""
    if time_diff <= 60 * 60 * 24:
        str = "{}時間前".format(int(time_diff/(60*60)))
    elif time_diff <= 60 * 60 * 24 * 30:
        str = "{}日前".format(int(time_diff/(60*60*24)))
    elif time_diff <= 60 * 60 * 24 * 30 * 12:
        str = "{}ヶ月前".format(int(time_diff/(60*60*24*30)))
    else:
        str = "{}年前".format(int(time_diff/(60*60*24*30*12)))

    return str

def get_rating_path(org_rate_num):

    # List of path to star
    rating_list = []

    if org_rate_num <1:
        for i in range(0,5):
            rating_list.append('streamer/img/star-empty.png')
        return rating_list

    #Put full star till int
    for num_loop in range(int(org_rate_num)):
        rating_list.append('streamer/img/star.png')


    #put half or empty star for the float
    float_num = org_rate_num - (num_loop+1)
    if float_num <= 0.25:
        rating_list.append('streamer/img/star-empty.png')
    else:
        rating_list.append('streamer/img/star-half.png')

    #put empty star for the rest to 5.
    for n in range(num_loop+2, 5):
      rating_list.append('streamer/img/star-empty.png')

    return rating_list


def getGameidFromStr(str):


        GAME_CATEGORY_OTHERES = 1
        GAME_CATEGORY_PUBG_PC = 2
        GAME_CATEGORY_PUBG_MOBILE = 5
        GAME_CATEGORY_FORTNITE_PC = 4
        GAME_CATEGORY_FORTNITE_MOBILE = 18

        title = str.lower()
        update_game_id = GAME_CATEGORY_OTHERES
        mobile_array = ['mobile','スマホ','モバイル']

        key = 'util.getGameidFromStr'
        game_dict = cache.get(key)
        if game_dict is None:

            game_dict = {}

            #Get Game_Tag
            game_tags = Game_Tag.objects.all().order_by('priority')

            #Create Game Tag Dict
            for tag in game_tags:
                game_dict[tag.game_tag.lower()] = tag.game_id

            cache.set(key, game_dict, 60)

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
                if update_game_id == GAME_CATEGORY_PUBG_PC and is_mobile == True:
                    update_game_id = GAME_CATEGORY_PUBG_MOBILE

                # IF game_id equal PUBG and is_mobile true, game_id is PUBG Mobile
                if update_game_id == GAME_CATEGORY_FORTNITE_PC and is_mobile == True:
                    update_game_id = GAME_CATEGORY_FORTNITE_MOBILE

                break

        return update_game_id
