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

def standardize(df):
    attrList = ['PersonalityTrait', 'Likes', 'DisLikes']

    # Change each nominal attribute to numeric and standardize the data
    for attribute in attrList:
        enc = LabelEncoder()
        enc.fit(df[attribute])
        df[attribute] = enc.transform(df[attribute])

    attrList = list(df.columns)
    df[attrList] = StandardScaler().fit_transform(df[attrList])

def calculate_PCA(dataFrame):
    del df["Type1"]
    del df["Type2"]
    standardize(dataFrame)

    attrList = list(dataFrame.columns)
    n_components = len(attrList)
    pca = PCA(n_components=n_components)
    pca.fit_transform(dataFrame[attrList])
    eigenvalues = pca.explained_variance_

    cos_two = np.zeros(shape=(n_components, 12))

    # first 12 Pricipal Components
    for n in range(0, 12):
        for m in range(len(pca.components_[n])):
            cos_two[m, n] = pca.components_[n][m] * pca.components_[n][m]

    # print(cos_two)
    # cos_two now holds the cos2 values for each attribute for the first 12 PCs
    percent_contribution_per_PC = np.zeros(shape=(n_components, 12))

    for n in range(0, 12):
        cos_two_col_sum = 0
        for m in range(n_components):
            cos_two_col_sum += cos_two[m,n]
        for m in range(n_components):
            percent_contribution_per_PC[m,n] = (cos_two[m,n] * 100)/cos_two_col_sum

    cumulative_contribution = np.zeros(shape=(n_components))
    
    for m in range(n_components):
        numerator = 0
        denominator = 0
        for n in range(0, 12):
            numerator += percent_contribution_per_PC[n,m] * eigenvalues[n]
            denominator += eigenvalues[n]
        cumulative_contribution[m] = numerator/denominator
    
    sortedAttrList = [x for _, x in sorted(zip(cumulative_contribution, attrList))]

    print(list(reversed(sorted(cumulative_contribution))))
    print("\nThe 12 most important attributes are: ", str(list(reversed(sortedAttrList[-12:]))))

def spearman_test(dataFrame):
    numeric_values = dataFrame.loc[:, ('Total','HP','Attack','Defense','SpAtk','SpDef','Speed','Generation','PersonalityTrait','Likes','DisLikes','Bonus')]
    independent_matrix = pd.DataFrame(columns=numeric_values.columns, index=numeric_values.columns)

    for x in range(len(numeric_values.columns)):
        for y in range(len(numeric_values.columns))[x:]:
            index = numeric_values.columns[x]
            columns = numeric_values.columns[y]

            corr, p_value = spearmanr(numeric_values[index], numeric_values[columns])
            
            if abs(corr) >= .5:
                independent_matrix[index][columns] = 'N'
            else:
                independent_matrix[index][columns] = 'I'

    print("\nSpearman test independence matrix:")
    print(independent_matrix)


if __name__ == "__main__":
    df = pd.read_csv("trenton_pokemon.csv")
    # standardize(df)
    spearman_test(df)
    # calculate_PCA(df)
    # Output the updated dataframe to a new csv
    df.to_csv("standardized.csv", index=False)