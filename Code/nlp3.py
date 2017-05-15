import nltk
import csv, time
from nltk.corpus import wordnet as wn
from nltk.tag.stanford import StanfordPOSTagger
import threading
from multiprocessing.dummy import Pool as ThreadPool





def main(start, stop):
	start_time = time.time()
	print 'start stop = ', start, stop

	stanford_dir = '.\data\stanford-postagger-full-2015-04-20\\'
	modelfile = stanford_dir + 'models\english-bidirectional-distsim.tagger'
	jarfile = stanford_dir + 'stanford-postagger.jar'

	tagger = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)

	# sentence = 'How can I increase the speed of my internet connection while using a VPN?'
	# print tagger.tag(sentence.split())

	# for word, tag in tagger.tag(nltk.word_tokenize(sentence)):
	# 	print 'word: ',word,'\ttag: ',tag

	count = 0
	real_matches = 0
	correct_matches = 0
	wrong_matches = 0
	with open(".\data\quora_duplicate_questions.tsv") as tsvfile:
	    tsvreader = csv.reader(tsvfile, delimiter="\t")
	    #print 'inside thread call....start = ',start,"\tstop = ",stop
	    #print 'inside run = ', (stop/100)
	    for line in tsvreader:

	    	count = count + 1
	    	#print 'count = ', count 

	    	if count<start:
	    		continue

	    	if count>stop:
	    		break

	    	print "-------------------------------"
	    	print "count: ", count
	    	print "-------------------------------"
	    	duplicate = line[5]
	    	print'duplicate',duplicate
	    	if (duplicate == '1'):
	    		real_matches = real_matches + 1

	    	q1 = tagger.tag(nltk.word_tokenize(line[3].lower()))
	    	q2 = tagger.tag(nltk.word_tokenize(line[4].lower()))

	    	q1_nouns = dict()
	    	for word, tag in q1:
	    		if tag[:2] == 'NN':
	    			q1_nouns[word] = 1

	    	q2_nouns = dict()
	    	for word, tag in q2:
	    		if tag[:2] == 'NN':
	    			q2_nouns[word] = 1

	    	print 'nouns q1: ', q1_nouns,'\tnouns q2: ', q2_nouns

	    	noun_match = False
	       	for key, value in q1_nouns.items():
	       		if (key in q2_nouns):
	       			noun_match = True
	       			break
	       	print 'noun_match: ', noun_match
	       	if (noun_match):
	       		q1_verbs = dict()
	       		for word, tag in q1:
	       			if tag[:2] == 'VB':
	       				q1_verbs[word] = 1

	       		q2_verbs = dict()
	       		for word, tag in q2:
	       			if tag[:2] == 'VB':
	       				q2_verbs[word] = 1

	       		print 'verbs q1: ',q1_verbs,'\tverbs q2: ', q2_verbs

	       		verb_match = False

	       		if len(q1_verbs) == 0 or len(q2_verbs) == 0:
	       			verb_match = True
	       			continue

	       		for key, value in q1_verbs.items():
	       			if (key in q2_verbs):
	       				verb_match = True
	       				break
	       			if (verb_match == False and len(wn.synsets(key))>0):
	       				syn = wn.synsets(key)[0]
	       				for lemma in syn.lemmas():
	       					print 'synonym of ', key, ": ", lemma.name()
	       					if (lemma.name() in q2_verbs):
	       						verb_match = True
	       						break

	       		if (verb_match == False) :
		       		for key, value in q2_verbs.items():
		       			if (key in q1_verbs):
		       				verb_match = True
		       				break
		       			if (verb_match == False and len(wn.synsets(key))>0):
		       				print key
		       				syn = wn.synsets(key)[0]
		       				for lemma in syn.lemmas():
		       					print 'synonym of ', key, ": ", lemma.name()
		       					if (lemma.name() in q1_verbs):
		       						verb_match = True
		       						break

	       		if (verb_match):
	       			#print ' '
	       			if (line[5] == '1'):
	       				print 'DUPLICATE'
	       				correct_matches = correct_matches + 1;
	       			else:
	       				print 'DUPLICATE BUT WRONG!!!!!'
	       				wrong_matches = wrong_matches + 1;


	print 'correct_matches : ', correct_matches
	print 'wrong_matches : ', wrong_matches
	print 'real_matches : ', real_matches

	print('\n\nrun time : ', time.time() - start_time)









try:	
	main(2, 21)
except:
   print "Error: unable to start thread"
