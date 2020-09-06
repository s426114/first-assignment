import pandas as pd
from pathlib import Path

#Import file and create dataframe
flat_df = pd.read_csv(Path(Path.cwd() / "train.tsv"),"\t", names=['Price', 'RoomNo', 'Area', 'Floor', 'Lozalization', 'Description'])

#Calc sq meter for every row & avg sq meter
flat_df['PriceSqMeter'] = round(flat_df['Price'] / flat_df['Area'] * 1000)
avg_sq_price = round(flat_df['PriceSqMeter'].mean())

#Save data to csv given exercise constraints
out_df = flat_df[['Price', 'RoomNo', 'PriceSqMeter']].loc[(flat_df['RoomNo'] >= 3) & (flat_df['PriceSqMeter'] < avg_sq_price)]
out_df.to_csv(Path(Path.cwd() / 'Exercise1' / 'out1.csv'), index=False, header=False)