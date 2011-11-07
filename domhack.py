#~/usr/bin/python

#domhack.py - multithreaded whois search of all possible alpha combinations of a particular tld
#Nov 2011 - twitter.com/xlfe

tld='mu'
threads=5

from pywhois import whois
from sys import argv
from multiprocessing import Process,Queue
from random import randint
from string import lowercase

def iter_alpha(root='',length=2):
	for c in lowercase:
		a = ''.join([root,c])
		if length>1:
			for i in iter_alpha(a,length-1):
				yield i
		else:
			yield a

def check_domain(domains,rq):

	for d in domains:
		w = whois(d)
		rq.put([w.domain_name,w.status,d])

if __name__ == '__main__':
	
	domains = ['{0}.{1}'.format(i,tld) for i in iter_alpha()]
	domain_count = len(domains)
	q = Queue()
	d_threads=[]

	for i in range(0,threads-2):
		dpt = domain_count / threads
		dt = []
		while dpt > 0:
			dt.append(domains.pop(randint(0,len(domains)-1)))
			dpt=dpt-1
		d_threads.append(dt)
	d_threads.append(domains)		

	for t in d_threads:
		t = Process(target=check_domain,args=(t,q,))
		t.start()
	
	while domain_count > 0:
		w= q.get(block=True,timeout=10)
		if len(w[0]) ==0:
			w[0]=w[2]
		print '{0}:{1}'.format(w[0],w[1])
	
	
