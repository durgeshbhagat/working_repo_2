#!/usr/bin/python

# this file calculates tf,df,idf of all the NER term , unigram,bi-gram and tri-grram present in the document.

import os
import sys
import pickle
import time


ip_dir ='ip'

def calculate_ner_terms(fname):
    inverted_dic ={ 'PER': {}, 'LOC': {}, 'ORG' : {}} 
  
    fname_total  = '%s/%s' %(ip_dir,fname)
    f = open(fname_total, 'r')
    story_dic = pickle.load(f)
    f.close()
    # Include 'PER' , 'LOC', 'ORG', DATE , Time  , ONS
    for story in sorted(story_dic):
        #print story	 
        temp_doc =[]
        temp = []
        for tag in ['PER' , 'LOC' , 'ORG'] :
            for term in story_dic[story]['NER'][tag]:
                if term in inverted_dic[tag]:
                    inverted_dic[tag][term] +=1 #tf only till now  
                else:
                    inverted_dic[tag][term] = 1
                    
                    
                    
    '''                
            #print item , story_dic[story]['NER'][item]
            temp += story_dic[story]['NER'][item]
        temp_doc.append(temp)
        temp =[]
        for item in ['ONS']:
            temp+= story_dic[story]['NER'][item]
        temp_doc.append(temp)
        #print 'Temp_doc :: ' , temp_doc
        #title_content = story_dic[story]['CONTENT'] + story_dic[story]['TITLE']
        #doc = re.findall(r'\w+(?:\'\w+)?',title_content) # tokenizing here
        doc_id = story.strip('.html').strip('.htm')
        event_id = '_'.join(doc_id.split('_')[:2])
        #print 'doc in load file ' , doc
        if len(temp_doc)>0:
            corpus.append(temp_doc)
            doc_ids.append(doc_id)
            if event_id not in event_list:
                event_list.append(event_id)
    f.close()'''
    return inverted_dic

def write_to_file(dirname,fname,l):
    try:
        os.mkdir(dirname)
    except :
        pass
    fname_total = '%s/%s' %(dirname,fname)
    f=open(fname_total,'w')
    st=''
    for item in l: 
       st += '%s,%d\n' %(item[0],item[1])
    f.write(st)
    f.close() 
    

def main():
    t1=time.time()
    fname = 'filtered_event_new2.pkl'
    inverted_dic = calculate_ner_terms(fname)
    per_inverted_list = inverted_dic['PER'].items()
    #loc_inverted_list = inverted_dic['LOC'].items()
    #org_inverted_list = inverted_dic['ORG'].items()
    
    per_inverted_list.sort(key= lambda item : item[1],reverse = True)
    print 'total no of PER ' , len(per_inverted_list)
    print per_inverted_list[:100]
    write_to_file('temp_dir','per_list.csv',per_inverted_list)
    t2 = time.time()
    
    print 'Time taken %f' %(t2-t1)
    
    
if __name__ =='__main__':
    main()
    
