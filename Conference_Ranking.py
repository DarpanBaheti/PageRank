import cPickle
import sqlite3
import time
import operator

conn=sqlite3.connect("Paper_db")
db=conn.cursor()

def main():
	print "SQL query: "
	sql = "select id,pub_venue from papers"
	t=time.time()
	db.execute(sql);
	qry=db.fetchall();
	tn =str(round(time.time() - t,2));
	print "Execute in "+str(tn)+" seconds."
	page_ranks=cPickle.load(open('page_ranks','r'))
	conf_rank_dict=cPickle.load(open('Dict/conf_rank_dict','r'))
	conf_paper_count=cPickle.load(open('Dict/conf_paper_count','r'))
	for i in qry:
		conf_rank_dict[i[1]]+=page_ranks[i[0]]/conf_paper_count[i[1]]
	print "DONE"
	s=0
	for i in conf_rank_dict:
		if s<conf_rank_dict[i]:
			s=conf_rank_dict[i]
	for i in conf_rank_dict:
		conf_rank_dict[i]/=s		
	cPickle.dump(conf_rank_dict,open('conf_rank_dict','wb'))
	sorted_conf_rank=sorted(conf_rank_dict.items(), key=operator.itemgetter(1), reverse=True)
	top=[]
	n=input("Enter the number of top conferences: ")
	for i in xrange(n):
		top.append(sorted_conf_rank[i][0])
	print "######################################"
	print  "             TOP CONFERENCES"
	print "######################################"
#top_final=[]
	count=1
	for i in top:
		print str(count)+".) "+str(i)
		count+=1
if __name__ == '__main__':
			main()			