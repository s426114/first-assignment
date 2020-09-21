import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn import linear_model, preprocessing
from sklearn.metrics import mean_squared_error
from scipy import stats


def plot_dataframe(data_df, columns, rows_no): 
    #Create plots for selected columns from passed dataframe
    fig, axs = plt.subplots(rows_no, len(columns), figsize=(16,8))
    fig.tight_layout(h_pad=4.0, w_pad=4.0)
    fig_list = fig.axes
    current_fig = 0

    for no, main_col in enumerate(columns):
        for other_col in columns[no+1:]:
            data_df.plot(x=main_col, y=other_col, marker='x', color='b', markersize=1, linestyle='', ax=fig_list[current_fig])
            fig_list[current_fig].set_xlabel(main_col, fontsize=8)
            fig_list[current_fig].set_ylabel(other_col, fontsize=8)
            current_fig += 1

    plt.show()


#EX 1

#Read data
data_df = pd.read_csv(Path(Path.cwd() / "survey_results_public.csv"), usecols=['Respondent', 'WorkWeekHrs', 'YearsCode', 'Age1stCode', 'YearsCodePro', 'ConvertedComp', 'Student', 'FizzBuzz'], index_col='Respondent')

#Drop empty records and convert float columns to integers (we want whole hours without minutes)
data_df.dropna(inplace=True, how='any')

#Replace strings inside YearsCode & YerasCodePro & Age1stCode column
data_df.replace(to_replace={'Less than 1 year':'0', 'More than 50 years':'50', 'Younger than 5 years':'5', 'Older than 85':'85'}, inplace=True)

#Cast numerical columns to float
data_df = data_df.astype({'WorkWeekHrs':'int64', 'YearsCode':'int64', 'YearsCodePro':'int64', 'Age1stCode':'int64', 'ConvertedComp':'int64'})

#Check for correlation - use corr() and charts
#plot_dataframe(data_df, data_df.select_dtypes(include=['int64']).columns, 2)
#print(data_df.corr())

#Chosen variables [ ConvertedComp, Age1stCode ] - independent variables; ['YearsCode'] - dependend variables
dep_var_num = ['Age1stCode', 'ConvertedComp']
dep_var_other = ['FizzBuzz', 'No', 'Yes, full-time', 'Yes, part-time']
indep_var_num = ['YearsCode']

#EX 2

#Replace text values to numercial data
data_df['FizzBuzz'].replace(to_replace={'Yes': '1', 'No': '0'}, inplace=True)

#Replace values via one-hot-encoding method
ohe_df = pd.get_dummies(data_df['Student'])
data_df.drop('Student', axis = 1, inplace=True)
data_df = data_df.join(ohe_df)

#EX 3

#Calc standard dev and mean for independent variables and remove outliers
mean = np.mean(data_df['ConvertedComp'])
st_dev = np.std(data_df['ConvertedComp'])
data_df = data_df[(data_df['ConvertedComp'] >= (mean - 3 * st_dev)) & (data_df['ConvertedComp'] <= (mean + 3 * st_dev))]

mean = np.mean(data_df['Age1stCode'])
st_dev = np.std(data_df['Age1stCode'])
data_df = data_df[(data_df['Age1stCode'] >= (mean - 5 * st_dev)) & (data_df['Age1stCode'] <= (mean + 5 * st_dev))]


#Use quantile to remove outliers from YearsCode
#data_df = data_df[(data_df['YearsCode'] >= data_df['YearsCode'].quantile(.15)) & (data_df['YearsCode'] <= data_df['YearsCode'].quantile(.85))]

#Create plots for numerical data one more time
#plot_dataframe(data_df, (indep_var_num + dep_var_num), 1)

#EX4 & EX5

#Create linear regression models & predict values
regression_model = linear_model.LinearRegression()
regression_model.fit(data_df[['Age1stCode']], data_df[indep_var_num])
data_df['Prediction_1'] = regression_model.predict(data_df[['Age1stCode']])

regression_model = linear_model.LinearRegression()
regression_model.fit(data_df[dep_var_num], data_df[indep_var_num])
data_df['Prediction_2'] = regression_model.predict(data_df[dep_var_num])

regression_model = linear_model.LinearRegression()
regression_model.fit(data_df[dep_var_num+dep_var_other], data_df[indep_var_num])
data_df['Prediction_3'] = regression_model.predict(data_df[dep_var_num+dep_var_other])

mse_data = {"one_var": mean_squared_error(data_df[indep_var_num], data_df['Prediction_1']),
            "two_vars": mean_squared_error(data_df[indep_var_num], data_df['Prediction_2']),
            "all_vars": mean_squared_error(data_df[indep_var_num], data_df['Prediction_3'])}
