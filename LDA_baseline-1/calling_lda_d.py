
import os
import sys
import itertools
import time 

t1=time.time()
#l= [0.02,0.04,0.06]

#l_per = list(set(list(itertools.permutations(l))))
alpha = [round(x * 0.1,2) for x in range(1, 5)]#0.1
eta = [round(x * 0.1,2) for x in range(1, 5)] #0.4
print alpha
print eta
alpha_eta = list(itertools.product(alpha,eta))
print alpha_eta , len(alpha_eta)


finp_file = '20-Newsgroup/20-Newsgroup_all_term.pkl' #'filtered_event_new2.pkl'
finp_file = 'filtered_event_new2.pkl'
#finp_file = 'Reuter-21578-R-8/Reuter-21578_r-8-train_no_stop.pkl' #'filtered_event_new2.pkl'
iter_count = 100
start = int(raw_input('Enter the start index : '))
end = int(raw_input('Enter the end index : '))
for i,cur_item in enumerate(alpha_eta[start:end],start):
    cur_alpha = cur_item[0]
    cur_eta = cur_item[1]
    #fsp_file = 'per_%0.2f_loc_%0.2f_org_%0.2f' %(cur_l)
   
    #cmd = 'python make_special_word.py -f filtered_event_new2.pkl --per=%0.1f --loc=%0.1f --org=%0.1f' %(cur_l)
    #cmd = 'python lda_d.py   --alpha=%0.2f --eta=%0.2f  -f %s -s -i %d' %(cur_alpha, cur_eta, finp_file, iter_count) 
    cmd = 'python lda_d.py   --alpha=%0.2f --eta=%0.2f  -f %s -s -i %d' %(cur_alpha, cur_eta, finp_file, iter_count) 
    print ' ##:', i, cmd
    os.system(cmd)


t2 =time.time()

print 'Total time taken :' , (t2-t1)
