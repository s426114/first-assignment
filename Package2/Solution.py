import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

#EX 1

#Read data
data_df = pd.read_csv(Path(Path.cwd() / "survey_results_public.csv"), usecols=['Respondent', 'WorkWeekHrs', 'YearsCode', 'Age1stCode', 'YearsCodePro', 'ConvertedComp', 'Student', 'FizzBuzz'], index_col='Respondent')

#Drop empty records and convert float columns to integers (we want whole hours without minutes)
data_df.dropna(inplace=True, how='any')

#Replace strings inside YearsCode & YerasCodePro & Age1stCode column
data_df.replace(to_replace={'Less than 1 year':'0', 'More than 50 years':'50', 'Younger than 5 years':'5', 'Older than 85':'85'}, inplace=True)

#Cast numerical columns to float
data_df = data_df.astype({'WorkWeekHrs':'int64', 'YearsCode':'int64', 'YearsCodePro':'int64', 'Age1stCode':'int64', 'ConvertedComp':'int64'})

#Check number of int columns
num_cols = data_df.select_dtypes(include=['int64']).columns

#Check for correlation - use corr() and charts
fig, axs = plt.subplots(2,len(num_cols),figsize=(16,8))
fig.tight_layout(h_pad=4.0, w_pad=4.0)
fig_list = fig.axes
current_fig = 0

for no, main_col in enumerate(num_cols):
    for other_col in num_cols[no+1:]:
        data_df.plot(x=main_col, y=other_col, marker='x', color='b', markersize=1, linestyle='', ax=fig_list[current_fig])
        fig_list[current_fig].set_xlabel(main_col, fontsize=8)
        fig_list[current_fig].set_ylabel(other_col, fontsize=8)
        current_fig += 1

#plt.show()
#print(data_df.corr())

#Chosen variables [ ConvertedComp, Age1stCode ] - independent variables; ['YearsCode'] - dependend variables

#EX 2

#Replace text values to numercial data
data_df['FizzBuzz'].replace(to_replace={'Yes': '1', 'No': '0'}, inplace=True)

#Replace values via one-hot-encoding method
ohe_df = pd.get_dummies(data_df['Student'])
data_df.drop('Student', axis = 1, inplace=True)
data_df = data_df.join(ohe_df)

print(data_df)