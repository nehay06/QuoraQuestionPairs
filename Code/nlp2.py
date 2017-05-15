import nltk
import csv, time
from nltk.corpus import wordnet as wn

start = time.time()

grammar = "NP: {<DT>?<JJ>*<NN>}"
parser = nltk.RegexpParser(grammar)
count = 0
real_matches = 0
correct_matches = 0
wrong_matches = 0

with open(".\data\quora_duplicate_questions.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
    	if count == 0:
    		count = 1
    		continue

    	if count == 10000:
    		break

    	count = count + 1
    	print "-------------------------------"
    	print "count: ", count
    	print "-------------------------------"
    	duplicate = line[5]
    	print'duplicate',duplicate
    	if (duplicate == '1'):
    		real_matches = real_matches + 1

    	q1_nouns = dict()
    	for word, tag in nltk.pos_tag(nltk.word_tokenize(line[3])):
    		if tag == 'NN' or tag == 'NNP':
    			q1_nouns[word.lower()] = 1

    	q2_nouns = dict()
    	for word, tag in nltk.pos_tag(nltk.word_tokenize(line[4])):
    		if tag == 'NN' or tag == 'NNP':
    			q2_nouns[word.lower()] = 1

    	print 'nouns q1: ', q1_nouns,'\tnouns q2: ', q2_nouns

    	noun_match = False
       	for key, value in q1_nouns.items():
       		if (key in q2_nouns):
       			noun_match = True
       			break

       	if (noun_match):
       		q1_verbs = dict()
       		for word, tag in nltk.pos_tag(nltk.word_tokenize(line[3])):
       			if tag == 'VB' or tag == 'VBP':
       				q1_verbs[word.lower()] = 1

       		q2_verbs = dict()
       		for word, tag in nltk.pos_tag(nltk.word_tokenize(line[4])):
       			if tag == 'VB' or tag == 'VBP':
       				q2_verbs[word.lower()] = 1

       		print 'verbs q1: ',q1_verbs,'\tverbs q2: ', q2_verbs

       		verb_match = False

       		if len(q1_verbs) == 0 or len(q2_verbs) == 0:
       			verb_match = True
       			continue

       		for key, value in q1_verbs.items():
       			if (key in q2_verbs):
       				verb_match = True
       				break
       			if (verb_match == False and len(wn.synsets(key.lower()))>0):
       				syn = wn.synsets(key.lower())[0]
       				for lemma in syn.lemmas():
       					print 'synonym of ', key.lower(), ": ", lemma.name()
       					if (lemma.name() in q2_verbs):
       						verb_match = True
       						break

       		if (verb_match == False) :
	       		for key, value in q2_verbs.items():
	       			if (key in q1_verbs):
	       				verb_match = True
	       				break
	       			if (verb_match == False and len(wn.synsets(key.lower()))>0):
	       				print key.lower()
	       				syn = wn.synsets(key.lower())[0]
	       				for lemma in syn.lemmas():
	       					print 'synonym of ', key.lower(), ": ", lemma.name()
	       					if (lemma.name() in q1_verbs):
	       						verb_match = True
	       						break

       		if (verb_match):
       			print ' '
       			if (line[5] == '1'):
       				print 'DUPLICATE'
       				correct_matches = correct_matches + 1;
       			else:
       				print 'DUPLICATE BUT WRONG!!!!!'
       				wrong_matches = wrong_matches + 1;


print 'correct_matches: ', correct_matches
print 'wrong_matches: ', wrong_matches
print 'real_matches: ', real_matches

print('\n\nrun time: ', time.time() - start)
