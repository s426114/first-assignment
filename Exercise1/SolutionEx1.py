import pandas as pd
from pathlib import Path

#Import file and create dataframe
flat_df = pd.read_csv(Path(Path.cwd() / "train.tsv"),"\t", names=['Price', 'RoomNo', 'Area', 'Floor', 'Lozalization', 'Description'])

#Calculate average flat price and store value in out0.csv file
with open("./Exercise1/out0.csv", 'w') as out:
    out.write(str(round(flat_df['Price'].mean())))
