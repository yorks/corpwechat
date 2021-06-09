#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import json
import time
import os


class API(object):
    """ Base class for most corpwechat API object.

    Args:
        configpath:  用来保存配置的文件路径，很重要，不要被其它人读取.
        corpid:  企业号的id，如果在配置文件中没有配置，可以在这里指定.
        corpsecret: 企业号的应用凭证密钥, 如没配置也可以在这里指定.
    """

    def __init__(self, configpath, corpid=None, corpsecret=None):
        self.api_pre    = 'https://qyapi.weixin.qq.com/cgi-bin/'
        self.configpath = configpath
        self.corpid     = corpid
        self.corpsecret = corpsecret

        self.config = self.get_config()

        cf_corpid = self.config.get('corpid', None)
        cf_corpsecret = self.config.get('corpsecret', None)
        if not cf_corpid:
            self.config['corpid'] = self.corpid
        if not cf_corpsecret:
            self.config['corpsecret'] = self.corpsecret
        self.access_tk = self.config.get('access_tk', None)
        self.tk_expires = self.config.get('tk_expires', int(time.time()))
        self.config['access_tk'] = self.access_tk
        self.config['tk_expires'] = self.tk_expires

        #print self.config




    def get_config(self):

        try:
            fp = open(self.configpath, 'r')
            content = fp.read()
            fp.close()
            return json.loads( content )
        except Exception as e:
            print (e)
            return {}

    def save_config(self):
        try:
            fw = open(self.configpath, 'w')
            fw.write(json.dumps(self.config))
            fw.close()
            return True
        except Exception as e:
            print (e)
            return False

    def get_token(self):
        now = int(time.time())
        if now <= self.config['tk_expires'] and self.config['access_tk']:
            return self.config['access_tk']

        if not self.config['corpid']:
            print ("missing corpid")
            return False
        if not self.config['corpsecret']:
            print ("missing corpsecret")
            return False
        #print "get new token..."
        payload = {'corpid':self.config['corpid'], 'corpsecret':self.config['corpsecret']}
        url = self.api_pre + 'gettoken'
        r = requests.get(url, params=payload)
        try:
            ret = r.json()
        except Exception as e:
            print (e)
            return False
        self.config['access_tk'] = ret['access_token']
        self.config['tk_expires'] = int(time.time()) + ret['expires_in'] - 10
        self.save_config()
        return self.config['access_tk']

    def _users_format_2_str(self, users):
        if isinstance(users, list):
            return '|'.join(users)
        else:
            return users

    def _push_message(self, agentid=0, msgtype='text', content={}, touser='@all',
            toparty='', totag='', safe=0):
        payload = {'touser': self._users_format_2_str(touser),
                   'toparty': self._users_format_2_str(toparty),
                   'totag': self._users_format_2_str(totag),
                   'agentid': agentid,
                   'msgtype': msgtype,
                    msgtype: content,
                }
        if msgtype != 'news':
            payload['safe'] = safe

        url = self.api_pre + 'message/send'
        tk  = self.get_token()
        r = requests.post(url, json=payload, params={'access_token':tk})
        try:
            ret = r.json()
        except Exception as e:
            print (e)
            return False
        return ret

    def push_text_msg(self, agentid=0, content='',
            touser='@all', toparty='', totag='', safe=0):
        return self._push_message(agentid=agentid, msgtype='text',
                content={'content':content},  touser=touser,
                toparty=toparty, totag=totag, safe=safe)

    def push_textcard_msg(self, agentid=0, title='', description='', url='',
            touser='@all', toparty='', totag='', safe=0):
        content = { "title" : title,
            "description" : description,
            "url" : url,
            "btntxt":"More"
            }
        return self._push_message(agentid=agentid, msgtype='textcard',
                content=content,  touser=touser,
                toparty=toparty, totag=totag, safe=safe)


    def push_image_msg(self, agentid=0, media_id='', filepath='',
            touser='@all', toparty='', totag='', safe=0):

        if not media_id:
            ret = self.upload_image(filepath)
            if not ret:
                return ret
            media_id = ret['media_id']

        return self._push_message(agentid=agentid, msgtype='image',
                content={'media_id':media_id},  touser=touser,
                toparty=toparty, totag=totag, safe=safe)

    def push_file_msg(self, agentid=0, media_id='', filepath='',
            touser='@all', toparty='', totag='', safe=0):

        if not media_id:
            ret = self.upload_file(filepath)
            if not ret:
                return ret
            media_id = ret['media_id']

        return self._push_message(agentid=agentid, msgtype='file',
                content={'media_id':media_id},  touser=touser,
                toparty=toparty, totag=totag, safe=safe)

    def push_voice_msg(self, agentid=0, media_id='', filepath='',
            touser='@all', toparty='', totag='', safe=0):

        if not media_id:
            ret = self.upload_voice(filepath)
            if not ret:
                return ret
            media_id = ret['media_id']

        return self._push_message(agentid=agentid, msgtype='voice',
                content={'media_id':media_id},  touser=touser,
                toparty=toparty, totag=totag, safe=safe)

    def push_video_msg(self, agentid=0, media_id='',filepath='',
            title='', description='',
            touser='@all', toparty='',  totag='', safe=0):

        if not media_id:
            ret = self.upload_video(filepath)
            if not ret:
                return ret
            media_id = ret['media_id']

        video_content = { 'media_id': media_id, 'title': title, 'description':description }

        return self._push_message(agentid=agentid, msgtype='video',
                content=video_content,  touser=touser,
                toparty=toparty, totag=totag, safe=safe)

    def push_news_msg(self, agentid=0, articles=None,
            touser='@all', toparty='', totag=''):
        return self._push_message(agentid=agentid, msgtype='news',
                content={'articles': articles},  touser=touser,
                toparty=toparty, totag=totag, safe=safe)

    def push_one_news_msg(self, agentid=0, title='', description='',
            url='', picurl='', touser='@all', toparty='', totag=''):
        articles = [
                {
                 'title':title,
                 'description':description,
                 'url':url,
                 'picurl':picurl,
                 }
        ]
        return self.push_news_msg(agentid=0, articles=articles,
                 touser=touser, toparty=toparty, totag=totag)

    def push_mpnews_msg(self, agentid=0, articles=None,
            touser='@all', toparty='', totag='', safe=0):
        return self._push_message(agentid=agentid, msgtype='mpnews',
                content={'articles': articles},  touser=touser,
                toparty=toparty, totag=totag, safe=safe)

    def push_one_mpnews_msg(self, agentid=0, title='', thumb_media_id='',
            author='', content_source_url='', content='', digest='',
            touser='@all', toparty='', totag='', safe=0):

        articles=[{
             "title": title,
             "thumb_media_id": thumb_media_id,
             "author": author,
             "content_source_url": content_source_url,
             "content": content,
             "digest": digest,
            }]
        return self.push_mpnews_msg(agentid=0, articles=articles,
                 touser=touser, toparty=toparty, totag=totag)




    def _upload(self, filepath, type_='file'):
        if not os.path.isfile(filepath):
            return False

        fsize = os.path.getsize(filepath)
        if type_ in ['image', 'voice'] and fsize >= 2*1024*1024:
            print ("file size too large > 2M")
            return False
        if type_ == 'video' and fsize >= 10*1024*1024:
            print ("file size too large > 10M")
            return False

        if type_ == 'file' and fsize >= 20*1024*1024:
            print ("file size too large > 20M")
            return False


        files = {'media': open(filepath, 'rb')}
        payload = {'type':type_}
        playload['access_token'] = self.get_token()
        r = requests.post(url, files=files, params=payload)
        try:
            ret = r.json()
        except Exception as e:
            print (e)
            return False
        return ret

    def upload_image(self, filepath):
        return self._upload(filepath, 'image')
    def upload_voice(self, filepath):
        return self._upload(filepath, 'voice')
    def upload_video(self, filepath):
        return self._upload(filepath, 'video')
    def upload_file(self, filepath):
        return self._upload(filepath, 'file')

    def get_agent_list(self):
        url = self.api_pre + 'agent/list'
        payload = {'access_token':self.get_token() }
        r = requests.get(url, params=payload)
        try:
            ret = r.json()
        except Exception as e:
            print (e)
            return False
        return ret





if __name__ == "__main__":
    aid = None
    content = None
    import sys
    try:
        cf = sys.argv[1]
        if not os.path.isfile(cf):
            content = cf
            cf = './config.json'
    except:
        cf = './config.json'

    corpwx = API(cf)
    tk = corpwx.get_token()
    if not tk:
        sys.exit(1)

    ret = corpwx.get_agent_list()
    if len(ret['agentlist']) == 1:
        aid = ret['agentlist'][0]['agentid']

    try:
        input = raw_input
    except:
        pass
    if not aid:
        for a in ret['agentlist']:
            print ("agentid:", a['agentid'], "name:", a['name'])
        aid = int(input('please input which agentid to send msg:'))
    if not content:
        content=input('please input the msg to send to @all:')
    print (corpwx.push_text_msg(agentid=aid, content=content))
