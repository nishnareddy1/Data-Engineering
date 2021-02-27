import pandas as pd
covid_df = pd.read_csv ('Downloads/COVID_county_data.csv/COVID_county_data.csv')
deaths_list=[]
cases_list=[]
for ind,date in enumerate(covid_df['date']):
    deaths=0
    cases=0
    if date[0:4]=='2020' and date[5:7]=='12':
        deaths=covid_df['deaths'][ind]
        cases=covid_df['cases'][ind]
    deaths_list.append(deaths)
    cases_list.append(cases)
covid_df['dec2020Deaths']=deaths_list
covid_df['Dec_Cases']=cases_list
covid_df=covid_df.groupby(['state','county']).agg({'cases':'sum','deaths':'sum','dec2020Deaths':'sum','Dec_Cases':'sum'})
covid_df.loc[[('Virginia','Loudoun'), ('Oregon','Washington'), ('Kentucky','Harlan'), ('Oregon','Malheur')]]