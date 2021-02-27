import pandas as pd
acs_df = pd.read_csv ('Downloads/acs2017_census_tract_data.csv/acs2017_census_tract_data.csv')
acs_df.rename(columns={'County': 'county','State':'state'}, inplace=True)
acs_df['county'] = acs_df['county'].map(lambda k:k.strip('County').strip())
acs_df=acs_df.groupby(['state','county']).agg({'TotalPop':'sum','Poverty':'mean','IncomePerCap':'mean'})
acs_df.loc[[('Virginia','Loudoun'),('Oregon','Washington'),('Kentucky','Harlan'),('Oregon','Malheur')]]

