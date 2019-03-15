
import os
import sys
import itertools
import time 

t1=time.time()
#l= [0.02,0.04,0.06]

i = 1 # int(sys.argv[1])
alpha = [0.1, 0.1, 0.1] # [ dataset-1, dataset-2, datset-3]
eta = [0.2, 0.2, 0.2]  # [ dataset-1, dataset-2, dataset-3]
dataset = ['Dataset-1' , 'Dataset-2' , 'Dataset-3']
#finp_file =  #'filtered_event_new2.pkl'
finp_file = ['restoredDate_filtered_event_new_v.2_0_900.pkl', 'Reuter-21578-R-8/Reuter-21578_r-8-train_no_stop.pkl', '20-Newsgroup/20-Newsgroup_all_term.pkl']  #'filtered_event_new2.pkl'
iter_count = 120

no_of_topic = 8

cmd = 'python lda_d.py     --alpha=%0.2f --eta=%0.2f --dataset=%s -f %s -s -i %d -k %d' %(alpha[i], eta[i], dataset[i], finp_file[i], iter_count, no_of_topic) 
print(cmd)
os.system(cmd)


t2 =time.time()

print('Total time taken :' , (t2-t1))
