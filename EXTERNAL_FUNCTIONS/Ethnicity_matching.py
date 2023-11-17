import pandas as pd
import numpy as np
import os
import json
import ast
import math 
import time 
import requests

#This file is used to generate a csv which matches freebase id of ethnicities to the actual english name 
characterDF,movieDF,nameDF,plotDF,tvtropDF = DataImport.OpenMainMovieDatasetDF(PATH_IN)

def FreeBase(key):
    '''
    The functions looks on the Wikidata freebase and gives the name of the page corresponding to the key provided 
    '''
    time.sleep(1) #Avoid the timeout errors 
    try :
        if isinstance(key,float) : 
            return ''
        key = "'"+str(key)+"'"
        url = "https://query.wikidata.org/sparql"
        query = """SELECT  ?sLabel WHERE {
                        VALUES ?id {"""+key+"""} 
                        ?s wdt:P646 ?id .
                            SERVICE wikibase:label {bd:serviceParam wikibase:language "en" .}
                            }
        """
        r = requests.post(url, params = { 'format': 'json','query': query})
        r = r.json()
        if len(r['results']['bindings'])==0 : 
            # The query didn't give any results
            return '' 
        else : 
            return r['results']['bindings'][0]['sLabel']['value']
    except : 
        print('ERROR')
        print(r)
        print(key)

Unique_ethnics = characterDF[['Actor ethnicity']].dropna().drop_duplicates()
Unique_ethnics['ethinicty (en)'] = Unique_ethnics['Actor ethnicity'].apply(FreeBase)
Unique_ethnics.to_csv('ethnicity.csv',index = False)

