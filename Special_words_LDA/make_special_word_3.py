# This file generates weightage file for NER from Dataset-2 and Dataset-3
import os
import pickle
import sys
import time


fname_list = ['ip/restoredDate_filtered_event_new_v.2_0_900.pkl', '/home/durgesh/crawl_api/text_datasets/Reuter-21578-R-8/Reuter-21578_train_all_terms_ner_tagged.pkl' ,

'/home/durgesh/crawl_api/text_datasets/20-Newsgroup/20-Newsgroup_all_term_ner_tagged.pkl'
]

base_out_dir = 'weightage_file'

dataset_list = [ 'Dataset-1' , 'Dataset-2' , 'Dataset-3' ]

setup = 'ner_keywords'

entity_weight = [0,0.2, 0.1]
excluded_tag = [ 'OT' , 'ONS']

def filter_ner(dataset, weight, file_index):
    t1 = time.time()
    sp_word = []
    f=open(fname_list[file_index],'r')

    story_dic = pickle.load(f)
    f.close()
    story_keys_list = story_dic.keys()
    st = ''
    if dataset=='Dataset-1':
        for story in story_keys_list[:]:
            #print(story_dic[story].keys())
            #print(story_dic[story]['NER']['TITLE_CONTENT'].keys())
            for tag in story_dic[story]['NER']['TITLE_CONTENT']:
                if tag not in excluded_tag:
                    sp_word += story_dic[story]['NER']['TITLE_CONTENT'][tag]
    else:
       for story in story_keys_list[:]:
            for tag in story_dic[story]['entity']:
                if tag not in excluded_tag:
                    sp_word += story_dic[story]['entity'][tag]
    sp_word = list(set(sp_word))
    for word in sp_word:
        st += '%s #,# %f\n' %(word.encode('utf-8').strip(), weight)

    fout_dir = '%s/%s/%s' %(base_out_dir, dataset , setup)

    try:
        os.makedirs(fout_dir)
    except:
        pass
    fout_name_total = '%s/%s-ner_keyword_%0.1f' %(fout_dir, dataset, weight)
    print( 'Writing in file :', fout_name_total)
    fout =open(fout_name_total,'w')
    fout.write(st)
    fout.close()
    t2 = time.time()
    print('Time taken for  %s  is %f ' %(dataset, (t2-t1)))
    #print story_dic[story_keys_list[0]]['entity'].keys()


def main():
    t_start = time.time()
    for i,dataset in enumerate(dataset_list[0:3],0):
        for score in range(1,2):
            filter_ner(dataset= dataset_list[i], weight = score * 0.1 ,file_index=i)
    t_end = time.time()
    print('\n \t\t ----- Total taken is : %f' %(t_end-t_start))

if __name__ == '__main__':
    main()
