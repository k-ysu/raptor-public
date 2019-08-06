from django.urls import path
#from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from streamer.sitemaps import VideoSitemap, DeletedVideoSitemap, StreamerSitemap, StreamerVideosSitemapNew, StreamerVideosSitemapRecommend, StreamerVideosSitemapPopular
from streamer.sitemaps import GameSitemap,GameVideosSitemapNew, GameVideosSitemapRecommend, GameVideosSitemapPopular
from streamer.sitemaps import RankingSitemap, GameListSitemap, StaticSitemap
from django.views.decorators.cache import cache_page
from . import views
from django.conf import settings


if settings.SERVER_SERVICE == 'jp':

    sitemaps = {
        'static': StaticSitemap,
        'streamer': StreamerSitemap,
        'game' : GameSitemap,
        'ranking': RankingSitemap,
        'game_list': GameListSitemap,
        #'streamer-videos-new' : StreamerVideosSitemapNew,
        #'streamer-videos-reommend' : StreamerVideosSitemapRecommend,
        #'streamer-videos-popular' : StreamerVideosSitemapPopular,
        #'game-videos-new' : GameVideosSitemapNew,
        #'game-videos-recommend' : GameVideosSitemapRecommend,
        #'game-videos-popular' : GameVideosSitemapPopular,
        #'video': VideoSitemap,
        #'deleted_video': DeletedVideoSitemap,
    }

else:

    sitemaps = {
        'static': StaticSitemap,
        'streamer': StreamerSitemap,
        'game' : GameSitemap,
        'ranking': RankingSitemap,
        'game_list': GameListSitemap
    }


cache_time = 60 * 30
if settings.SERVER_CONF == 'debug':
    cache_time = 0

urlpatterns = [
    path('', cache_page(cache_time)(views.index), name='top'),
    path('index', cache_page(cache_time)(views.index), name='index'),
    path('streamer/<int:streamer_id>', cache_page(cache_time)(views.streamer), name='streamer'),
    path('streamer_videos/<int:streamer_id>/<slug:sort>', cache_page(60*10)(views.streamer_videos), name='streamer_videos'),
    path('video/<int:video_id>', cache_page(cache_time)(views.video), name='video'),
    path('game/<slug:game_name_sys>', cache_page(cache_time)(views.game), name='game'),
    path('game_videos/<slug:game_name_sys>/<slug:sort>', cache_page(cache_time)(views.game_videos), name='game_videos'),
    path('game_list/<int:sort_id>', cache_page(cache_time)(views.game_list), name='game_list'),
    path('ranking/<slug:type>/<slug:sort_id>/<slug:category>/page/<int:page>', cache_page(cache_time)(views.ranking), name='ranking'),
    path('sitemap.xml/', cache_page(cache_time)(sitemaps_views.index), {'sitemaps': sitemaps , 'sitemap_url_name': 'sitemaps'}),
    path('sitemap-<section>.xml',cache_page(cache_time)(sitemaps_views.sitemap), {'sitemaps': sitemaps}, name='sitemaps'),
]


# 以下を定義
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
