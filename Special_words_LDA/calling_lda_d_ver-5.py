# to call lda for non uniform

import os
import time 

t1 = time.time()
# l = [0.02,0.02,0.02]

# l_per = list(set(list(itertools.permutations(l))))

l_per = []

#eta_2 = 0.1  # float(sys.argv[1]) # Non special word ; eta_1 : special word

eta_2_start = 2
eta_2_end = 3

eta_1_start = 1  # int(sys.argv[2])
eta_1_end = 2  # int(sys.argv[3])

setup_list = ['ner_keywords', 'tf-df-icf', 'IG']

k = 40

no_of_topic = 53
did = 'Dataset-1'
#setup = 'title_content_ief_top_%d_per_loc_org_keywords_eta2_%0.1f' % (k, eta_2)  # 'title_ief_top_%d_per_loc_org_keywords_eta2_%0.1f' %(k,eta_2)
for cur_eta_1 in range(eta_1_start, eta_1_end):
    for cur_eta_2 in range(eta_2_start, eta_2_end):
        eta_1 = cur_eta_1* 0.1
        eta_2 = cur_eta_2 * 0.1
        for index, cur_setup in enumerate(setup_list[2:3], 2):
            if index == 0:
                fsp_file = '%s/ner_keywords/%s-ner_keyword_%0.1f' % (did, did, eta_1)
                setup = 'ner_keywords'
            elif index == 1:
                fsp_file = '%s/tf-df-icf/top-%d/%s-tf-df-icf_weight_%0.2f' % (did, k, did, eta_1)
                setup = 'tf-df-icf_top-%d' % (k)
            elif index ==2:
                fsp_file = '%s/IG/top-%d/%s-IG_weight_%0.2f' % (did, k, did, eta_1)
                setup = 'IG_top-%d' %(k)

            finp_file = 'restoredDate_filtered_event_new_v.2_0_900.pkl'

            iter_count = 120
            cmd = 'python lda_d_ver-1.py   --alpha=0.1 --eta1=%0.2f --eta2=%0.2f --fin=%s --fsp=%s -s -i %d --dp=%s --setup=%s --datasets=%s -k %d' \
                  % (eta_1, eta_2, finp_file, fsp_file, iter_count, 'uniform', setup, did, no_of_topic)
            print(' ##:', cmd)
            os.system(cmd)

t2 = time.time()

print('Total time taken :', (t2-t1))
