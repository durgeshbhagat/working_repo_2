
import os
import sys
import itertools
import time 

t1=time.time()
#l= [0.02,0.02,0.02]

#l_per = list(set(list(itertools.permutations(l))))

l_per = []
for i in range(1,6):
    l_per.append(0.1*i)
    
setup = sys.argv[1]
eta_2 = float(sys.argv[2])
for i,cur_l in enumerate(l_per,1):
    fsp_file = 'uniform/PER_%0.2f/per_%0.2f' %(cur_l,cur_l)
    finp_file = 'filtered_event_new2.pkl'
    iter_count = 100
    #cmd = 'python make_special_word.py -f filtered_event_new2.pkl --per=%0.1f --loc=%0.1f --org=%0.1f' %(cur_l)
    #cmd = 'python lda_d_ver-1.py   --alpha=0.1 --eta1=0.2 --eta2=0.4  --fin=%s --fsp=%s -s -i %d' %(finp_file, fsp_file, iter_count) 
    cmd = 'python lda_d_ver-1.py   --alpha=0.1  --eta2=%0.1f --fin=%s --fsp=%s -s -i %d --dp=%s --setup=%s' %(eta_2,finp_file, fsp_file, iter_count,'uniform',setup ) 

    print ' ##:', i, cmd
    os.system(cmd)


t2 =time.time()

print 'Total time taken :' , (t2-t1)
