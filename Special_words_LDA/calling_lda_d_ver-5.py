# to call lda for non uniform

import os
import sys
import itertools
import time 

t1=time.time()
#l= [0.02,0.02,0.02]

#l_per = list(set(list(itertools.permutations(l))))

l_per = []

   


eta_2 =  0.2 #float(sys.argv[1]) # Non special word ; eta_! : special word

eta_1_start = 1 # int(sys.argv[2])
eta_1_end =  2 #int(sys.argv[3])
#for i,tag in enumerate(['PER', 'LOC','ORG'],1):
#for i,tag in enumerate(['PER_LOC', 'PER_ORG', 'LOC_ORG','PER_LOC_ORG'],1):
#setup = 'uniform_checking_title_%0.1f' %(eta_2)
#fsp_file = 'uniform/checkin_model_0.20/checking_model_title_0.20' 
#finp_file = 'filtered_event_new2.pkl'

#setup = 'uniform_checking_title_%0.1f' %(eta_2)
#fsp_file = 'uniform/checkin_model_0.20/checking_model_title_0.20' 
#finp_file = 'filtered_event_new2.pkl'
k = 40
no_of_topic = 53
did = 'Dataset-1'
setup = 'title_content_ief_top_%d_per_loc_org_keywords_eta2_%0.1f' %(k,eta_2) #'title_ief_top_%d_per_loc_org_keywords_eta2_%0.1f' %(k,eta_2)
for temp_eta1 in range(eta_1_start, eta_1_end):
    eta_1 = temp_eta1 * 0.1
    #fsp_file = 'uniform/title_0.10/PER_LOC_ORG_KEYWORDS_0.10'
    fsp_file  = 'uniform/title_content_ief_top_%d/tf_ief_term_ief_weight_%0.2f' %(k,eta_1)
    #fsp_file = 'uniform/title_ief_top_%d/term_ief_weight_%0.2f' %(k,eta_1)
    finp_file = 'restoredDate_filtered_event_new_v.2_0_900.pkl'

    iter_count = 5
    #cmd = 'python make_special_word.py -f filtered_event_new2.pkl --per=%0.1f --loc=%0.1f --org=%0.1f' %(cur_l)
    #cmd = 'python lda_d_ver-1.py   --alpha=0.1 --eta1=0.2 --eta2=0.4  --fin=%s --fsp=%s -s -i %d' %(finp_file, fsp_file, iter_count) 
    cmd = 'python lda_d_ver-1.py   --alpha=0.1  --eta2=%0.1f --fin=%s --fsp=%s -s -i %d --dp=%s --setup=%s --datasets=%s -k %d' %(eta_2,finp_file, fsp_file, iter_count,'uniform',setup, did, no_of_topic ) 

    print ' ##:', cmd
    os.system(cmd)


t2 =time.time()

print 'Total time taken :' , (t2-t1)
