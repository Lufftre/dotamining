# Dota mining
Predict game winner using a Naive Bayes classifier.  
With a corpus size of 3963 matches it achieves a performance of:  

Individual accuracy: 64.13%  
Match accuracy: 74.52%  

## Scraping
The match data used is provided by [opendota.com](https://www.opendota.com).

## Available parameters
* ```-s N```, ```--scrape N```  
Extend corpus with N new matches
* ```-t```, ```--train```  
Train the classifier using the updated corpus
* ```-c CORPUS```, ```--corpus CORPUS```  
Path to pickle file of corpus. Deafult: corpus.p
* ```-l CLASSIFIER```, ```--classifier CLASSIFIER``` 
Path to pickle file of classifier. Deafult: classifier.p
### Features
* ```--unigram```
* ```--bigram```
* ```--trigram```
* ```--wp30```  
Words per 30 minutes
* ```--sdi```  
Shannon Diversity Index

### Extras
* ```--fourgram```
* ```--fivegram```

 ## Baseline example
```python3 dotaminer.py --train --unigram```
 
 ## Complete system example
```python3 dotaminer.py --train --unigram --bigram --trigram --wp30 --sdi```
 
