"""
VKontake HTTP API implementation stub
http://vk.com/pages?oid=-1&p=%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5_%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%BE%D0%B2_API
"""
from docutils.nodes import warning

__author__ = 'Nikolay Anokhin'

import datetime
import numpy
import csv
import io
import urllib2

import user
from api import Api
def save_page(id):
    response = urllib2.urlopen('http://vk.com/id'+str(id))
    html = response.read()
    f = open(str(id)+'.html', 'wb')
    f.write(html)
    f.close()

def get_page_info(id):
    response = urllib2.urlopen('http://vk.com/id'+str(id))
    html = response.read()
    w = html.find('<a name="wall">')
    if w!= -1:
        v = html[w:].find('slim_header')+w+len('slim_header>>')
        i = 0
        while not('0' <= html[v+i] and html[v+i] <= '9'):
            i = i+1
        v = v+i
        i = 0
        while '0' <= html[v+i] and html[v+i] <= '9':
            i = i+1
        try:
            wall = int(html[v:v+i])
        except:
            wall = -1
    else:
        wall = -1
    w = html.find('<a href="/albums')
    if w!= -1:
        v = html[w:].find('pm_counter')+w+len('pm_counter>>')
        i = 0
        while not('0' <= html[v+i] and html[v+i] <= '9'):
            i = i+1
        v = v+i
        i = 0
        while '0' <= html[v+i] and html[v+i] <= '9':
            i = i+1
        try:
            photo = int(html[v:v+i])
        except:
            photo = -1
    else:
        photo = -1
    w = html.find('act=idols')
    if w!= -1:
        v = html[w:].find('pm_counter')+w+len('pm_counter>>')
        i = 0
        while not('0' <= html[v+i] and html[v+i] <= '9'):
            i = i+1
        v = v+i
        i = 0
        while '0' <= html[v+i] and html[v+i] <= '9':
            i = i+1
        try:
            subs = int(html[v:v+i])
        except:
            subs = -1
    else:
        subs = -1

    return subs, wall, photo

class VkApi(Api):
    endpoint = "https://api.vk.com/method/{method}"

    def get_friend_ids(self, uid):
        json = self.call("friends.get", uid=uid)
        for friend_id in json.get("response", []):
            yield str(friend_id)

    def get_profiles(self, uid_list):
        uids = ",".join(uid_list)
        json = self.call("getProfiles", uids=uids,
                         fields="sex,status,contacts,relation")
        if json is not None:
            for user_json in json.get("response", []):
                yield self.json_to_user(user_json)

    def get_users(self, uid_list):
        uids = ",".join(uid_list)
        json = self.call("users.get", uids=uids, fields="uid,first_name,last_name,sex,bdate")
        for user_json in json.get("response", []):
            yield self.json_to_user(user_json)

    def json_to_user(self, json):
        u = user.User(json['uid'], json['first_name'], json['last_name'])
        ##university = json.get('universities')
        #if university and len(university) != 0:
        #    u.is_university = True
        #    u.grad_university = university[0].get('graduation')
        u.sex = json.get('sex')
        if json.get('relation'):
            u.relation = json.get('relation')
        if json.get('status') and len(json.get('status')) > 0:
            u.is_exist_status = 1
        u.number_of_friends = len(self.call("friends.get", uid=u.uid).get("response", []))
        u.subscriptions, u.wall_len, u.photos = get_page_info(u.uid)
        #u.subscriptions = len(self.call("subscriptions.get", uid=u.uid).get("response", []))
        #u.wall_len = len(self.call("wall.get", uid=u.uid).get("response", []))
        #u.photos = len(self.call("photos.getProfile", uid=u.uid).get("response", []))
        return u

    @staticmethod
    def parse_birth_date(birth_date_str):
        if birth_date_str:
            parts = birth_date_str.split('.')
            if len(parts) == 3:
                try:
                    return datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
                except ValueError:
                    print birth_date_str
                    raise



def main():
    num_of_requests = 20
    num_of_ids = 10
    maxid = 240 * 1000 * 1000
    #https://oauth.vk.com/authorize?client_id=1&scope=friends&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.12&response_type=token
    token = "f3f0323f0bf6d5790be2d23c646a0ba208495c3fcb98a82d3554da312fc9d453b1ba2bb9bddcb4f8d0fcd"
    api = VkApi(token)
    f = io.open("users.csv", "a", encoding='utf-8')
    for r in range(0, num_of_requests):
        uids = []
        for i in range(0, num_of_ids):
            uid = numpy.random.randint(1, maxid)
            uids.append(str(uid))
        for u in api.get_profiles(uids):
            f.write(u','.join(u.to_list())+'\n')
        f.flush()
        print("req"+str(r))
    f.close();
    print("Ok")


if __name__ == "__main__":
    main()