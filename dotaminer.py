from scrape import scrape

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--scrape', type=int, help="Scrape given amount of matches")
args = parser.parse_args()

def main():
    if args.scrape:
        scrape(args.scrape)
    print('klar')

if __name__ == '__main__':
    main()