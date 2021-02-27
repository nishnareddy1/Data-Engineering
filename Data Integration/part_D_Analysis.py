import matplotlib.pyplot as plt
import seaborn as sns

a = ('cases', 'Poverty')
b = ('deaths', 'Poverty')
c = ('cases', 'IncomePerCap')
d = ('deaths', 'IncomePerCap')
e = ('Dec_Cases', 'Poverty')
f = ('Dec_Cases', 'Poverty')
g = ('Dec_Cases', 'IncomePerCap')
h = ('Dec_Cases', 'IncomePerCap')

oregondf = df.loc[df.index.get_level_values('state') == 'Oregon']

cor = []

cor.append(a)
cor.append(b)
cor.append(c)
cor.append(d)
cor.append(e)
cor.append(f)
cor.append(g)
cor.append(h)

# For Oregon Data
plots_oregon = []
for row in cor:
    graph = (oregondf[row[0]].corr(df[row[1]]), row[0], row[1])
    plots_oregon.append(graph)

for i in plots_oregon:
    R = i[0]
    print("R values", R)
    if (R > 0.5 or R < -0.5):
        plt.figure()
        sns.scatterplot(data=oregondf, x=i[1], y=i[2])

# USA
plots_all=[]
for row in cor:
    graph=(df[row[0]].corr(df[row[1]]),row[0],row[1])
    plots_all.append(graph)

for i in plots_all:
    R=i[0]
    print("R values", R)
    if(R>0.5 or R<-0.5):
        plt.figure()
        sns.scatterplot(data=df,x=i[1],y=i[2]) #for others