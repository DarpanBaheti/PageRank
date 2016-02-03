import sqlite3
import cPickle
from collections import defaultdict
import operator
import unicodedata

page_ranks=cPickle.load(open('page_ranks','r'))
conf_rank_dict=cPickle.load(open('conf_rank_dict','r'))
author_paper_count=cPickle.load(open('Dict/author_paper_count','r'))
paper_author=cPickle.load(open('Dict/paper_author','r'))
paper_conf=cPickle.load(open('Dict/paper_conf','r'))

author_rank_dict=defaultdict(float)
for i in author_paper_count:
	author_rank_dict[i]=0.0

print "Data Loaded Press Enter to continue"
raw_input()
#conn=sqlite3.connect('Paper_db')
#db=conn.cursor()
#sql='select id,pub_venue from papers'
#db.execute(sql)
#query=db.fetchall()
#print "query DONE"
count=1
for paper in page_ranks:
	#print count
	count+=1
	authors=paper_author[paper]
	paper_rank=page_ranks[paper]
	conference=paper_conf[paper]
	conference_rank=conf_rank_dict[conference]
	for author in authors:
		#print author
		author_uni=unicodedata.normalize('NFKD',author).encode('ascii','ignore')
		#print authors
		#print author_uni
		#print author_uni in author_paper_count
		#print author_paper_count[author_uni]
		author_rank_dict[author_uni]+=(paper_rank*conference_rank)/author_paper_count[author_uni]

cPickle.dump(author_rank_dict,open('author_rank_dict','wb'))
print "Authors Rated"
n=input("No of Top Authors: ")

sorted_authors=sorted(author_rank_dict.items(), key=operator.itemgetter(1), reverse=True)
print "#######################################################################################################################################"
print "                                                    TOP AUTHORS"
print "#######################################################################################################################################"
for i in xrange(n):
	print str(i+1)+".) "+sorted_authors[i][0]+" ( Score: "+str(sorted_authors[i][1])+")"