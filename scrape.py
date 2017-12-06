import requests
# F6036466EC1574A73431ADEB21792D5B
# match_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={}'
# response = requests.get(match_url.format('F6036466EC1574A73431ADEB21792D5B'))
# print(response)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# Make a get request to get the latest position of the international space station from the opennotify api.
match_url = 'https://api.opendota.com/api/matches/{}'

corpus = []
for i in range(2):
    response = requests.get(match_url.format(3602154686 - i))
    data = response.json()
    radiant_win = data['radiant_win']
    print(radiant_win)
    # Print the status code of the response.
    document = [[],[]]
    if data['chat']:
        for asf in data['chat']:
            if asf['type'] == 'chat':
                if radiant_win and asf['slot'] < 5:
                    document[0].append(asf['key'])
                    # fmt = '\033[92m{}\033[0m'
                else:
                    document[1].append(asf['key'])
                    # fmt = '\033[91m{}\033[0m'
                # print(fmt.format(asf['key']))
        print('Added match to corpus')
        corpus.append(document)
    else:
        print('No chat available')
    #print('---')
for win, lose in corpus:
    for msg in win:
        print('\033[92m{}\033[0m'.format(msg))
    for msg in lose:
        print('\033[91m{}\033[0m'.format(msg))