import pickle
import os
from scrape import scrape
from naive import NaiveBoi

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--scrape', type=int, help="Scrape given amount of matches")
parser.add_argument('-t', '--train', action='store_true', help="Train classifier")
parser.add_argument('-c', '--corpus', default='corpus.p', help="Corpus to use")
parser.add_argument('-l', '--classifier', default='classifier.p', help="Classifier to use")
parser.add_argument('chatlogs', nargs='*', help="Chat to classify")

args = parser.parse_args()

def main():
    corpus = pickle.load(open(args.corpus, 'rb')) if os.path.isfile(args.corpus) else []
    if args.scrape:
        updated_corpus = scrape(args.scrape, corpus=corpus)
        pickle.dump(updated_corpus, open(args.corpus, 'wb'))
        print(len(updated_corpus))
    
    naiveBoi = pickle.load(open(args.classifier, 'rb')) if os.path.isfile(args.classifier) else NaiveBoi()
    if args.train:
        naiveBoi.train(corpus)
        pickle.dump(naiveBoi, open(args,classifier, 'wb'))
    
    if args.chatlogs:
        for chatlog in args.chatlogs:
            print(naiveBoi.classify(chatlog))

if __name__ == '__main__':
    main()