from ..models import Youtube_Video
import urllib.request
import json
import pprint
import ssl
import emoji
import sys
import datetime
import random
import logging
import time

class YoutubeApi():

    #ssl
    context = ssl.SSLContext()

    #api_key_primary = "fake", #Raptor Test API esports.raptor@gmail.com
    api_key_primary = 'fake' #Raptor1 API esports.raptor@gmail.com
    api_key_secondary = 'fake' #Raptor1 API esports.raptor@gmail.com
    #api_key_secondary = 'fake' #VideoApp API

    #Channel API detail
    channel_api = "https://www.googleapis.com/youtube/v3/channels?id={}&key={}&part={}"
    channel_part = "snippet,contentDetails,statistics"


    #Video List  API detail
    videolist_api = "https://www.googleapis.com/youtube/v3/playlistItems?playlistId={}&key={}&part={}&fields={}&maxResults={}"
    videolist_part = "contentDetails"
    videolist_fields = "nextPageToken,pageInfo,items(contentDetails,snippet(publishedAt,title,description,thumbnails(standard)))"

    #Popular Video List  API detail
    popular_videolist_api = "https://www.googleapis.com/youtube/v3/search?channelId={}&key={}&part={}&fields={}&maxResults={}&&order=viewCount"
    popular_videolist_part = "snippet"
    popular_videolist_fields = "nextPageToken,pageInfo,items(id,snippet(publishedAt,title,description,thumbnails(default)))"
    popular_max_results = 50

    #Youtube Video details
    video_api = 'https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part={}&fields={}&maxResults={}'
    video_part_all = 'snippet,statistics,status,id'
    video_part_statistics = 'statistics,id'
    video_fields_all = 'items(id,snippet(publishedAt,title,description,tags,thumbnails),status,statistics)'
    video_fields_statistics = 'items(id,statistics)'


    def get_api_key(self , type):
        ran_int = random.randint(0,0)

        #Sleep here to prevent from ban from youtube
        time.sleep(0.1)

        api_key = ''
        if type == 'updateVideoInfo':
            api_key = self.api_key_secondary
        else:
            api_key = self.api_key_primary

        return api_key

    def remove_emoji(self, src_str):
        return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

    def updateVideoInfo(self ,YVideos, video_ids , info_all):
        #pprint.pprint(YVideos)

        #remove last character ,
        video_ids = video_ids[:-1]

        #Part Switch
        video_part = ""
        if info_all == True:
            video_part = self.video_part_all
            video_fields= self.video_fields_all
        else:
            video_part = self.video_part_statistics
            video_fields= self.video_fields_statistics


        api_key = self.get_api_key('updateVideoInfo')
        url = self.video_api.format(video_ids,api_key,video_part,video_fields,50)
        req = urllib.request.Request(url)
        #pprint.pprint(url)
        with urllib.request.urlopen(req,context=self.context) as res:

            #Get Data
            body = json.load(res)
            #statics = body['items'][0]['statistics']
            #pprint.pprint(body)

            for item in body['items']:

                youtube_video_org_id = item['id']

                #Get Objects
                yvideo = YVideos[youtube_video_org_id]

                if yvideo is None:
                    print('No Video => {}'.format(youtube_video_org_id))
                    continue
                else:
                    print('Video Update, ID => {} , YoutubeVideoId => {}'.format(yvideo.id, youtube_video_org_id))


                #====Update Statics
                if 'statistics' in item:

                    statistics = item['statistics']
                    viewCount = statistics['viewCount'] if 'viewCount' in item['statistics'] else 0
                    likeCount = statistics['likeCount'] if 'likeCount' in item['statistics'] else 0
                    dislikeCount = statistics['dislikeCount'] if 'dislikeCount' in item['statistics'] else 0
                    favoriteCount = statistics['favoriteCount'] if 'favoriteCount' in item['statistics'] else 0
                    commentCount = statistics['commentCount'] if 'commentCount' in item['statistics'] else 0

                    yvideo.viewCount = viewCount
                    yvideo.likeCount = likeCount
                    yvideo.dislikeCount = dislikeCount
                    yvideo.favoriteCount = favoriteCount
                    yvideo.commentCount = commentCount


                #====The rest of info
                #pprint.pprint(info_all)
                if info_all == True:

                    video_title = self.remove_emoji( item['snippet']['title'] ) if 'title' in item['snippet'] else None
                    video_description = self.remove_emoji( item['snippet']['description'] ) if 'description' in item['snippet'] else None

                    if video_title == 'Deleted video':
                        yvideo.video_title = video_title
                        yvideo.video_description = video_description
                        yvideo.active = False
                        yvideo.save()
                        break


                    youtube_tag = item['snippet']['tags'] if 'tags' in item['snippet'] else None
                    youtube_created_at = item['snippet']['publishedAt'] if 'publishedAt' in item['snippet'] else None

                    video_thumbnail_medium = None
                    video_thumbnail_default = None
                    if 'thumbnails' in item['snippet']:
                        video_thumbnail_default = item['snippet']['thumbnails']['default']['url'] if 'default' in item['snippet']['thumbnails'] else None
                        video_thumbnail_medium = item['snippet']['thumbnails']['medium']['url'] if 'medium' in item['snippet']['thumbnails'] else None



                    status = item['status']
                    uploadStatus = status['uploadStatus']
                    privacyStatus = status['privacyStatus']
                    license = status['license']
                    embeddable = status['embeddable']
                    publicStatsViewable = status['publicStatsViewable']

                    yvideo.youtube_tag = youtube_tag
                    yvideo.video_title = video_title
                    yvideo.video_description = video_description
                    yvideo.youtube_created_at = youtube_created_at
                    yvideo.video_thumbnail_medium = video_thumbnail_medium
                    yvideo.video_thumbnail_default = video_thumbnail_default
                    yvideo.uploadStatus = uploadStatus
                    yvideo.privacyStatus = privacyStatus
                    yvideo.license = license
                    yvideo.embeddable = embeddable
                    yvideo.publicStatsViewable = publicStatsViewable
                    yvideo.will_info_update = False


                    if yvideo.privacyStatus == 'unlisted':
                        yvideo.active = False


                try:

                    yvideo.save()

                except Exception as e:
                    print('=======================ERROR START=======================')
                    dt_error_now = datetime.datetime.now()
                    print('{} : Video Update, ID => {} , YoutubeVideoId => {}'.format(dt_error_now,yvideo.id, youtube_video_org_id))
                    tb = sys.exc_info()[2]
                    print("message:{0}".format(e.with_traceback(tb)))
                    print('Deactive this video => {}'.format(yvideo.id))

                    #===Deactivate
                    yvideo.video_title = None
                    yvideo.video_description = None
                    yvideo.youtube_tag = None
                    yvideo.active = False
                    yvideo.save()

                    print('=======================ERROR END=======================')






    def UpdateStreamerInfo(self , s):

        streamer = s
        channel_part = self.channel_part

        #Only get banner is it is null
        if streamer.streamer_banner is None:
            channel_part = "{},brandingSettings".format(self.channel_part)

        api_key = self.get_api_key('UpdateStreamerInfo')
        url = self.channel_api.format(streamer.youtube_channel_id,api_key,channel_part)
        pprint.pprint(url)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req,context=self.context) as res:

            #Get Data
            body = json.load(res)
            statics = body['items'][0]['statistics']
            #pprint.pprint(body)
            #pprint.pprint(statics)

            #details Data
            youtube_upload_list_id = body['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            youtube_suscribers = statics['subscriberCount']
            youtube_total_views = statics['viewCount']
            youtube_total_videos = statics['videoCount']
            streamer_thumbnail =  body['items'][0]['snippet']['thumbnails']['default']['url']
            streamer_description = body['items'][0]['snippet']['localized']['description']
            youtube_channel_name = body['items'][0]['snippet']['localized']['title']
            youtube_channel_created = body['items'][0]['snippet']['publishedAt']

            #remove remove_emoji
            streamer_description = self.remove_emoji(streamer_description)
            youtube_channel_name = self.remove_emoji(youtube_channel_name)

            #Save to Streamer
            streamer.streamer_name = youtube_channel_name
            streamer.youtube_upload_list_id = youtube_upload_list_id
            streamer.youtube_suscribers = youtube_suscribers
            streamer.youtube_total_views = youtube_total_views
            streamer.youtube_total_videos = youtube_total_videos
            streamer.youtube_channel_created = youtube_channel_created
            streamer.streamer_thumbnail = streamer_thumbnail
            streamer.streamer_description = streamer_description
            streamer.is_ready = True

            #Only update banner is it is null
            if streamer.streamer_banner is None and 'bannerMobileImageUrl' in body['items'][0]['brandingSettings']['image']:
                streamer_banner = body['items'][0]['brandingSettings']['image']['bannerMobileImageUrl']
                streamer.streamer_banner = streamer_banner

            #youtube_channel_created // not used yet
            streamer.save()


    def postPopularVideoRequest(self ,streamer , pager_key):

        api_key = self.get_api_key('postPopularVideoRequest')
        url = self.popular_videolist_api.format(streamer.youtube_channel_id,api_key,self.popular_videolist_part,self.popular_videolist_fields,self.popular_max_results)

        if pager_key is not None:
            url += "&pageToken={}".format(pager_key)

        #pprint.pprint(url)
        req = urllib.request.Request(url)

        body = None
        with urllib.request.urlopen(req,context=self.context) as res:
            #Get Data
            body = json.load(res)

        return body

    def saveVideosFromResults(self, streamer, items, video_keys ):

        for item in items:

            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']

                if video_id in video_keys:
                    print(' -this video is exist => {}'.format(video_id))
                    continue
                else:
                    print(' -create new video => {}'.format(video_id))

                    #get meta data
                    video_title = self.remove_emoji( item['snippet']['title'] )
                    video_description = self.remove_emoji( item['snippet']['description'] )
                    youtube_created_at = item['snippet']['publishedAt']

                    #update video_keys_list
                    video_keys.append(video_id)

                    new_video = Youtube_Video()
                    new_video.streamer_id = streamer.id
                    new_video.game_id = 1 #Set no category for now
                    new_video.youtube_channel_id = streamer.youtube_channel_id
                    new_video.youtube_video_org_id = video_id
                    new_video.video_title = video_title
                    new_video.video_description = video_description
                    new_video.youtube_created_at = youtube_created_at
                    new_video.will_info_update = True
                    new_video.save()

        return video_keys

    def registerPopularVideo(self ,s):

        streamer = s
        video_keys = []

        #Get all video data
        videos = Youtube_Video.objects.filter(streamer=s.id)
        for video in videos:
            video_keys.append(video.youtube_video_org_id)

        pager = True
        pager_key = None
        loop = 1;
        while pager == True:

            print("get all video page {}".format(loop))
            loop += 1
            pager = False

            #Request
            body = self.postPopularVideoRequest(streamer,pager_key)
            #pprint.pprint(body)

            #save Data
            video_keys = self.saveVideosFromResults(streamer,body['items'],video_keys)

            if 'nextPageToken' in body and body['nextPageToken'] is not None:
                pager = True
                pager_key = body['nextPageToken']

            #inifinite loop save
            if loop >= 10000:

                #off the flag
                streamer.will_update_popular_video = False
                s.save()

                #kill the process
                sys.stderr.write('Infinite Loop, 10000+ loops. Shut down')
                sys.exit()

    def saveVideosFromUploadlistResults(self, streamer, items, video_keys ):

        for item in items:

            if 'contentDetails' in item:
                video_id = item['contentDetails']['videoId']

                if video_id in video_keys:
                    print(' -this video is exist => {}'.format(video_id))
                    continue
                else:
                    print(' -create new video => {}'.format(video_id))

                    #update video_keys_list
                    video_keys.append(video_id)

                    new_video = Youtube_Video()
                    new_video.streamer_id = streamer.id
                    new_video.game_id = 1 #Set Category to General
                    new_video.youtube_channel_id = streamer.youtube_channel_id
                    new_video.youtube_video_org_id = video_id
                    #new_video.video_title = video_title
                    #new_video.video_description = video_description
                    #new_video.youtube_created_at = youtube_created_at
                    new_video.will_info_update = True
                    new_video.save()

        return video_keys



    def postNewVideoRequest(self ,streamer ,max_results, pager_key):


        api_key = self.get_api_key('postNewVideoRequest')
        url = self.videolist_api.format(streamer.youtube_upload_list_id,api_key,self.videolist_part,self.videolist_fields,max_results)

        if pager_key is not None:
            url += "&pageToken={}".format(pager_key)

        pprint.pprint(url)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req,context=self.context) as res:

            #Get Data
            body = json.load(res)


        return body



    def registerNewVideo(self ,s , is_all_videos):

        streamer = s
        video_keys = []
        max_results = 10

        #Get all video data
        videos = Youtube_Video.objects.filter(streamer=s.id)
        for video in videos:
            video_keys.append(video.youtube_video_org_id)

        if not video_keys:
            max_results = 50

        if is_all_videos is True:
            max_results = 50


        pager = True
        pager_key = None
        loop = 1;
        while pager == True:

            print("get all video page {}".format(loop))
            loop += 1
            pager = False

            #Request
            body = self.postNewVideoRequest(streamer,max_results,pager_key)
            #pprint.pprint(body)

            #save Data
            video_keys = self.saveVideosFromUploadlistResults(streamer,body['items'],video_keys)

            if is_all_videos is False:
                #No Loop
                pager = False
            elif 'nextPageToken' in body and body['nextPageToken'] is not None:

                #Loop to end of the page
                pager = True
                pager_key = body['nextPageToken']

            #inifinite loop save
            if loop >= 10000:

                #off the flag
                streamer.will_update_popular_video = False
                s.save()

                #kill the process
                sys.stderr.write('Infinite Loop, 10000+ loops. Shut down')
                sys.exit()

        return
