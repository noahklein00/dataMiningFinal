import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from feature_engine.discretisation import EqualWidthDiscretiser
from feature_engine.discretisation import EqualFrequencyDiscretiser

from scipy.stats import chi2_contingency
from scipy.stats import chi2
from scipy.stats import spearmanr

# Changes unknown generation values to valid generations based off of location in the list
# Assumes Pokemon are listed in order
def processGeneration(df):
    generationCol = df.loc[:, ('Generation')].copy()
    print(generationCol.unique())
    for i in range(len(generationCol)):
        if generationCol[i] == "?":
            if generationCol[i-1] == generationCol[i+1]:
                generationCol[i] = generationCol[i-1]
    
    df.loc[:, ('Generation')] = generationCol
    generationCol = df.loc[:, ('Generation')].copy()
    print(generationCol.unique())
    return df

def removeDuplicates(df):
    # 395 is Walnut, 715 is duplicate of KeldeoResolute Forme
    df.drop(labels=[395, 715], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def removeWorthlessAttributes(df):
    del df["ID"]
    del df["Name"]
    del df["EyeColor"]
    del df["Legendary"]
    return df

def combineDecision(df):
    df['combinedDecision'] = df[['Type1', 'Type2']].agg(' '.join, axis=1)
    del df["Type1"]
    del df["Type2"]
    return df

def removeMoreAttributes(df):
    del df["HP"]
    del df["Attack"]
    del df["Defense"]
    del df["SpAtk"]
    del df["SpDef"]
    del df["Speed"]
    return df

def binTotalAndBonus(df):
    disc = EqualWidthDiscretiser(bins=9, variables=['Total'], return_object=True)
    dataCopy = df.loc[:].copy()
    dataCopy = disc.fit_transform(dataCopy)

    df.loc[:] = dataCopy 

    disc = EqualWidthDiscretiser(bins=16, variables=['Bonus'], return_object=True)
    dataCopy = df.loc[:].copy()
    dataCopy = disc.fit_transform(dataCopy)

    df.loc[:] = dataCopy 
    return df 

def changeToString(df):
    df['Total'] = df['Total'].astype(str)
    df['Generation'] = df['Generation'].astype(str)
    df['Bonus'] = df['Bonus'].astype(str)

    totalCol = df.loc[:, ('Total')].copy()
    generationCol = df.loc[:, ('Generation')].copy()
    bonusCol = df.loc[:, ('Bonus')].copy()
    for i in range(df.shape[0]):
        totalCol[i] = totalCol[i] + "b"
        generationCol[i] = generationCol[i] + "b"
        bonusCol[i] = bonusCol[i] + "b"

    df.loc[:, ('Total')] = totalCol
    df.loc[:, ('Generation')] = generationCol
    df.loc[:, ('Bonus')] = bonusCol
    return df

if __name__ == "__main__":
    df = pd.read_csv("cleanedPokemon.csv")
    df = binTotalAndBonus(df)
    df = changeToString(df)
    df.to_csv("binnedPokemon.csv", index=False)
    # print(df)