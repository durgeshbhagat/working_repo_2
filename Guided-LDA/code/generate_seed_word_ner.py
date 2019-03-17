
# This file generates weightage file for NER from Dataset-2 and Dataset-3
import os
import pickle
import time
import json

fname_list = ['../ip/restoredDate_filtered_event_new_v.2_0_900.pkl',
              '/home/durgesh/crawl_api/text_datasets/Reuter-21578-R-8/Reuter-21578_train_all_terms_ner_tagged.pkl',
              '/home/durgesh/crawl_api/text_datasets/20-Newsgroup/20-Newsgroup_all_term_ner_tagged.pkl']

base_out_dir = '../seed_word'

dataset_list = ['Dataset-1', 'Dataset-2', 'Dataset-3']

setup = 'ner_keywords'

entity_weight = [0.1, 0.2, 0.1]
excluded_tag = ['OT', 'ONS']


def filter_ner(dataset, file_index):
    t1 = time.time()
    sp_word = []
    f = open(fname_list[file_index], 'r')

    story_dic = pickle.load(f)
    f.close()
    story_keys_list = story_dic.keys()
    st = ''

    term2event = {}
    event2term = {}

    uniq_event2term = {}

    if dataset == 'Dataset-1':
        for story in story_keys_list[:]:
            event = '_'.join(story.split('_')[:2])
            #print('Event :', event)
            if event not in event2term:
                event2term[event] = []
            # print(story_dic[story].keys())
            # print(story_dic[story]['NER']['TITLE_CONTENT'].keys())
            for tag in story_dic[story]['NER']['TITLE_CONTENT']:
                if tag not in excluded_tag:
                    event2term[event] += story_dic[story]['NER']['TITLE_CONTENT'][tag]
    else:

        for story in story_keys_list[:]:
            if dataset == 'Dataset-2':
                event = story.split('_')[-2]
                #print('Event :', event)
            if dataset == 'Dataset-3':
                event = story.split('_')[-2]
                #print('Event :', event)
            if event not in event2term:
                event2term[event] = []
            for tag in story_dic[story]['entity']:
                if tag not in excluded_tag:
                    event2term[event] += story_dic[story]['entity'][tag]


    for event in event2term:
        event2term_list = list(set(event2term[event]))
        for term in event2term_list:
            if term == u'':
                continue
            else:
                term = str(term.encode('ascii', 'ignore').decode('ascii'))
            if term not in term2event:
                term2event[term] = []
            term2event[term].append(event)

    for term in term2event:
        if len(term2event[term]) ==1:
            event = term2event[term][0]
            #print(event)
            if event not in uniq_event2term:
                uniq_event2term[event] =[]
            uniq_event2term[event].append(term)

    print(sorted(uniq_event2term.keys()))
    # sp_word = list(set(sp_word))
    # if u'' in sp_word:
    #     sp_word.remove(u'')
    # print(sp_word[:10])
    #
    #
    # for word in sp_word:
    #     st += '%s\n' % (word.encode('utf-8').strip())
    # sp_word = list(set(sp_word))
    # if u'' in sp_word:
    #     sp_word.remove(u'')
    # print(sp_word[:10])
    #
    #
    # for word in sp_word:
    #     st += '%s\n' % (word.encode('utf-8').strip())

    fout_dir = '%s/%s/%s' % (base_out_dir, dataset, setup)

    try:
        os.makedirs(fout_dir)
    except:
        pass
    fout_name_total = '%s/%s-%s.json' % (fout_dir, dataset, setup)
    print('Writing in file :', fout_name_total)
    fout = open(fout_name_total, 'w')
    json.dump(uniq_event2term, fout , indent =4)
    fout.close()
    t2 = time.time()
    print('Time taken for  %s  is %f ' % (dataset, (t2-t1)))
    # print story_dic[story_keys_list[0]]['entity'].keys()


def main():
    t_start = time.time()
    for i, dataset in enumerate(dataset_list[0:], 0):
            filter_ner(dataset=dataset_list[i],  file_index=i)
    t_end = time.time()
    print('\n \t\t ----- Total taken is : %f' % (t_end - t_start))


if __name__ == '__main__':
    main()
