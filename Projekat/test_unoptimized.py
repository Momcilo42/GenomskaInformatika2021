import subprocess
import sys
from os import close

def test(file_name, term, tally_factor, sa_factor ):
	cmd = ["python3","test.py",file_name, term, str(tally_factor), str(sa_factor)]
	subprocess.check_call(cmd)

species = ['e_coli','coffea_arabica','mus_pahari']
terms=[['TACGTACG','TCGATGCAG','TGCTGAACAGTC'],['ATGCATG','TCTCTCTA','TTCACTACTCTCA'],['ATGATG','CTCTCTA','TCACTACTCTCA']]

with open('unoptimized.csv','w')as f:
	f.write('term,tally_factor,sa_factor,mem,time,found\n')



for i in range(len(species)):
	for term in terms[i]:
		test(species[i]+'.fa',term,0,0)
