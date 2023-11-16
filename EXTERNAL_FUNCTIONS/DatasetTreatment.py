import pandas as pd
import ast

def split_dict(row):
    '''
    This function splits a dictonnary in two distinct lists : list of the keys , list of the values 
    '''
    if not row : 
        keys, values = [], []
    else : 
        keys, values = zip(*row.items())
    return pd.Series({'Keys': list(keys), 'Values': list(values)})

def MovieDF_Treatment(MovieDF) :
    '''
    This function deals with the dataframe MovieDF
    '''
    df = MovieDF.copy(deep = True)
    #Movie languages 
    df['Movie languages'] = df['Movie languages'].apply(ast.literal_eval)
    df[['Freebase Language', 'Movie languages']] = df['Movie languages'].apply(split_dict)
    
    #Movie countrty 
    df['Movie countries'] = df['Movie countries'].apply(ast.literal_eval)
    df[['Freebase country', 'Movie countries']] = df['Movie countries'].apply(split_dict)
    #Movie genres 
    
    df['Movie genres'] = df['Movie genres'].apply(ast.literal_eval)
    df[['Freebase genre', 'Movie genres']] = df['Movie genres'].apply(split_dict)
    return df


def extract_top_firstname(name, valid_firstnames, name_occurrences_dict):
    if isinstance(name, str):
        names = name.split()
        firstnames = [n for n in names if n in valid_firstnames]
        if firstnames:
            top_firstname = max(firstnames, key=lambda n: name_occurrences_dict.get(n, 0))
            return top_firstname
    return None