import logging
import requests
import json
import random
import time


logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage):

        # You can iterate over ids, or get list of objects
        # from any API, or iterate throught pages of any site
        # Do not forget to skip already gathered data
        # Here is an example for you

        config = json.load(open('config.json'))

        ids = self.collect_ids(config)
        match_ids = self.get_match_ids(ids, config)
        matches_data = self.get_match_data(match_ids, config)

        storage.write_data([matches_data])

    def collect_ids(self, config):
        vowels_lower = 'aeiou'
        vowels_upper = vowels_lower.upper()
        consonants_lower = "bcdfghjklmnpqrstvwxz"
        consonants_upper = consonants_lower.upper()
        names_int = 0
        ids = []

        while names_int<20:
            name = ''
            name = random.choice(vowels_upper)
            for i in range(random.randint(1, 2)):
                name += random.choice(consonants_lower)
                name += random.choice(vowels_lower)
            # name = 'Kortium'

            url = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/'+name+'?api_key='+config['api_key']
            response = requests.get(url)

            if not response.ok:
                logger.error(response.text)
                # then continue process, or retry, or fix your code

            else:
                # Note: here json can be used as response.json
                data = json.loads(response.text)
                ids.append(data["accountId"])
                names_int = names_int+1
                # save scrapped objects here
                # you can save url to identify already scrapped objects
            time.sleep(1/1.2)
        return ids


    def get_match_ids(self, ids, config):
        match_ids = []

        for player in ids:
            url = 'https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/'+str(player)+'/recent?api_key='+config['api_key']
            response = requests.get(url)

            if not response.ok:
                logger.error(response.text)
                if response.status_code == 429:
                    break
                # then continue process, or retry, or fix your code

            else:
                # Note: here json can be used as response.json
                data = json.loads(response.text)
                for j in range(0,len(data["matches"])):
                    match_ids.append(data["matches"][j]["gameId"])
            time.sleep(1/1.2)
        return match_ids

    def get_match_data(self, match_ids, config):
        text = '[ '
        for match in match_ids:
            url = 'https://euw1.api.riotgames.com/lol/match/v3/matches/'+str(match)+'?api_key='+config['api_key']
            response = requests.get(url)

            if not response.ok:
                logger.error(response.text)
                if response.status_code == 429:
                    break
                # then continue process, or retry, or fix your code

            else:
                # Note: here json can be used as response.json
                data = response.text
                text = text+data+','

            time.sleep(1/1.2)
        text = text[:-1]+']'
        return text
