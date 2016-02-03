import cPickle
from collections import defaultdict
import operator

print "Initialising Dictionaries from Pickles"
update_page_rank=defaultdict(float)

page_ranks=cPickle.load(open('Dict/page_ranks','r'))
inlinks_dict=cPickle.load(open('Dict/inlink_dict','r'))
outlink_count_dict=cPickle.load(open('Dict/outlink_count_dict','r'))

theta=0.86

print "Initialising"

iteration=0

while True:
	flag=True
	print "iteration: "+str(iteration+1)
	iteration+=1
	for paper in  page_ranks:
		current_score=page_ranks[paper]
		if paper in inlinks_dict:
			inlink_list=inlinks_dict[paper]
			new_score=0.0
			for each_inlink in inlink_list:
				if each_inlink in page_ranks:
					new_score+=(page_ranks[each_inlink])/(outlink_count_dict[each_inlink])
			new_score=(1-theta)+theta*new_score
		#new_score+=0.15/1632442
			if abs(current_score-new_score)>0.0000001:
				flag=False
			update_page_rank[paper]=new_score

	if flag==True:
		break
	for paper in page_ranks:
		page_ranks[paper]=update_page_rank[paper]
	if iteration%100==0:
		print "Saving Current Ranks"
		cPickle.dump(page_ranks,open('current_ranks','wb'))
	del(update_page_rank)
	update_page_rank=defaultdict(float)
max_score=0

for paper in page_ranks:
	if max_score<page_ranks[paper]:
		max_score=page_ranks[paper]
for paper in page_ranks:
	page_ranks[paper]/=max_score		
print "Done"

cPickle.dump(page_ranks,open('page_ranks','wb'))

print
print "DONE !!! PAGERANKED SUCCESSFULLY!"	

