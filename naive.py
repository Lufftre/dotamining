train_set = []
for match_id, radiant_win, doc in corpus:
    match_str_win = []
    match_str_lose = []
    for player, msgs in doc.items():
        for msg in msgs:
            if radiant_win and player < 5:
                match_str_win.append(msg.lower())
            else:
                match_str_lose.append(msg.lower())
    train_set.append((' '.join(match_str_win), 'win'))
    train_set.append((' '.join(match_str_lose), 'lose'))

print(len(corpus))
all_words = set(word.lower() for passage in train_set for word in nltk.word_tokenize(passage[0]))
#t = [({word: (word in nltk.word_tokenize(x[0])) for word in all_words}, x[1]) for x in train_set]
#classifier = nltk.NaiveBayesClassifier.train(t)
#pickle.dump(classifier, open('classifier.p', 'wb'))
classifier = pickle.load(open('classifier.p', 'rb'))
for test_sentence in ['just end this team', 'ggwp ez )']:
    test_sent_features = {word.lower(): (word in nltk.word_tokenize(test_sentence.lower())) for word in all_words}
    print(test_sentence+':', classifier.classify(test_sent_features))


parsed_matches = []
win_bag = {}
lose_bag = {}
for match_id, radiant_win, doc in corpus:
    if match_id in parsed_matches:
        continue
    parsed_matches.append(match_id)
    for player, msgs in doc.items():
        if radiant_win and player < 5:
            for msg in msgs:
                msg = msg.lower()
                win_bag[msg] = win_bag.get(msg, 0) + 1
        else:
            for msg in msgs:
                msg = msg.lower()
                lose_bag[msg] = lose_bag.get(msg, 0) + 1

print(win_bag)
print(lose_bag)
print()
print(len(corpus))
print(sorted(win_bag, key=lambda k: -win_bag[k])[:20])
print(sorted(lose_bag, key=lambda k: -lose_bag[k])[:20])
#print(corpus)