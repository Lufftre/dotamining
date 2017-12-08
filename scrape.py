import requests
import pickle
import os
from w8m8 import w8m8
from apikeys import steam_api

def scrape(tot):
    match_url = 'https://api.opendota.com/api/matches/{}'
    if os.path.exists('corpus.p'):
        corpus = pickle.load(open('corpus.p', 'rb'))
        ids = [corpus[-1][0]]
    else:
        corpus = []
        ids = []
    i = 0
    n = 0

    while n < tot:
        w8m8.progressbar(n/tot, i)
        try:
            if not i % 100:
                matches_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={}&matches_requested=100&skill=3'
                if ids:
                    matches_url += '&start_at_match_id=%s' % ids[-1]
                response = requests.get(matches_url.format(steam_api))
                ids = [match['match_id'] for match in response.json()['result']['matches']]
                if len(ids) == 0:
                    continue
            
            match_id = ids[i % len(ids)]

            response = requests.get(match_url.format(match_id))
            data = response.json()
            i += 1
            
            if not data.get('radiant_win') or not data.get('chat'):
                continue
            
            document = {}
            for msg in data['chat']:
                if msg['type'] == 'chat':
                    document[msg['slot']] = document.get(msg['slot'], []) + [msg['key']]
            corpus.append((match_id, data['radiant_win'], document))
            n += 1
        except Exception as error:
            print(error)
    w8m8.progressbar(n/tot)
    pickle.dump(corpus, open('corpus.p', 'wb'))



