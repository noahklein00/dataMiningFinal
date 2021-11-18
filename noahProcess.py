import pandas as pd

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

# if __name__ == "__main__":
#     df = pd.read_csv("Pokemon.csv")
#     processGeneration(df)
#     removeDuplicates(df)
#     removeWorthlessAttributes(df)
#     print(df)