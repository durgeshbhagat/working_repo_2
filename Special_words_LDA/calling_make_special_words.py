# Aprogram to call make_special_word.py with differenet parameter 



import os
import sys
import itertools

#l= [0.02,0.02,0.02]

#l_per = list(set(list(itertools.permutations(l))))

l_per = []
for i in range(1,6):
    l_per.append(0.1*i)    
entity =sys.argv[1]    
for cur_l in l_per:
    #cmd = 'python make_special_word_2.py -f filtered_event_new2.pkl --per=%0.2f --loc=%0.2f --org=%0.2f --dp=%s --setup=%s' %(cur_l,'uniform','PER')
    #cmd = 'python make_special_word_2.py -f filtered_event_new2.pkl --per=%0.2f  --dp=%s --setup=%s' %(cur_l,'uniform','PER')
    cmd = 'python make_special_word_2.py -f filtered_event_new2.pkl --entity_weight=%0.2f  --dp=%s --setup=%s' %(cur_l,'uniform',entity)
    print cmd
    os.system(cmd)
