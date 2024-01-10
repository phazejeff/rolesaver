import os
import discord
import pprint
import requests

# the patreon api might be the worst api i have ever had the displeasure to work with. there are some responses that literally give you links to 404s. their documentation is hilariously bad, and the python library hasnt been maintained in over 5 years. honestly its a miracle this works. i hope to never touch this bullshit again, but i know patreon will one day wake up and decide to change something without me knowing which will break everything.

class Patreon:
    BASE_URL = "https://www.patreon.com"
    TOKEN = os.environ["PATREON_TOKEN"]

    def __init__(self):
        self.TOKEN = os.environ["PATREON_TOKEN"]
        self.tier_ids = os.environ["PATREON_TIER_IDS"].split(",")
        self.campaign_id = self._get("/api/oauth2/v2/campaigns", params={
            "include" : "tiers",
            "fields[tier]" : "title"
        }).json()['data'][0]['id']           
        
    def _get(self, api, params=None):
        return requests.get(self.BASE_URL + api, headers={
            "Authorization" : "Bearer " + self.TOKEN
        }, params=params)
    
    def _get_no_base(self, api):
        return requests.get(api, headers={
            "Authorization" : "Bearer " + self.TOKEN
        })

    def get_premium_members(self):
        url = f"/api/oauth2/v2/campaigns/{self.campaign_id}/members"
        params = {
            "include": "currently_entitled_tiers,user",
            "fields[tier]" : "title",
            "fields[member]": "patron_status",
            # "include": "",
            "fields[user]" : "social_connections"
        }

        res = self._get(url, params=params).json()
        
        active_ids = []
        next = True

        while next:
            for member in res['data']:
                patron_status = member['attributes']['patron_status']
                patron_tiers = member['relationships']['currently_entitled_tiers']['data'] # [{'id' : '00000', 'type' : 'tier'},]

                if patron_status == 'active_patron' and [i['id'] for i in patron_tiers if i['id'] in self.tier_ids]: # 2nd part of this creates a new list based off the intersection of the two lists. if list is empty the if statement is false, because python
                    active_ids.append(member['relationships']['user']['data']['id'])

            try:
                next = res['links']['next']
                res = self._get_no_base(next).json()
            except:
                next = False
        
        next = True
        discord_ids = []
        res = self._get(url, params=params).json()

        while next:
            for member in res['included']:
                if member['id'] in active_ids:
                    try:
                        discord_ids.append(int(member['attributes']['social_connections']['discord']['user_id']))
                    except:
                        pass

            try:
                next = res['links']['next']
                res = self._get_no_base(next).json()
            except:
                next = False

        return discord_ids
    
    def is_member_premium(self, member: discord.Member):
        members = self.get_premium_members()
        return member.id in members
    
