import pandas as pd
from pathlib import Path

#Import files and create dataframes
flat_df = pd.read_csv(Path(Path.cwd() / "train.tsv"),"\t", names=['Price', 'RoomNo', 'Area', 'Floor', 'Lozalization', 'Description'])
info_df = pd.read_csv(Path(Path.cwd() / "description.csv"),",")

#Merge dataframes and save to out3.csv file given exercise restrictions
out_df = pd.merge(flat_df, info_df, left_on=["Floor"], right_on=["liczba"]).drop(columns=["liczba"])
out_df.to_csv(Path(Path.cwd() / 'Exercise1' / 'out2.csv'), index=False, header=False)