import subprocess
import sys
from os import close

def test(file_name, term, tally_factor, sa_factor ):
	cmd = ["python3","test.py",file_name, term, str(tally_factor), str(sa_factor)]
	subprocess.check_call(cmd)

species = sys.argv[1]
seq1 = sys.argv[2]
seq2 = sys.argv[3]
seq3 = sys.argv[4]

with open(species+'.csv','w')as f:
	f.write('term,tally_factor,sa_factor,mem,time,found\n')


tally_factors = [8,32,128,512]
sa_factors = [4,16,64,254]
terms = [seq1,seq2,seq3]
print(terms)
for term in terms:
	for tally in tally_factors:
		for sa in sa_factors:
			test(species+'.fa',term,tally,sa)
