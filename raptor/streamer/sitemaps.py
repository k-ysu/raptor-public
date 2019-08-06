from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url
from .models import Youtube_Video, Streamer, Game
from django.urls import reverse
import datetime
import pprint


class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        page_param = ['top']
        return page_param

    def lastmod(self, obj):
        return datetime.date.today()

    def location(self, item):
        return reverse(str(item))


class GameListSitemap(Sitemap):

    changefreq = "daily"
    priority = 0.8

    def items(self):
        page_param = [10,1,2,3]
        return page_param

    def lastmod(self, obj):
        return datetime.date.today()

    def location(self, item):
        return reverse('game_list', args=[str(item)])



class RankingSitemap(Sitemap):

    changefreq = "daily"
    priority = 0.8

    def items(self):
        page_param = [
            {'type': 'video', 'sort_id': 'all', 'category': 'all'},
            {'type': 'streamer', 'sort_id': 'all', 'category': 'all'},
            {'type': 'streamer', 'sort_id': 'all', 'category': 'male'},
            {'type': 'streamer', 'sort_id': 'all', 'category': 'female'},
        ]
        return page_param

    def lastmod(self, obj):
        return datetime.date.today()

    def location(self, item):
        return reverse('ranking', args=[str(item['type']), str(item['sort_id']),str(item['category']),1])



class VideoSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.1

    def items(self):
        return Youtube_Video.objects.filter(active=1, is_ready=1).order_by('id')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return reverse('video', args=[str(item.id)])

class DeletedVideoSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.1

    def items(self):
        return Youtube_Video.objects.filter(active=0).order_by('id')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return reverse('video', args=[str(item.id)])



class StreamerSitemap(Sitemap):

    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Streamer.objects.filter(active=1, is_ready=1).order_by('id')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return reverse('streamer', args=[str(item.id)])


class StreamerVideosSitemapNew(StreamerSitemap):
    def location(self, item):
        return reverse('streamer_videos', args=[str(item.id) , 'new'])

class StreamerVideosSitemapRecommend(StreamerSitemap):
    def location(self, item):
        return reverse('streamer_videos', args=[str(item.id) , 'recommend'])

class StreamerVideosSitemapPopular(StreamerSitemap):
    def location(self, item):
        return reverse('streamer_videos', args=[str(item.id) , 'popular'])


class GameSitemap(Sitemap):

    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Game.objects.filter(active=1).order_by('id')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return reverse('game', args=[str(item.game_name_sys)])

class GameVideosSitemapNew(GameSitemap):
    def location(self, item):
        return reverse('game_videos', args=[str(item.game_name_sys) , 'new'])

class GameVideosSitemapRecommend(GameSitemap):
    def location(self, item):
        return reverse('game_videos', args=[str(item.game_name_sys) , 'recommend'])

class GameVideosSitemapPopular(GameSitemap):
    def location(self, item):
        return reverse('game_videos', args=[str(item.game_name_sys) , 'popular'])
