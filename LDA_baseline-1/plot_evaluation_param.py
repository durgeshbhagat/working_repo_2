import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv
from matplotlib.pyplot import subplots

axes = plt.gca()
#axes.set_ylim([0.0,1.5])
axes.set_xlim([0.0,200])
color = [ 'w','b','g','r','c',]
csv_data = read_csv('LDA_base_line_evaluation.txt', index_col=0, header=0, sep='\t',names=['Precision','Recall', 'F-measure','JC', 'Rand index'])

#index = list(csv_data.index.get_values())
index =['0.1-0.1','0.1-0.2','0.1-0.3','0.1-0.4','0.2-0.1','0.2-0.2','0.2-0.3','0.2-0.4','0.3-0.1','0.3-0.2','0.3-0.3','0.3-0.4','0.4-0.1','0.4-0.2','0.4-0.3','0.4-0.4']
mat = DataFrame.as_matrix(csv_data)
#columns = ['eq_wt(0.85)'	,'the_hindu(0.75)'	,'temp_gtd(0.25)',	'activeness(0.35)', 'train_gtd']
# columns = ['Southeast Asia',	'South Asia',	'Western Europe',	'Middle East & North Africa',	'Sub-Saharan Africa']
#columns = ['islamist_sepa',	'left_wing',	'nat_and_sep',	'nationalist',	'religious_islamic']
columns = ['Precision','Recall', 'F-measure','JC', 'Rand index'] #['$PR$','$PPR^{Co}$',	'$PPR^{T}_{Rel}$',	'$PPR^{T}_{Act}$',	'$Freq$',	'$Recy$']
print mat
df = DataFrame(mat, index=index, columns=columns)
#print 'csv_data :: ' , csv_data['Alpha_Eta']
fig, ax = subplots(subplot_kw={'ylim': (0.0,1.0)})
df.plot(ax=ax, kind='bar', legend=False, color= color, grid=False)
#df.plot(ax=ax, kind='bar', legend=False,color=['w'],grid=False) 
ax.set_ylabel("Correlation with Ground Truth Frequency")
ax.set_xlabel("Ideological Groups")
#ax.set_title('')
#ax.set_yticklabels([0.0,0.2,0.4,0.6,0.8,1.0 ])
#ax.set_yticklabels([0.0,0.2,0.4,0.6,0.8,1.0])
bars = ax.patches
#hatches = ''.join(h*len(df) for h in '*\-O/.')

#for bar, hatch in zip(bars, hatches):
#    bar.set_hatch(hatch)

ax.set_xticklabels(df.index, rotation=45, fontsize='9')
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.legend(ncol=3, loc='upper center')
fig.savefig('plot2.eps', bbox_inches='tight')
