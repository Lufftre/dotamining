from nltk import NaiveBayesClassifier, word_tokenize
from nltk.metrics.scores import precision, recall, f_measure
from nltk.corpus import stopwords
from collections import Counter
import w8m8
# import matplotlib.pyplot as plt
import numpy
import math
thresh = 5


def sdi(data):
    from math import log as ln
    
    def p(n, N):
        """ Relative abundance """
        if n is 0:
            return 0
        else:
            return (float(n)/N) * ln(float(n)/N)
            
    N = sum(data.values())
    
    return -sum(p(n, N) for n in data.values() if n is not 0)


class NaiveBoi(NaiveBayesClassifier):
    def __init__(self):
        self.vocabulary = []

    def get_features(self, document, duration, extra, selected_feats):
        words_in_document = set(document)
        features = {}


        if 'unigram' in selected_feats:
            for word in self.common_unigrams:
                features['word({})'.format(word)] = (word in words_in_document)

        if 'bigram' in selected_feats:
            for bigram in self.common_bigrams:
                features['bigram({})'.format(bigram)] = bigram in ' '.join(document)

        if 'trigram' in selected_feats:
            for trigram in self.common_trigrams:
                features['trigram({})'.format(trigram)] = trigram in ' '.join(document)

        if 'fourgram' in selected_feats:
            for fourgram in self.common_fourgrams:
                features['fourgram({})'.format(fourgram)] = fourgram in ' '.join(document)

        if 'fivegram' in selected_feats:
            for fivegram in self.common_fivegrams:
                features['fivegram({})'.format(fivegram)] = fivegram in ' '.join(document)

        if 'wp30' in selected_feats:
            wp30 = len(document) // (duration / 1800)
            bins = numpy.linspace(0, 200, 5)
            features['wp30'] = int(numpy.digitize(wp30, bins))
            # nchars = [0,0,0,0,0]
            # for player, message in extra:
            #     nchars[player] += len(message)
            # avg = sum(nchars) / 5
            # bins = numpy.linspace(0, 5, 5)
            # #features['chatter'] = int(numpy.digitize(max(nchars) / avg, bins))
            # features['chatter2'] = max(nchars) / sum(nchars) > 0.5

        if 'sdi' in selected_feats:
            nchars = {0:0,1:0,2:0,3:0,4:0}
            for player, message in extra:
                nchars[player] += len(message)
            bins = numpy.linspace(0, math.log(5), 5)
            features['sdi'] = int(numpy.digitize(sdi(nchars), bins))


        return features
    
    def parse_corpus(self, corpus):
        train_set = []
        for match_id, radiant_win, duration, avg_mmr, doc in w8m8.iterate(corpus, out='Parsing Corpus'):
            match_str_win = []
            match_str_win2 = []
            match_str_lose = []
            match_str_lose2 = []
            for player, msgs in doc.items():
                for msg in msgs:
                    #msg = ' '.join([spell(word) for word in msg.split()])
                    if player < 5:
                        if radiant_win:
                            match_str_win.append(msg.lower())
                            match_str_win2.append((player, msg.lower()))
                        else:
                            match_str_lose.append(msg.lower())
                            match_str_lose2.append((player, msg.lower()))
                    else:
                        if radiant_win:
                            match_str_lose.append(msg.lower())
                            match_str_lose2.append((player-5, msg.lower()))
                        else:
                            match_str_win.append(msg.lower())
                            match_str_win2.append((player-5, msg.lower()))

            if len(match_str_win) >=  thresh and len(match_str_lose) >= thresh:
                train_set.append(( ' '.join(match_str_win).split(), 'win', duration, match_str_win2))
                train_set.append((' '.join(match_str_lose).split(), 'lose', duration, match_str_lose2))
                
        return train_set

    def train(self, corpus, selected_feats):
        train_set = self.parse_corpus(corpus)
        print('Train set:', len(train_set))

        # # unigram
        self.unigrams = Counter([word for chat,win,duration,extra in train_set for word in chat])
        self.common_unigrams = [unigram for unigram, value in self.unigrams.items() if value > 1]
        # print(len(self.unigrams), len(self.common_unigrams))

        # # bigram
        self.bigrams = Counter([' '.join((word, chat[i+1])) for chat,win,duration,extra in train_set for i,word in enumerate(chat[:-1])])
        self.common_bigrams = [bigram for bigram, value in self.bigrams.items() if value > 1]
        # print(len(self.bigrams), len(self.common_bigrams))
        # # trigram
        self.trigrams = Counter([' '.join((word, chat[i+1], chat[i+2])) for chat,win,duration,extra in train_set for i,word in enumerate(chat[:-2])])
        self.common_trigrams = [trigram for trigram, value in self.trigrams.items() if value > 1]
        # print(len(self.trigrams), len(self.common_trigrams))
        # # fourgram
        self.fourgrams = Counter([' '.join((word, chat[i+1], chat[i+2], chat[i+3])) for chat,win,duration,extra in train_set for i,word in enumerate(chat[:-3])])
        self.common_fourgrams = [fourgram for fourgram, value in self.fourgrams.items() if value > 1]
        # print(len(self.fourgrams), len(self.common_fourgrams))
        # # fivegram
        self.fivegrams = Counter([' '.join((word, chat[i+1], chat[i+2], chat[i+3], chat[i+4])) for chat,win,duration,extra in train_set for i,word in enumerate(chat[:-4])])
        self.common_fivegrams = [fivegram for fivegram, value in self.fivegrams.items() if value > 1]
        # print(len(self.fivegrams), len(self.common_fivegrams))

        ###### WP30 PLOT #######
        # wp30s = [len(chat) // (duration / 1800) for chat,win,duration,extra in train_set]
        # n, bins, patches = plt.hist(wp30s, 100,alpha=0.75)
        # plt.show()
        # self.doclen = Counter([len(chat) for chat,win,duration in train_set])



        ###### CHATTER PLOT ######
        # data = []
        # for chat, win, duration,extra in w8m8.iterate(train_set, out='Training'):
        #     nchars = [0,0,0,0,0]
        #     for player, message in extra:
        #         nchars[player] += len(message)
        #     avg = sum(nchars) / 5
        #     data.append(max(nchars) / avg)
        # n, bins, patches = plt.hist(data, 1000,alpha=0.75)
        # plt.show()

        t = []
        for chat, win, duration,extra in w8m8.iterate(train_set, out='Training'):
            features = self.get_features(chat, duration, extra, selected_feats)
            t.append((features, win))
        self.classifier = NaiveBayesClassifier.train(t)  
        self.classifier.show_most_informative_features(20)

    def test(self, corpus, selected_feats):
        test_set = self.parse_corpus(corpus)
        print('Test set:', len(test_set))

        # winpreds = 0

        # Predict match winner
        correct_match = 0
        it = iter(w8m8.iterate(test_set, out='Testing'))
        for chat,win,duration,extra in it:
            guess = self.classify(chat,duration,extra, selected_feats, prob=True)
            chat,win2,duration,extra = next(it)
            guess2 = self.classify(chat,duration,extra, selected_feats, prob=True)
            if guess.prob('win') > guess2.prob('win'):
                correct_match += 1

        # Predict individual team chatlogs
        winpreds = set()
        losepreds = set()
        wingold = set()
        losegold = set()
        correct_individual = 0
        for i,(chat,win,duration,extra) in enumerate(w8m8.iterate(test_set, out='Testing')):
            guess = self.classify(chat,duration,extra, selected_feats)
            if guess == 'win':
                winpreds.add(i)
            else:
                losepreds.add(i)
            if win == 'win':
                wingold.add(i)
            else:
                losegold.add(i)
            if win == guess:
                correct_individual += 1

        p_win = precision(wingold, winpreds)*100
        r_win = recall(wingold, winpreds)*100
        f_win = f_measure(wingold, winpreds)*100
        p_lose = precision(losegold, losepreds)*100
        r_lose = recall(losegold, losepreds)*100
        f_lose = f_measure(losegold, losepreds)*100
        print('Win:')
        print('Precision: {:.2f}%'.format(p_win))
        print('Recall: {:.2f}%'.format(r_win))
        print('F-measure: {:.2f}%\n'.format(f_win))

        print('Lose:')
        print('Precision: {:.2f}%'.format(p_lose))
        print('Recall: {:.2f}%'.format(r_lose))
        print('F-measure: {:.2f}%\n'.format(f_lose))

        print('Individual accuracy: {:.2f}%'.format(100*correct_individual/len(test_set)))
        print('Match accuracy: {:.2f}%'.format(200*correct_match/len(test_set)))


    def classify(self, chatlog, duration, extra, selected_feats, prob=False):
        features = self.get_features(chatlog, duration, extra, selected_feats)
        if prob:
            return self.classifier.prob_classify(features)
        else: 
            return self.classifier.classify(features)