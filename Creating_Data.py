import cPickle
import sqlite3
from collections import defaultdict
import time
import unicodedata

conn=sqlite3.connect("Paper_db")
db=conn.cursor()

def inversedictionary(d):
	inversedict={}
	for i,j in d.iteritems():
		keys=inversedict.setdefault(j,[])
		keys.append(i)
	return inversedict	

def main():
	print "SQL query: "
	sql = "select id,ref_id,pub_venue,year,authors from papers"
	t=time.time()
	db.execute(sql);
	qry=db.fetchall();
	tn =str(round(time.time() - t,2));
	print "Execute in "+str(tn)+" seconds."
	outlink_count_dict=defaultdict(int)
	inlinks_count_dict=defaultdict(int)
	outlink_dict={}
	paper_year={}
	inlink_dict=defaultdict(list)
	page_ranks=defaultdict(float)
	conf_paper_count=defaultdict(int)
	conf_rank_dict=defaultdict(float)
	paper_conf={}
	year_paper_count=defaultdict(int)
	year_citation_count=defaultdict(int)
	avg_year_citation_count=defaultdict(float)
	paper_author=defaultdict(list)
	author_paper_count=defaultdict(int)

	count=0
	for i in qry:
		conf_paper_count[i[2]]+=1
		paper_conf[i[0]]=i[2]
		page_ranks[i[0]]=1.0 #/1632442.0 #NEDD TO CHANGE TO NUMBER OF PAPERS
		outlink_dict[i[0]]=str(i[1])
		inlinks_count_dict[i[0]]=0
		outlink_count_dict[i[0]]=len(str(i[1]).split(";"))
		paper_year[i[0]]=i[3]
		paper_author[i[0]]=i[4].split(',')
	for i in qry:
		for j in str(i[1]).split(";"):
			if j!='' and int(j) in inlinks_count_dict:
				inlinks_count_dict[int(j)]+=1
				inlink_dict[int(j)].append(i[0])
	for i in conf_paper_count:
		conf_rank_dict[i]=0.0
	for paper in page_ranks:
		year=paper_year[paper]
		year_citation_count[year]+=outlink_count_dict[paper]
		year_paper_count[year]+=1
	for year in year_citation_count:
		avg_year_citation_count[year]=(year_citation_count[year]*1.0)/year_paper_count[year]
	for paper in paper_author:
		authors=paper_author[paper]
		for author in authors:
			author_uni=unicodedata.normalize('NFKD',author).encode('ascii','ignore')
			author_paper_count[author_uni]+=1

	cPickle.dump(page_ranks,open('Dict/page_ranks','wb'))
	cPickle.dump(outlink_dict,open('Dict/outlink_dict','wb'))
	cPickle.dump(outlink_count_dict,open('Dict/outlink_count_dict','wb'))
	cPickle.dump(inlink_dict,open('Dict/inlink_dict','wb'))
	cPickle.dump(inlinks_count_dict,open('Dict/inlinks_count_dict','wb'))
	cPickle.dump(conf_paper_count,open('Dict/conf_paper_count','wb'))
	cPickle.dump(conf_rank_dict,open('Dict/conf_rank_dict','wb'))
	cPickle.dump(paper_year,open('Dict/paper_year','wb'))
	cPickle.dump(avg_year_citation_count,open('Dict/avg_year_citation_count','wb'))
	cPickle.dump(year_paper_count,open('Dict/year_paper_count','wb'))
	cPickle.dump(year_citation_count,open('Dict/year_citation_count','wb'))
	cPickle.dump(paper_author,open('Dict/paper_author','wb'))
	cPickle.dump(author_paper_count,open('Dict/author_paper_count','wb'))
	cPickle.dump(paper_conf,open('Dict/paper_conf','wb'))
	print "Saving Em ALL"
	print len(inlinks_count_dict)			
	conn.commit()
	db.close()

if __name__ == '__main__':
	main()