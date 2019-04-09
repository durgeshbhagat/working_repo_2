
import os
import sys
import itertools
import time 

t1=time.time()
#l= [0.02,0.04,0.06]

i = 2 #int(sys.argv[1])
j = 0
alpha = [0.1, 0.1, 0.1] # [ dataset-1, dataset-2, datset-3]
eta1 = [0.1, 0.2, 0.1]  # [ dataset-1, dataset-2, dataset-3]
eta2 = [0.2, 0.3, 0.2]  # [ dataset-1, dataset-2, dataset-3]
dataset = ['Dataset-1' , 'Dataset-2' , 'Dataset-3']

setup_list= ['ner_keywords', 'tf-df-ief', 'IG']
#finp_file =  #'filtered_event_new2.pkl'
finp_file = ['restoredDate_filtered_event_new_v.2_0_900.pkl', 'Reuter-21578-R-8/Reuter-21578_r-8-train_no_stop.pkl', '20-Newsgroup/20-Newsgroup_all_term.pkl']  #'filtered_event_new2.pkl'
iter_count = 120

topic_list = [53, 8, 20]

no_of_topic = topic_list[i]
setup = setup_list[j]

cmd = 'python guided-lda_d.py  --alpha=%0.2f --eta1=%0.2f --eta2=%0.2f --dataset=%s --setup=%s -f %s -s -i %d -k %d' %(alpha[i], eta1[i], eta2[i], dataset[i], setup, finp_file[i], iter_count, no_of_topic)
print  (cmd)
os.system(cmd)


t2 =time.time()

print('Total time taken :' , (t2-t1))
