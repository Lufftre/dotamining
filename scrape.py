import requests
import pickle
import os
import w8m8
from apikeys import steam_api

def scrape(n, corpus=[]):

    matches_url = 'https://api.opendota.com/api/explorer?sql=select%20match_id,radiant_win,duration,avg_mmr%20from%20public_matches%20where%20duration%20%3E%20900%20and%20lobby_type%20=%207%20and%20avg_mmr%20%3E%203000%20order%20by%20match_id%20desc%20limit%2010000'

    response = requests.get(matches_url)
    data = response.json()
    c = 0
    for i, row in enumerate(data['rows']):
        try:
            chat = get_chatlog(row['match_id'])
        except Exception:
            chat = {}

        if chat:
            corpus.append((row['match_id'], row['radiant_win'], row['duration'], row['avg_mmr'], chat))
            c += 1
        w8m8.progressbar(c/n)
        if c == n:
            break

    return corpus


def get_chatlog(match_id):
    match_url = 'https://api.opendota.com/api/matches/{}'
    response = requests.get(match_url.format(match_id))
    data = response.json()
    chatlog = {}
    if data.get('chat'):    
        for msg in data['chat']:
            if msg['type'] == 'chat':
                chatlog[msg['slot']] = chatlog.get(msg['slot'], []) + [msg['key']]
    return chatlog

if __name__ == '__main__':
    data = get_matchids()
    print(data)