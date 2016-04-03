import nltk;
from nltk.sentiment.vader import SentimentIntensityAnalyzer;
import csv;
import collections;
import random;
import operator;
import os
import json
# failed attempts to fix:
# nltk.download('all') # run this in heroku python terminal
#nltk.data.path.append('./nltk_data/') # fix for heroku??

dictionary = {} # depreciated global
sentences = []

#Read csv and create list from it
def getSentences():
	global sentences;
	currdir = os.path.dirname(os.path.realpath(__file__))
	with open(currdir + '/quotes.csv', 'rb') as csvfile:
		r = csv.reader(csvfile);
		for line in r:
			quote = line[0];
			#line.replace("'", "'")
			sentences.append(quote);
	return sentences;

#Create a dictionary with tokens from each quote
def getQuoteSubject():
	global dictionary;
	global sentences;

	sid = SentimentIntensityAnalyzer();
	for sentence in sentences:
		#Sentiment analysis
		'''
		print sentence;
		ss = sid.polarity_scores(sentence);
		for k in sorted(ss):
			print('{0}: {1}'.format(k, ss[k]));
		print;
		'''

		#Get tokens in quote
		tokens = nltk.word_tokenize(sentence);
		#Get parts of speech of each token
		tagged = nltk.pos_tag(tokens);
		#Keep track of what's been added already
		added = [];

		for t in tagged:
			tnew = (unicode(t[0], errors='ignore'), t[1])
			t = tnew
			#If not yet added and a signifcant token (e.g. not a punctuation mark, not a letter, etc.)
			if len(t[0]) > 1 and t[0].lower() not in added:
				#If the token isn't in the dictionary yet, add it
				if t[0] not in dictionary:
					temp = [];
					try:
						temp.append(unicode(sentence, errors='ignore'))
					except:
						print sentence
					dictionary[t[0]] = temp;
				#If it's already in the dictionary, append it to the list of quotes associated with it
				else:
					temp = dictionary[t[0]];
					
					try:
						temp.append(unicode(sentence, errors='ignore'));
					except:
						print sentence
					dictionary[t[0]] = temp;

				added.append(t[0].lower());
	# save it as output json, so we only need to run this whenever we update quote db
	with open('quotedict.json', 'w') as fp:
		json.dump(dictionary, fp)

#If you want an ordered dictionary to print quotes into a new csv file ordered by token
#NOTE: repeats possible
def printOrderedDict():
	global dictionary;

	od = collections.OrderedDict(sorted(dictionary.items()));
	with open('ordered_quotes.csv', 'wb') as csvfile2:
		w = csv.writer(csvfile2);
		for k, v in od.iteritems(): w.writerow(v);

#Given tags and probabilities of a picture, find a quote which has the most tokens matching 
#the tags, weighting for probability of the tag being correct
def findQuoteFromTag(tags, probabilities):
	global sentences;
	currdir = os.path.dirname(os.path.realpath(__file__))
	with open(currdir + '/quotedict.json') as data_file:    
		dictionary = json.load(data_file)
	# print type(dictionary)


	#List of possible quotes to use
	possible_quotes = [];

	#Number of tags times the probability of each tag for each possible quote
	#The quote with the highest count will be used
	counts = [];

	#Go through all the tags
	for i in range(0, len(tags)):
		tag = tags[i];
		#If it's in the dictionary, that means there is at least one quote that has that token.
		#All quotes with this token are now possibilities for this image
		if tag in dictionary.keys():
			quotes = dictionary[tag];
			#Get all quotes with this token
			for quote in quotes:
				#Add to the list of possible quotes if it's not already there
				if quote not in possible_quotes:
					possible_quotes.append(quote);
					#Initialize it with a count of 1 times the probability of the tag being correct
					counts.append(1 * probabilities[i]);
				#If it's already in the list of possible quotes, increase its count by 
				#1 times the probability of this tag being correct
				else:
					index = possible_quotes.index(quote);
					counts[index] += 1 * probabilities[i];

	#If there's at least one possible quote, return the one with the highest count
	if len(possible_quotes) > 0:
		index, value = max(enumerate(counts), key=operator.itemgetter(1));
		return possible_quotes[index];

	#If there aren't any matching quotes, return a random one!
	else:
		index = random.randint(0, len(sentences) - 1);
		return sentences[index];

#Yay main method!
def generateQuote(tags, probabilities):
	#Read in csv of quotes
	getSentences();
	#Get the tokens of each quote and create dictionary
	# getQuoteSubject(); # only need to run once now
	#Given a picture's tags, return a quote with as many matching tags (weighted by probability) as possible
	# print findQuoteFromTag(tags, probabilities);
	return findQuoteFromTag(tags, probabilities);
generateQuote(["small", "apple", "duck"], [.1, .9, .3]);