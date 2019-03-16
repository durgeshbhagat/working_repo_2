# to call PKSS-LDA for dataset-2  : Reuter dataset
# last modified : 29th May , 2018
import os
import sys
import itertools
import time 

t1=time.time()

l_per = []

   


#eta_2 = 0.1 # float(sys.argv[1]) # Non special word ; eta_! : special word

eta_1_start = 1 #int(sys.argv[2])
eta_1_end = 6 #int(sys.argv[3])

setup_list = ['ner_keywords', 'tf-df-icf']

k = 40

for temp_eta_2 in range(1,6):
    eta_2 = temp_eta_2 * 0.1
    setup = 'tf-df-ief-%d_eta_2-%0.2f' %(k,eta_2) # 'ner_keywords' # changed Here ! ----
    did = 'Dataset-2'
    no_of_topic = 8

    for eta_1 in range(eta_1_start, eta_1_end):
        temp_eta1 = eta_1* 0.1
        for index, cur_setup in enumerate(setup_list):
            if index == 0:
                fsp_file = '%s/ner_keywords/%s-ner_keyword_%0.1f' % (did, did, temp_eta1)
                setup = 'ner_keywords'
            elif index == 1:
                fsp_file = '%s/tf-df-icf/top-%d/%s-tf-df-icf_weight_%0.2f' % (did, k, did, temp_eta1)
                setup = 'tf-df-icf_top-%d' % (k)

            eta_1 = temp_eta1 * 0.1
            finp_file = 'Reuter-21578-R-8/Reuter-21578_r-8-train_no_stop.pkl'

            iter_count = 100
            cmd = 'python lda_d_ver-1.py   --alpha=0.1 --eta1=%0.2f --eta2=%0.2f --fin=%s --fsp=%s -s -i %d --dp=%s --setup=%s --datasets=%s -k %d' \
                  % (temp_eta1, eta_2, finp_file, fsp_file, iter_count, 'uniform', setup, did, no_of_topic)
            print(' ##:', cmd)
            os.system(cmd)

    t2 = time.time()

    print('Total time taken :', (t2-t1))


