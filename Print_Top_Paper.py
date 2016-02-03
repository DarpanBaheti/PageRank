import cPickle
import sqlite3
import operator
page_rank_dict=cPickle.load(open('page_ranks','r'))
sorted_page_rank = sorted(page_rank_dict.items(), key=operator.itemgetter(1), reverse=True)
top=[]
n=input("Enter the number of top papers: ")
for i in xrange(n):
	top.append(sorted_page_rank[i][0])

conn=sqlite3.connect('Paper_db')
db=conn.cursor()
print "######################################"
print  "             TOP PAPERS"
print "######################################"
#top_final=[]
#for i in top:
#	top_final.append(str(i))
#ids=','.join(top_final)	
for i in xrange(n):
	sql='select title,year,authors,id from papers where id='+str(top[i])
	db.execute(sql)
	query=db.fetchall()
	print str(i+1)+".) "+str(query[0][0])+" ( "+str(query[0][1])+" ) by: "+str(query[0][2])+" Score : "+str(page_rank_dict[query[0][3]])