import matplotlib.pyplot as plt
import seaborn as sns
lis = []
one = ('cases', 'Poverty')
lis.append(one)
two = ('deaths', 'Poverty')
lis.append(two)
three = ('cases', 'IncomePerCap')
lis.append(three)
four = ('deaths', 'IncomePerCap')
lis.append(four)
five = ('Dec_Cases', 'Poverty')
lis.append(five)
six = ('Dec_Cases', 'Poverty')
lis.append(six)
seven = ('Dec_Cases', 'IncomePerCap')
lis.append(seven)
eight = ('Dec_Cases', 'IncomePerCap')
lis.append(eight)

oregondf = df.loc[df.index.get_level_values('state') == 'Oregon']

# For Oregon Data
oregon = []
for row in lis:
    graph = (oregondf[row[0]].corr(df[row[1]]), row[0], row[1])
    oregon.append(graph)

for i in oregon:
    R = i[0]
    print("R values", R)
    if (R > 0.5 or R < -0.5):
        plt.figure()
        sns.scatterplot(data=oregondf, x=i[1], y=i[2])

# USA
all=[]
for row in lis:
    R=(df[row[0]].corr(df[row[1]]),row[0],row[1])
    all.append(R)

for i in all:
    R=i[0]
    print("R values", R)
    if(R>0.5 or R<-0.5):
        plt.figure()
        sns.scatterplot(data=df,x=i[1],y=i[2]) #for others