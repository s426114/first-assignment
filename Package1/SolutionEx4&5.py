import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

#Read data
data_df = pd.read_csv(Path(Path.cwd() / "survey_results_public.csv"), usecols=['Respondent', 'WorkWeekHrs', 'CodeRevHrs', 'Student'], index_col='Respondent')

#Drop empty records and convert float columns to integers (we want whole hours without minutes)
data_df.dropna(inplace=True, how='any')
data_df.astype({'WorkWeekHrs':'int32', 'CodeRevHrs':'int32'}, copy=False)

#Remove records where CodeRevHrs > WorkWeekHrs & WorkWeekHrs >= (24*7)
data_df = data_df[(data_df['WorkWeekHrs'] < 168) & (data_df['CodeRevHrs'] < data_df['WorkWeekHrs'])]

#Create plot for selected numerical columns
data_df.plot(x='WorkWeekHrs', y='CodeRevHrs', marker='x', color='b', markersize=0.3, linestyle='', title='Code review hours vs Total time working')

#Group data by student column
df_groups = data_df.groupby(['Student'])

#Setup Subplots and plot each group from df_groups
fig, axs = plt.subplots(len(df_groups))
fig.tight_layout(h_pad=4.0)

for (name, df), ax in zip(df_groups, axs.flat):
    df.plot(x='WorkWeekHrs', y='CodeRevHrs', marker='x', color='b', markersize=0.3, linestyle='', title=('Are you a student? : ' + name), ax=ax)

plt.show()