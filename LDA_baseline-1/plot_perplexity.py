import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import itertools


base_dir ='results/all_words'

dir_list = os.listdir(base_dir)
dir_list.sort()
dir_total = []
legend_list=[]
style_1 = [ '-' ,'--','o','2']
style_2 = [ 'b','g','r','c']
final_style = list(itertools.product(style_1,style_2)) 
for i,cur_dir in enumerate(dir_list):
    temp_list = cur_dir.strip().split('_')
    st= '%0.1f_%0.1f' %(float(temp_list[3]),float(temp_list[5]))
    print 'st=%s ' %(st)
    legend_list.append(st)
    

for i,cur_dir in enumerate(dir_list):
    cur_dir_total ='%s/%s' %(base_dir,cur_dir)
    cur_dir_list = os.listdir(cur_dir_total)
    cur_dir_list.sort()
    t = '%s/%s' %(cur_dir_total,cur_dir_list[0])
    dir_total.append(t)

p_list=[]    
for i,cur_dir in enumerate(dir_total):
    print 'Processing %d , cur_dir =%s' %(i,cur_dir)
    p_list.append([])
    fname_log_dir ='%s/%s' %(cur_dir,'log_file.txt')
    f=open(fname_log_dir,'r')
    line_list= f.read().strip().split('\n')
    for j,cur_line in enumerate(line_list[1:-1],1):
        cur_line_list = cur_line.strip().split('\t')[0].split(' ')
        p = float(cur_line_list[1].strip('p='))
        p_list[i].append(p)
        #print 'Perplexity : ', p

x=range(1,121)
print x
fig =plt.figure()
#fig, ax = plt.subplots()
for i,p in enumerate(p_list):
    print ' i=%d , len p[i]=%d' %(i, len(p))
    sty = '%s%s' %(final_style[i][1],final_style[i][0])
    plt.plot(x,p_list[i],sty,label=legend_list[i])
plt.legend(loc='best')
plt.xlabel('------Iteration Count --->')
plt.ylabel('---- Perplexity------>')
fname_out = 'perplexity.eps'
fig.savefig(fname_out)
print final_style
