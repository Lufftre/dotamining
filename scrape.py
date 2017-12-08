import requests
import pickle
import os
from w8m8 import w8m8
from apikeys import steam_api

def get_matchids(match_id=None):
    matches_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={}&matches_requested=100&skill=3&lobby_type=7'.format(steam_api)
    if match_id:
        matches_url += '&start_at_match_id={}'.format(match_id)

    print('STEAM API CALL')
    response = requests.get(matches_url)
    try:
        data = response.json()
    except Exception as error:
        print('Failed to get match ids')
        return None

    ids = [match['match_id'] for match in data['result']['matches']]
    return ids


def get_chatlog(match_id):
    match_url = 'https://api.opendota.com/api/matches/{}'

    print('OPENDOTA API CALL:', match_id)
    response = requests.get(match_url.format(match_id))
    try:
        data = response.json()
    except Exception as error:
        print('Failed to get match detalis ({})'.format(match_id))
        return None

    if not data.get('radiant_win') or not data.get('chat'):
        return None
    
    chatlog = {}
    for msg in data['chat']:
        if msg['type'] == 'chat':
            chatlog[msg['slot']] = chatlog.get(msg['slot'], []) + [msg['key']]

    return (match_id, data.get('radiant_win'), chatlog)


def scrape(tot, corpus=[]):
    
    ids = [corpus[-1][0]] if corpus else []
    n = 0
    match_id = None
    while n < tot:
        w8m8.progressbar(n/tot)
        while not ids:
            ids = get_matchids(match_id) if match_id else get_matchids()
        
        match_id = ids.pop()
        document = get_chatlog(match_id)
        if document:
            corpus.append(document)
            n += 1

    w8m8.progressbar(n/tot)
    return corpus



