######################
# IC # 4 # Pandas and Numpy data cleaning
#############################
# Sabrina Akter # 9/30/2026 #

# Imports
import pandas as pd
import numpy as np


# Load csv
df = pd.read_csv("eye_health.csv")


# Print csv stats before cleaning
print(
    df.shape,
    df.dtypes,
    df.isna().sum(),  # Print total number of NaN values
    df.nunique(),
    sep="\n"
)


# Print number of duplicated values
print("Duplicates:", df.duplicated().sum())


# Drop columns with no data (only NaN)
df = df.dropna(axis=1, how="all")


# Drop columns that end in "ID"
df = df.drop(columns=[c for c in df.columns if c.endswith("ID")])


# Drop rows with no value in the column "Data_Value"
df = df.dropna(subset=["Data_Value"])


# Drop unnecessary columns
df = df.drop(
    columns=[
        "Geolocation",
        "Data_Value_Footnote_Symbol",
        "Data_Value_Footnote",
        "StateAbbr",
        "NonWeightedSample",
        "Geographic Level",
        "Numerator"
    ]
)


# Make column headers snake_case
df.columns = df.columns.str.lower().str.replace(" ", "_")


# Create new column "error"
df["error"] = (
    df["high_confidence_limit"] -
    df["low_confidence_limit"]
) / 2


# Create prevalence level description
df["prevalence_level"] = np.select(
    condlist=[
        df["data_value"] < 5,
        df["data_value"] <= 7
    ],
    choicelist=[
        "Low",
        "Medium"
    ],
    default="High"
)


# Save cleaned dataframe to a new CSV file
df.to_csv(
    path_or_buf="eye_health_2022_clean.csv",
    index=False
)


# Check that saved CSV has the same shape as dataframe
print(
    pd.read_csv("eye_health_2022_clean.csv").shape == df.shape
)