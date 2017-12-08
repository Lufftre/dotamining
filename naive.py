from nltk import NaiveBayesClassifier, word_tokenize

class NaiveBoi(NaiveBayesClassifier):
    def __init__(self):
        self.vocabulary = []
    
    def train(self, corpus):
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

        all_words = {}
        for chatlog, outcome in train_set:
            for word in word_tokenize(chatlog):
                all_words[word.lower()] = all_words.get(word.lower(), 0) + 1
        self.vocabulary = [word for word,n in all_words.items() if n>2]
        # all_words = set(word.lower() for passage in train_set for word in nltk.word_tokenize(passage[0]))
        t = [({word: (word in word_tokenize(x[0])) for word in self.vocabulary}, x[1]) for x in train_set if x[0] in self.vocabulary]
        self.classifier = NaiveBayesClassifier.train(t)  
    
    def classify(self, chatlog):
        chatfeats = {word.lower(): (word in word_tokenize(chatlog.lower())) for word in self.vocabulary}
        return self.classifier.classify(chatfeats)
