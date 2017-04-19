#!/usr/bin/python -tt

# Porgram to make special word weighatge file

import pickle
import os
import sys



def load_file(filename,per_weight,loc_weight,org_weight):
    corpus = []
    doc_ids= []
    event_list=[]
    entity_dic =[ {},{},{}]
    PER_dic= {}
    LOC_dic={}
    ORG_dic={}
    weight_dic = { 'PER' : per_weight , 'LOC' : loc_weight,'ORG' : org_weight }
    fname_total  = 'ip/%s' %(filename)
    f = open(fname_total, 'r')
    story_dic = pickle.load(f)
    f.close()
    # Include 'PER' , 'LOC', 'ORG', DATE , Time  , ONS
    for story in sorted(story_dic):
        #print story	 
        temp_doc =[]
        temp = []
        for i,tag in enumerate(['PER' , 'LOC' , 'ORG']) :
            cur_dic = entity_dic[i]
            for entity in story_dic[story]['NER'][tag]:
                if entity in cur_dic:
                    cur_dic[entity] += 1
                else:
                    cur_dic[entity] = 1
    st =''             
    for i,tag in enumerate(['PER','LOC','ORG']):
        cur_dic = entity_dic[i]
        for entity in cur_dic:
            st += '%s #,# %f\n' %(entity,weight_dic[tag] ) # curently editing here 
    out_dir = 'weightage_file'
    fout_name ='%s/per_%0.02f_loc_%0.2f_org_%0.2f' %(out_dir, per_weight,loc_weight,org_weight)
    fout= open(fout_name,'w')
    fout.write(st)
    fout.close() 
    return corpus, doc_ids, event_list

def main():
    import optparse
    import vocabulary 
    global out_dir 
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="corpus filename")
    parser.add_option("--per", dest="per_weight", type="float", help="person weight", default=0.2)
    parser.add_option("--loc", dest="loc_weight", type="float", help="location weight", default=0.4)
    parser.add_option("--org", dest="org_weight", type="float", help="organisation weight", default=0.1)
    (options, args) = parser.parse_args()
    '''
    parser.add_option("-c", dest="corpus", help="using range of Brown corpus' files(start:end)")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
    parser.add_option("--eta1", dest="eta1", type="float", help="parameter eta for ner word", default=0.4)
    parser.add_option("--eta2", dest="eta2", type="float", help="parameter eta for Non-ner word", default=0.2)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=10)
    parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
    parser.add_option("--stopwords", dest="stopwords", help="exclude stop words", action="store_true", default=False)
    parser.add_option("--seed", dest="seed", type="int", help="random seed")
    parser.add_option("--df", dest="df", type="int", help="threshold of document freaquency to cut words", default=0)
    (options, args) = parser.parse_args()
    pass
    '''
    if options.filename:
         corpus,doc_ids, event_list  = vocabulary.load_file(options.filename)
    else:
        options.filename = 'filtered_event_new2.pkl'
        corpus,doc_ids, event_list  = vocabulary.load_file(options.filename)
        
    load_file(options.filename,options.per_weight,options.loc_weight,options.org_weight)   
    #voca = vocabulary.Vocabulary(options.stopwords)
    #docs = [voca.doc_to_ids(doc) for doc in corpus]
    #corpus = vocabulary.load_corpus(options.corpus)
    #if not corpus: parser.error("corpus range(-c) forms 'start:end'")
if __name__ =='__main__':
    main()
