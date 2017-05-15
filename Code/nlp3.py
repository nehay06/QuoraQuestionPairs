import nltk
import csv, time
from nltk.corpus import wordnet as wn
from nltk.tag.stanford import StanfordPOSTagger
import threading
from multiprocessing.dummy import Pool as ThreadPool





def main(start, stop):
	start_time = time.time()
	print 'start stop = ', start, stop

	stanford_dir = 'C:\Users\Arunima Chaudhary\Desktop\NLP Project\stanford-postagger-full-2015-04-20\\'
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
	with open("C:\Users\Arunima Chaudhary\Downloads\quora_duplicate_questions.tsv") as tsvfile:
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

	# stanford_dir = 'C:\Users\Arunima Chaudhary\Desktop\NLP Project\stanford-postagger-full-2015-04-20\\'
	# modelfile = stanford_dir + 'models\english-bidirectional-distsim.tagger'
	# jarfile = stanford_dir + 'stanford-postagger.jar'

	# tagger = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)
	# q1 = 'What is the step by step guide to invest in share market?'
	# q2 = 'What is the step by step guide to invest in share market in india?'

	# q1_tags = tagger.tag(nltk.word_tokenize(q1))
	# q2_tags = tagger.tag(nltk.word_tokenize(q2))

	# q1_nouns = dict()
	# q1_verbs = dict()
	# for word, tag in q1_tags:
	# 	if tag[:2] == 'NN':
	# 		q1_nouns[word] = 1
	# 	if tag[:2] == 'VB':
	# 		q1_verbs[word] = 1

	# q2_nouns = dict()
	# q2_verbs = dict()
	# for word, tag in q1_tags:
	# 	if tag[:2] == 'NN':
	# 		q2_nouns[word] = 1
	# 	if tag[:2] == 'VB':
	# 		q2_verbs[word] = 1

	# print q1_nouns
	# print q1_verbs
	# print q2_nouns
	# print q2_verbs

	main(2, 21)

# 	start_num = []
# 	stop_num = []
# #2425743
# 	for i in range(0, 2426):
# 		if i == 0:
# 			start_num.append(2)
# 		else:
# 			start_num.append(i*1000)

# 		if i == 2425:
# 			stop_num.append(2425743)
# 		else:
# 			stop_num.append((i+1)*1000)

# 	print start_num
# 	print stop_num
# 	# start_num = [2,101,201,301,401,501,61,701,801,901]
# 	# stop_num = [100,200,300,400,500,600,700,800,900,1000]

# 	thread_list = []

# 	wn.ensure_loaded() 

# 	for i in range(0, 2426):
# 	    # Instantiates the thread
# 	    t = threading.Thread(target=main, args=(start_num[i],stop_num[i],))
# 	    # Sticks the thread in a list so that it remains accessible
# 	    print 'thread ',i
# 	    thread_list.append(t)

# 	for thread in thread_list:
# 		print 'starting thread'
# 		thread.start()

# 	for thread in thread_list:
# 		thread.join()

# 	print 'Done'

except:
   print "Error: unable to start thread"