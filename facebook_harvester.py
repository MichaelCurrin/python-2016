#!usr/bin/env python
"""
Facebook queries


This is an extract from my full script, which just includes two classes created to handle Facebook insights data
"""
import urllib2
import json
import datetime
import csv

# configuration data
import config_fb_preferences as conf_pref # system
import config_fb_search_values as conf_search # brand input

from time import sleep

import my_logger

#==============================================================================
# CLASSES
#==============================================================================


class FB_Page(object):
    """
    The FB_Page object contains information about a brand's Facebook page
    and is created using an ID (numeric or text)
    It can include
     - profile properties
     - fans over time.    
    """
    # Class constants
    field_names = ('Page ID','Page Handle', 'Link', 'Picture', 'Cover Photo',
                   'Update Time')
    fan_fields = ('Page ID', 'Page Handle', 'End Time', 'Fans', 'Country')

    def __init__(self, page_id, get_page_properties=True):
        """
        Create FB_Page object using page_id.
        The page_id can be text or numeric id for queries, but
        numeric id is preferred as it is constant.
        """
        self.update_time = datetime.datetime.now()

        self.page_id = page_id
        self.handle = ''
        self.cover_photo =''
        self.picture = ''
        self.fan_data = []
        self.post_objects = []

        if get_page_properties:
            self.QueryProperties()


    ### Basic page properties ###

    def SetProperties(self, data):
        """Assign properties to object, from API 'data' response"""
        self.update_time = datetime.datetime.now()
        self.cover_photo = data['cover']['source']
        self.picture = data['picture']['data']['url']
        self.link  = data['link']
        self.handle = self.link.split('/')[3]

    def QueryProperties(self, attempts=3, seconds=5):
        """
        Try X times to load page info.
        Break on success.
        If loading fails, wait Y seconds then try again.
        """
        global page_url

        counter = 0

        while True:
            counter +=1
            task = 'Get page properties - %s' % self.page_id
            try:
                page_data = GetJSON(page_url % self.page_id)
                self.SetProperties(page_data)
                logger.info(task)
                break
            except ValueError as e:
                
                print 'Failed to load page'
                print ' - %s' % self.page_id
                print ' - %s' % e
                logger.error(task)

                if counter <= attempts:
                    sleep(seconds)
                else:
                    break

    def GetFields(self):
        """Get tuple of field names for basic properties"""
        return self.field_names

    def GetValues(self):
        """Get tuple of values for the object properties."""
        values = (self.page_id, self.handle, self.link, self.picture, 
                    self.cover_photo, self.update_time)
        return values

    def PrintProperties(self):
        """Print output of paired field names and values for object.
        This is intended for one post or small volumes of objects,
        as it requires a lot of lines."""
        print
        print 'Properties'
        print '----------'

        # create pairs of fields and values
        property_list = zip(self.GetFields(),self.GetValues())
        for pair in property_list:
            print ' - %s:    %s' % (pair)
        print

    def GetHandle(self):
        """Return text ID of page"""
        return self.handle

    def GetID(self):
        """Return numeric ID of page"""
        return self.page_id


    ### Page fans ###

    def GetFansOfCountry(self, country_code='ZA'):
        """Return stored fan values for just specified country, as a list"""
        out_data = []
        for day in self.fan_data:
            # Get data for day if there is are values for the end_date point
            # and if that country code exists. (note that if condition A is 
            # then condition B won't be not evaluated)
            if 'value' in day.keys() and country_code in day['value'].keys():
                day_filtered = (self.page_id,
                                self.handle,
                                day['end_time'], # Date
                                day['value'][country_code], # Fan value
                                country_code)
                out_data.append(day_filtered)
        return out_data
    
    def GetFanFields(self):
        """Get tuple of field names for fan values."""
        return self.fan_fields

    def QueryFans(self, attempts=3, seconds=5):
        global page_fan_url
        global QUIET
        global FAN_PERIODS
        global logger

        if not QUIET:
             print '\n### Get Fans For Page ###'
             print 'Page ID: %s' % self.page_id
             
        url = page_fan_url % self.page_id

        paging_info = [] # create here to prevent error on break validation
        index = 0
        
        while index < FAN_PERIODS:
            index +=1
            fan_log = 'handle: %s  -- fans query page: #%i' % (self.handle, 
                        index)
            if not QUIET:
                print fan_log
            logger.info(fan_log)

            counter = 0
            while True:
                counter += 1
                if not QUIET and counter > 0:
                    print ' (attempt %i)' % counter
                try:
                    page_fan_data_list, paging_info = GetData(url)
                    break
                except ValueError as e:
                    print 'ERROR'
                    print ' - No fan data returned'
                    print ' - url:   %s' % url
                    print ' - error:   %s' % e
                    logger.error('No fan data returned -- %s' % url)
                    if counter <= attempts:
                        sleep(seconds)
                    else:
                        break
            
            if page_fan_data_list:
                # there can only be one item in the list, hence 0 is used
                # this includes various dates and countries
                current_values = page_fan_data_list[0]['values']

                # add query page values to object's data store
                self.fan_data += current_values
            
            # paging:
            #  - 'next' takes you into the future
            #  - 'previous' takes you into the past
            #  - If you query the past 91 days  (the API limit),
            #    the API will give you the previous 91 days in 'previous'.
            #    This should continue indefinitely
            if paging_info and 'previous' in paging_info:
                url = paging_info['previous']        
            else:
                # break if there are no previous data to look up
                break

    ### Page posts ###
    def QueryPostData(self, seconds=5, attempts=3):
        """
        For this FB_Page object
        Iterate through query pages of posts 
        Process the posts
        Then add them as FB_Post objects in this page object
        Continue to next results query page
        Break if there are no data or next pages to process
        """
        global page_posts_url
        global QUIET
        global logger

        url = page_posts_url % self.page_id

        if not QUIET:
            print
            print 'Get Posts for Page'

        results_page = 0
        while True:
            results_page+=1
            
            # break when *counter* for a post matches attempt limit
            counter = 0
            while counter <= attempts:
                counter += 1
                if not QUIET and counter > 1:
                    print ' (attempt %i)' % counter

                try:
                    post_data, paging_data = GetData(url)
                    break # escape loop on post load success
                except:
                    logger.error(url)
                    sleep(seconds)

            if not post_data:
                # Break page looping if there are no posts to process
                break

            post_log = ' - %s -- query page: #%i -- %i posts' % (self.handle, 
                                                                results_page, 
                                                                len(post_data))
            if not QUIET:
                print post_log
            logger.info(post_log)

            # record time for each query page load, so assign to related posts
            query_time = datetime.datetime.now() 

            post_obj_list = []

            # initiate post objects with only ID, then send data to object
            # to fill in properties and engagements
            for post_item in post_data:

                post_id = post_item['id']

                if not QUIET:
                    print ' - %s -- post ID: %s' % (self.handle, str(post_id))

                PostObj = FB_Post(post_id, query_time=query_time)
                PostObj.SetProperties(post_item)
                PostObj.SetEngagements(post_item)
                self.post_objects.append(PostObj)

                # test enagagements
                #PostObj.GetEngagements()

            if 'next' in paging_data:
                next_page = paging_data['next']
                url = next_page
                # - this will return as 
                #       ...likes.limit%281%29.summary%28true%29...
                #    but there brackets here are encoded safely as %28 and %29
            else:
                # Break if there is no next URL to load
                break

    def GetPostObjects(self):
        return self.post_objects

    def PrintAllPosts(self):
        if self.post_objects:
            for PostObj in self.post_objects:
                PostObj.PrintProperties()
        else:
            'No posts to print for %s (ID: %s)' % (self.handle, self.page_id)
        print

class FB_Post(object):
    """
    Initiate Facebook post object


    example of data for one post in /posts query.

    {page-id}/posts?
        since=...,
        &until=...
        &fields=comments.limit(0).summary(true),likes.limit(0).summary(true),
            shares,id,message,story,created_time,link,full_picture,type
        &access_token=...

    data reponse.

    1st item:

    [
      {
         "id": "1545794585705491_1950942671857345",
         "message": "Wow! It's the Crazy Brands Sale! Get \"gila\" deals for the Holidays from Senheng here >>   http://bit.ly/2fZiwrG",
         "created_time": "2016-12-03T10:00:50+0000",
         "link": "https://www.facebook.com/11street.my/photos/a.1581996048752011.1073741828.1545794585705491/1950942671857345/?type=3",
         "full_picture": "https://fb-s-a-a.akamaihd.net/h-ak-xpa1/v/t1.0-9/15267732_1950942671857345_1725291430160183823_n.png?oh=9d67cf3bd3a5f86a05a1639e39e6b566&oe=58B3BA10&__gda__=1488660077_a0b9acdafc4ba62030a28d40908a45cb",
         "type": "photo",
         "likes": {
            "data": [
               
            ],
            "summary": {
               "total_count": 29,
               "can_like": true,
               "has_liked": false
            }
         },
         "comments": {
            "data": [
               
            ],
            "summary": {
               "order": "ranked",
               "total_count": 2,
               "can_comment": true
            }
         }
      }

    """
    # header can be access from the class without creating an instance
    field_names = ('Post ID', 'Page ID', 'Created Time', 'Message', 
                   'Type', 'Image',
                   'Likes', 'Comments', 'Shares',
                   'Post Link', 'Content Link','Update Time')

    def __init__(self, post_id, query_time):
        """
        Initiate empty post object with just an ID.
        raw_post is the data part of the post from the API
        """
        if query_time:
            self.update_time = query_time # time the query ran
        else:
            self.update_time = datetime.datetime.now() # time object is created

        # ID is in the form '{page id}_{short post id}''
        self.post_id = post_id 
        split_id = post_id.split("_")
        self.page_id = str(split_id[0])

        self.created_time='' # post date and time
        self.post_type='NOT SET'
        self.msg='NO MESSAGE'

        self.content_link='NOT SET'
        self.post_link='NOT SET'

        
        self.full_picture='http://www.iconsdb.com/icons/preview/gray'\
                                '/text-file-3-xxl.png'
        # - placeholder icon for no image:

        self.like_count = 0
        self.comment_count = 0
        self.share_count = 0

    ### Basic properties ###

    def SetProperties(self, raw_post):
        """
        Set basic info for the FB post.
        raw_post is the API response for the post.
        Either from this query for all posts
            'graph.facebook.com/{page_id}/posts'
        Or from this query for a specific post
            'graph.facebook.com/{post_id}'
        """
        # set update time
        self.update_time = datetime.datetime.now()
        
        # set time
        self.created_time = raw_post['created_time']

        # set content link        
        if 'link' in raw_post:
            self.content_link = raw_post['link']            

        # Set post link
        # - Attempt to create one from full post id
        # - If loading of link fails, then use content link as post link.
        self.post_link = 'https://www.facebook.com/%s' % raw_post['id']
        test_html_load = GetHTML(self.post_link)
        if not test_html_load:
            self.post_link = self.content_link

        # Set picture link
        if 'full_picture' in raw_post:
            self.full_picture = raw_post['full_picture']

        # Attempt to set message, otherwise story
        if 'message' in raw_post:
            self.msg = raw_post['message']
        elif 'story' in raw_post:
            # e.g. '{page name} updated their cover photo'
            self.msg = raw_post['story']
        elif 'description' in raw_post:
            self.msg = raw_post['description']

        # Set post type
        if 'type' in raw_post:
            self.post_type = raw_post['type']

    def GetPostID(self):
        """Return id of post"""
        return self.post_id

    ### Post engagements

    def SetEngagements(self, raw_post):

        self.update_time = datetime.datetime.now()

        if 'likes' in raw_post:
            self.like_count = raw_post['likes']['summary']['total_count']

        if 'comments' in raw_post:
            self.comment_count = raw_post['comments']['summary']['total_count']

        if 'shares' in raw_post and 'count' in raw_post['shares']:
            self.share_count = raw_post['shares']['count']

    def EnterEngagements(self, likes=None, comments=None, shares=None):
        """
        Manually set engagements using integer inputs
        Usage:
            Only set values for metrics which have been inputted,
            e.g. setting Obj.SetEngagements(likes=100,shares=9)
                    will leave comments as 0.
        """
        self.update_time = datetime.datetime.now()

        if likes:
            self.like_count = likes
        if comments:
            self.comment_count = comments
        if shares:
            self.share_count = shares
    
    def GetEngagements(self):
        """Get tuple of likes, comments and shares"""
        return self.like_count, self.comment_count, self.share_count


    ### Properties and engagements

    def GetFields(self):
        """ Get tuple of column headers for properties"""
        return self.field_names

    def GetValues(self):
        """Get tuple of values for the object, excluding header"""
        values = (self.post_id, self.page_id, self.created_time, self.msg,
                  self.post_type, self.full_picture,
                  self.like_count, self.comment_count, self.share_count,
                  self.post_link, self.content_link, self.update_time)
        return values

    def PrintProperties(self):
        """Print output of paired field names and values for object.
        This is intended for one post or small volumes of objects,
        as it requires a lot of lines."""
        print
        print 'Properties'
        print '----------'

        # create pairs of fields and values
        property_list = zip(self.GetFields(),self.GetValues())
        for pair in property_list:
            print ' - %s:    %s' % (pair)
        print

# ...
