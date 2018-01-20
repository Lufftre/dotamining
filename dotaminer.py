import pickle
import os
from scrape import scrape
from naive import NaiveBoi

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--scrape', type=int, help="Scrape given amount of matches")
parser.add_argument('-t', '--train', action='store_true', help="Train classifier")
# parser.add_argument('-e', '--test', action='store_true', help="Test classifier")
parser.add_argument('-c', '--corpus', default='corpus.p', help="Corpus to use")
parser.add_argument('-l', '--classifier', default='classifier.p', help="Classifier to use")
parser.add_argument('--unigram', action='store_true', help="Use unigrams")
parser.add_argument('--bigram', action='store_true', help="Use bigrams")
parser.add_argument('--trigram', action='store_true', help="Use trigrams")
parser.add_argument('--fourgram', action='store_true', help="Use fourgrams")
parser.add_argument('--fivegram', action='store_true', help="Use fivegrams")
parser.add_argument('--wp30', action='store_true', help="Use words per 30min")
parser.add_argument('--sdi', action='store_true', help="Use Shannon diversity index")
# parser.add_argument('chatlogs', nargs='*', help="Chat to classify")

args = parser.parse_args()

def main():
    corpus = pickle.load(open(args.corpus, 'rb')) if os.path.isfile(args.corpus) else []
    if args.scrape:
        updated_corpus = scrape(args.scrape, corpus=corpus)
        pickle.dump(updated_corpus, open(args.corpus, 'wb'))
        # print(len(updated_corpus))
    
    print('Documents in corpus:', len(corpus))
    
    naiveBoi = pickle.load(open(args.classifier, 'rb')) if os.path.isfile(args.classifier) else NaiveBoi()

    selected_feats = []
    selected_feats += ['unigram'] if args.unigram else []
    selected_feats += ['bigram'] if args.bigram else []
    selected_feats += ['trigram'] if args.trigram else []
    selected_feats += ['fourgram'] if args.fourgram else []
    selected_feats += ['fivegram'] if args.fivegram else []
    selected_feats += ['wp30'] if args.wp30 else []
    selected_feats += ['sdi'] if args.sdi else []

    train = corpus[:len(corpus)//2]
    test = corpus[len(corpus)//2:]
    if args.train:
        naiveBoi.train(train, selected_feats)
        pickle.dump(naiveBoi, open(args.classifier, 'wb'))
        naiveBoi.test(test, selected_feats)

    #if args.test:

    # for match_id, radiant_win, duration, avg_mmr, chatlog in test:
    #     print(chatlog)
    #     input()
    
    # if args.chatlogs:
    #     for chatlog in args.chatlogs:
    #         print(naiveBoi.classify(chatlog))

if __name__ == '__main__':
    main()