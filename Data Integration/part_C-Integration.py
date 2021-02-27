df=acs_df.merge(covid_df, on=['state','county'], how='inner')
df.loc[[('Oregon')]]