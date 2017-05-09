#!/usr/bin/python -tt

# Porgram to make special word weighatge file

import pickle
import os
import sys

out_dir = 'weightage_file'

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
    
    fout_name ='%s/per_%0.02f_loc_%0.2f_org_%0.2f' %(out_dir, per_weight,loc_weight,org_weight)
    fout= open(fout_name,'w')
    fout.write(st)
    fout.close() 
    return 


def load_file_entity(filename,entity_tag,entity_weight):
   
    weight_dic = { 'PER' : per_weight , 'LOC' : loc_weight,'ORG' : org_weight }
    fname_total  = 'ip/%s' %(filename)
    f = open(fname_total, 'r')
    story_dic = pickle.load(f)
    f.close()
   
    st =''             
    for i,tag in enumerate([entity]):
        cur_dic = entity_dic[i]
        for entity in cur_dic:
            st += '%s #,# %f\n' %(entity,weight_dic[tag] ) # curently editing here 
    for entity in story_dic[story]['NER'][entity_tag]:
        st += '%s #,# %f\n' %(entity,entity_weight)
    fout_name ='%s/per_%0.02f' %(out_dir, per_weight) #,loc_weight,org_weight)
    fout= open(fout_name,'w')
    fout.write(st)
    fout.close() 
    return 


def main():
    import optparse
    #import vocabulary 
    global out_dir 
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="corpus filename")
    #parser.add_option("--per", dest="per_weight", type="float", help="person weight", default=0.2)
    #parser.add_option("--loc", dest="loc_weight", type="float", help="location weight", default=0.4)
    #parser.add_option("--org", dest="org_weight", type="float", help="organisation weight", default=0.1)
    parser.add_option("--dp", dest="dp", help="ditichlet prior sysmetric or asymmetric ?")
    parser.add_option("--entity_weight", dest="setup", help="entity_weight")
    parser.add_option("--setup", dest="setup", help="setup details")
    (options, args) = parser.parse_args()
    
    if options.dp == "uniform" and options.setup == "PER" :  
        out_dir = '%s/%s/%s_%0.2f' %(out_dir, options.dp, options.setup, options.entity_weight)
        try:
            os.makedirs(out_dir)
        except:
            pass
        load_file_entity(options.filename, options.setup, options.entity_weight)    
    '''
    if options.filename:
         corpus,doc_ids, event_list  = vocabulary.load_file(options.filename,t)
    else:
        options.filename = 'filtered_event_new2.pkl'
        corpus,doc_ids, event_list  = vocabulary.load_file(options.filename,t)
    '''  
    #load_file(options.filename,options.per_weight,options.loc_weight,options.org_weight)   
    #voca = vocabulary.Vocabulary(options.stopwords)
    #docs = [voca.doc_to_ids(doc) for doc in corpus]
    #corpus = vocabulary.load_corpus(options.corpus)
    #if not corpus: parser.error("corpus range(-c) forms 'start:end'")
if __name__ =='__main__':
    main()
