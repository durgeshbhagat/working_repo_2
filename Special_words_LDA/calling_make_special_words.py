# Aprogram to call make_special_word.py with differenet parameter 



import os
import sys
import itertools

l= [0.02,0.04,0.06]

l_per = list(set(list(itertools.permutations(l))))

for cur_l in l_per:
    cmd = 'python make_special_word.py -f filtered_event_new2.pkl --per=%0.2f --loc=%0.2f --org=%0.2f' %(cur_l)
    print cmd
    os.system(cmd)
