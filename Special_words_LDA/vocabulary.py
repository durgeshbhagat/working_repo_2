#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is available under the MIT License.
# (c)2010-2011 Nakatani Shuyo / Cybozu Labs Inc.

import pickle
import nltk, re

ip_dir ='ip'
def load_corpus(range):
    m = re.match(r'(\d+):(\d+)$', range)
    if m:
        start = int(m.group(1))
        end = int(m.group(2))
        from nltk.corpus import brown as corpus
        return [corpus.words(fileid) for fileid in corpus.fileids()[start:end]]
'''
#modified load_file
def load_file(filename):+
    corpus = []
    doc_ids= []
    event_list=[]
    f = open(filename, 'r')
    story_dic = pickle.load(f)
    f.close()
    for story in sorted(story_dic):
        title_content = story_dic[story]['CONTENT'] + story_dic[story]['TITLE']
        doc = re.findall(r'\w+(?:\'\w+)?',title_content) # tokenizing here
        doc_id = story.strip('.html').strip('.htm')
        event_id = '_'.join(doc_id.split('_')[:2])
        #print 'doc in load file ' , doc
        if len(doc)>0:
            corpus.appen(doc)
            doc_ids.append(doc_id)
            if event_id not in event_list:
                event_list.append(event_id)
    f.close()
    return corpus, doc_ids, event_list

#stopwords_list = nltk.corpus.stopwords.words('english')
fname_stopword = 'stop_word.txt'
f=open(fname_stopword,'r')
stopwords_list = f.read().strip().split('\n')
f.close()
'''


# new load_file by Durgesh on 12/10/16 


 # special words info in special_words_info 
def load_file(filename,special_words):
    corpus = []
    doc_ids= []
    event_list=[]
    fname_total  = '%s/%s' %(ip_dir,filename)
    f = open(fname_total, 'r')
    story_dic = pickle.load(f)
    f.close()
    # Include 'PER' , 'LOC', 'ORG', DATE , Time  , ONS
    for story in sorted(story_dic):
        #print story	 
        temp_doc =[]
        special_word =[]
        non_special_word=[]
        for item in ['PER' , 'LOC' , 'ORG', 'ONS'] :
            #print item , story_dic[story]['NER'][item]
            for term in story_dic[story]['NER'][item]:
                if term in special_words:
                    special_word.append(term)
                else:
                    non_special_word.append(term)
            #temp_doc += story_dic[story]['NER'][item]
        temp_doc.append(special_word)
        temp_doc.append(non_special_word)
        #temp =[]                       
        
        #for item in ['ONS']:
        #    temp_doc += story_dic[story]['NER'][item]
        #temp_doc.append(temp)
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
    f.close()
    return corpus, doc_ids, event_list



#stopwords_list = nltk.corpus.stopwords.words('english')
fname_stopword = 'stop_word.txt'
f=open(fname_stopword,'r')
stopwords_list = f.read().strip().split('\n')
f.close()



#print stop
#stopwords_list += "a,s,able,about,above,according,accordingly,across,actually,after,afterwards,again,against,ain,t,all,allow,allows,almost,alone,along,already,also,although,always,am,among,amongst,an,and,another,any,anybody,anyhow,anyone,anything,anyway,anyways,anywhere,apart,appear,appreciate,appropriate,are,aren,t,around,as,aside,ask,asking,associated,at,available,away,awfully,be,became,because,become,becomes,becoming,been,before,beforehand,behind,being,believe,below,beside,besides,best,better,between,beyond,both,brief,but,by,c,mon,c,s,came,can,can,t,cannot,cant,cause,causes,certain,certainly,changes,clearly,co,com,come,comes,concerning,consequently,consider,considering,contain,containing,contains,corresponding,could,couldn,t,course,currently,definitely,described,despite,did,didn,t,different,do,does,doesn,t,doing,don,t,done,down,downwards,during,each,edu,eg,eight,either,else,elsewhere,enough,entirely,especially,et,etc,even,ever,every,everybody,everyone,everything,everywhere,ex,exactly,example,except,far,few,fifth,first,five,followed,following,follows,for,former,formerly,forth,four,from,further,furthermore,get,gets,getting,given,gives,go,goes,going,gone,got,gotten,greetings,had,hadn,t,happens,hardly,has,hasn,t,have,haven,t,having,he,he,s,hello,help,hence,her,here,here,s,hereafter,hereby,herein,hereupon,hers,herself,hi,him,himself,his,hither,hopefully,how,howbeit,however,i,d,i,ll,i,m,i,ve,ie,if,ignored,immediate,in,inasmuch,inc,indeed,indicate,indicated,indicates,inner,insofar,instead,into,inward,is,isn,t,it,it,d,it,ll,it,s,its,itself,just,keep,keeps,kept,know,knows,known,last,lately,later,latter,latterly,least,less,lest,let,let,s,like,liked,likely,little,look,looking,looks,ltd,mainly,many,may,maybe,me,mean,meanwhile,merely,might,more,moreover,most,mostly,much,must,my,myself,name,namely,nd,near,nearly,necessary,need,needs,neither,never,nevertheless,new,next,nine,no,nobody,non,none,noone,nor,normally,not,nothing,novel,now,nowhere,obviously,of,off,often,oh,ok,okay,old,on,once,one,ones,only,onto,or,other,others,otherwise,ought,our,ours,ourselves,out,outside,over,overall,own,particular,particularly,per,perhaps,placed,please,plus,possible,presumably,probably,provides,que,quite,qv,rather,rd,re,really,reasonably,regarding,regardless,regards,relatively,respectively,right,said,same,saw,say,saying,says,second,secondly,see,seeing,seem,seemed,seeming,seems,seen,self,selves,sensible,sent,serious,seriously,seven,several,shall,she,should,shouldn,t,since,six,so,some,somebody,somehow,someone,something,sometime,sometimes,somewhat,somewhere,soon,sorry,specified,specify,specifying,still,sub,such,sup,sure,t,s,take,taken,tell,tends,th,than,thank,thanks,thanx,that,that,s,thats,the,their,theirs,them,themselves,then,thence,there,there,s,thereafter,thereby,therefore,therein,theres,thereupon,these,they,they,d,they,ll,they,re,they,ve,think,third,this,thorough,thoroughly,those,though,three,through,throughout,thru,thus,to,together,too,took,toward,towards,tried,tries,truly,try,trying,twice,two,un,under,unfortunately,unless,unlikely,until,unto,up,upon,us,use,used,useful,uses,using,usually,value,various,very,via,viz,vs,want,wants,was,wasn,t,way,we,we,d,we,ll,we,re,we,ve,welcome,well,went,were,weren,t,what,what,s,whatever,when,whence,whenever,where,where,s,whereafter,whereas,whereby,wherein,whereupon,wherever,whether,which,while,whither,who,who,s,whoever,whole,whom,whose,why,will,willing,wish,with,within,without,won,t,wonder,would,would,wouldn,t,yes,yet,you,you,d,you,ll,you,re,you,ve,your,yours,yourself,yourselves,zero".split(',')
recover_list = {"wa":"was", "ha":"has"}
wl = nltk.WordNetLemmatizer()

def is_stopword(w):
    return w in stopwords_list
def lemmatize(w0):
    w = wl.lemmatize(w0.lower())
    #if w=='de': print w0, w
    if w in recover_list: return recover_list[w]
    return w




# Storing seprately special_words and non-special words

class Vocabulary:
    def __init__(self, excluds_stopwords=False,special_words={}):
        self.vocas_sp = []        # id to word for NER
        self.vocas_id_sp = dict() # word to id for NER
        
        self.vocas_nsp = []        # id to word for Non-NER
        self.vocas_id_nsp = dict() # word to id for Non-NER
        
        self.docfreq_sp = []      # id to document frequency for NER
        self.docfreq_nsp = []     # id  to document frequency for NON-NER
        self.excluds_stopwords = excluds_stopwords
        self.special_words= special_words
        print 'Assam' in self.special_words

    def term_to_id(self, term0, ner_tag='Nner'):
        # ner_tag can be either ner or Nner
        term =term0.strip() #lemmatize(term0)
        #if not re.match(r'[a-z]+$', term): return None
        #print '\nTerm is :%s#' %(term),
        voca_id = None
        if self.excluds_stopwords and is_stopword(term): return None
        if term not in self.vocas_id_sp and term in self.special_words:
            voca_id = len(self.vocas_sp)
            #print '\t----------term is %s, id is : %d ' %(term,voca_id)
            self.vocas_id_sp[term] = voca_id
            self.vocas_sp.append(term)
            self.docfreq_sp.append(0)
        elif term not in self.vocas_id_nsp and term not in self.vocas_id_sp :
                #print 'Executinh Here!!!' 
                voca_id = len(self.vocas_nsp)
                self.vocas_id_nsp[term] = voca_id
                self.vocas_nsp.append(term)
                self.docfreq_nsp.append(0)   
        else:
            if term in self.special_words:
                #print 'TERM %s  Found in special words!!' %(term),
                voca_id = self.vocas_id_sp[term]
            else:
                #print 'TERM %s NOT found in special words !!! ' %(term),
                voca_id = self.vocas_id_nsp[term]
        return voca_id

    def doc_to_ids(self, doc):
        #print ' '.join(doc)
        new_doc = [] #list = []
        words = dict()
        #print 'Doc : ' , doc
        sp_doc =[] 
        nsp_doc =[]
        print '\n ##########Processing new DOC-------------------------'
        #print ' DOC is :', doc
        for i,cat in enumerate(doc):
            for term in doc[i]: # special non special ! Huh
                #print 'term : %s' %(term),
                wid = self.term_to_id(term)
                #print '  wid =%d , category =%d' %(wid,i) ,
                if wid != None:
                    if i==0 :
                        sp_doc.append(wid)
                    else:
                        nsp_doc.append(wid)
                    if not wid in words:
                        words[wid] = 1
                        #print ' Exits : ' , wid in self.docfreq_sp ,  wid in self.docfreq_nsp
                        if i==0 :
                            self.docfreq_sp[wid] += 1
                        else:
                            self.docfreq_nsp[wid] += 1
       
        if "close" in dir(doc) : doc.close()
        #print '\n Coded doc : ', [sp_doc,nsp_doc]
        return [sp_doc,nsp_doc]

    def cut_low_freq(self, corpus, threshold=1):
        new_vocas = []
        new_docfreq = []
        self.vocas_id = dict()
        conv_map = dict()
        for id, term in enumerate(self.vocas):
            freq = self.docfreq[id]
            if freq > threshold:
                new_id = len(new_vocas)
                self.vocas_id[term] = new_id
                new_vocas.append(term)
                new_docfreq.append(freq)
                conv_map[id] = new_id
        self.vocas = new_vocas
        self.docfreq = new_docfreq

        def conv(doc):
            new_doc = []
            for id in doc:
                if id in conv_map: new_doc.append(conv_map[id])
            return new_doc
        return [conv(doc) for doc in corpus]

    def __getitem__(self, v,cat='sp'):
    #returns the word corresponding to word no in the respective category  : Special Words and Non-Special Words ; cat takes two values : sp and nsp respectively 
        if cat == 'sp':
            return self.vocas_sp[v]
        elif cat =='nsp':
            return self.vocas_nsp[v]
        else:
            print 'Wrong Category provided : %s ' %(cat)
        return None   
    def size(self):
        return [len(self.vocas_sp), len(self.vocas_nsp)]

    def is_stopword_id(self, id):
        return self.vocas[id] in stopwords_list


'''
# Document represntation of list of list : [ [t1,t2,t3,.....] , [t2,t3,t4,...], ...,      ] 
class Vocabulary:
    def __init__(self, excluds_stopwords=False):
        self.vocas = []        # id to word 
        self.vocas_id = dict() # word to id 
        
 
        self.docfreq = []      # id to document frequency 
        self.excluds_stopwords = excluds_stopwords

    def term_to_id(self, term0):
        # ner_tag can be either ner or Nner
        term =term0 #lemmatize(term0)
        #if not re.match(r'[a-z]+$', term): return None
        voca_id = None
        if self.excluds_stopwords and is_stopword(term): return None
        if term not in self.vocas_id:
            voca_id = len(self.vocas)
            self.vocas_id[term] = voca_id
            self.vocas.append(term)
            self.docfreq.append(0)
      
        else:
                voca_id = self.vocas_id[term]
           
        return voca_id

    def doc_to_ids(self, doc):
        #print ' '.join(doc)
        new_doc = [] #list = []
        words = dict()
        #print 'Doc : ' , doc
        ner_doc =[] 
        for term in doc:
            #print 'term :: ' , term
            id = self.term_to_id(term) #, 'ner')
            if id != None:
                new_doc.append(id)
                if not id in words:
                    words[id] = 1
                    self.docfreq[id] += 1
       
        if "close" in dir(doc) : doc.close()
        return new_doc
    def cut_low_freq(self, corpus, threshold=1):
        new_vocas = []
        new_docfreq = []
        self.vocas_id = dict()
        conv_map = dict()
        for id, term in enumerate(self.vocas):
            freq = self.docfreq[id]
            if freq > threshold:
                new_id = len(new_vocas)
                self.vocas_id[term] = new_id
                new_vocas.append(term)
                new_docfreq.append(freq)
                conv_map[id] = new_id
        self.vocas = new_vocas
        self.docfreq = new_docfreq

        def conv(doc):
            new_doc = []
            for id in doc:
                if id in conv_map: new_doc.append(conv_map[id])
            return new_doc
        return [conv(doc) for doc in corpus]

    def __getitem__(self, v):
    #returns the word corresponding to word no
        return self.vocas[v]
   
    def size(self):
        return len(self.vocas)
    def is_stopword_id(self, id):
        return self.vocas[id] in stopwords_list




''' 
