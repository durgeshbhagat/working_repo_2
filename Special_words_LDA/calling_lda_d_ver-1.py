
import os
import sys
import itertools
import time 

t1=time.time()
l= [0.02,0.04,0.06]

l_per = list(set(list(itertools.permutations(l))))

for i,cur_l in enumerate(l_per,1):
    fsp_file = 'per_%0.2f_loc_%0.2f_org_%0.2f' %(cur_l)
    finp_file = 'filtered_event_new2.pkl'
    iter_count =100
    #cmd = 'python make_special_word.py -f filtered_event_new2.pkl --per=%0.1f --loc=%0.1f --org=%0.1f' %(cur_l)
    cmd = 'python lda_d_ver-1.py   --alpha=0.1 --eta1=0.2 --eta2=0.4  --fin=%s --fsp=%s -s -i %d' %(finp_file, fsp_file, iter_count) 

    print ' ##:', i, cmd
    os.system(cmd)


t2 =time.time()

print 'Total time taken :' , (t2-t1)
