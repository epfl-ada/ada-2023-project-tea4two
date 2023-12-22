#In this file we store all the functions used to make robot portrait of our average human 
import networkx as nx
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import statsmodels.formula.api as smf



#Functions for the regression on two movies 

def map(ref,elem): 
    '''
    Return the indices of the element elem in list ref 
    '''
    n = len(ref)
    for k in range(n) : 
        if ref[k] == elem : 
            return k 
    return None 

def Linear_reg_results(data,genre_lst,Ref): 
    '''
    This function computes the linear regression on the dataset 'data' filtered to keep only the genres from genre_lst 
    It runs the linear regression on movie_genres by taking as a renfernce the genre provided in the argument 'Ref
    '''
    #Filtering the dataset 

    reg_data = data[data['Movie_genres'].isin(genre_lst)]
    print('Movie_box_office_revenue_scaled ~ C(Movie_genres, Treatment('+Ref+'))')

    #Computes the linear regression 
    model = smf.ols(formula='Movie_box_office_revenue_scaled ~ C(Movie_genres, Treatment('+Ref+'))', data=reg_data).fit() 
    #Extraction of the results of the linear regression 
    reg_var = model.params.index[1:]
    reg_coef = model.params.values[1:]
    reg_pvalues = model.pvalues[1:]
    reg_sigma = model.bse.values[1:]
    reg_confidence = model.conf_int()[1:]
    Reg_res = pd.DataFrame(list(zip(reg_var, reg_coef, reg_pvalues,reg_sigma,reg_confidence[0],reg_confidence[1])),
              columns=['reg_var','reg_coef', 'reg_pvalues','reg_sigma','Lower_confidence','Higher_confidence'])
    
    return Reg_res 

def Linear_reg_plotting(Reg_res):
    '''
    This function takes into argument the dataframe with the results of the linear regression written in Linear_reg_results and plots all the coefficient of the linear regression 
    '''

    Reg_res = Reg_res.sort_values(by='reg_coef',ascending=True)

    #We rearrange a bit the labels to make it more readable 
    Reg_res['reg_var'] = Reg_res['reg_var'].str.replace('C(Movie_genres, Treatment("Drama"))[T.', '')
    Reg_res['reg_var'] = Reg_res['reg_var'].str.replace(']', '')


    #Plotting of the results 
    fig = plt.figure(figsize=(10,30))

    Reg_res['Err_Lower_confidence'] = Reg_res['Lower_confidence'] - Reg_res['reg_coef']
    Reg_res['Err_Higher_confidence'] = Reg_res['Higher_confidence'] - Reg_res['reg_coef']
    errors = np.abs(Reg_res[['Err_Lower_confidence','Err_Higher_confidence']].to_numpy()).T

    #We are using the 95% confidence interval to compute the error bars
    plt.errorbar(Reg_res['reg_coef'],Reg_res['reg_var'],xerr = errors,linestyle = 'none',marker = 'o',markeredgecolor = 'black')


    plt.vlines(0,0, len(Reg_res['reg_var']), linestyle = '--')
    plt.title('Distribution of features coefficients that influence Movie box office revenue')

    plt.ylim((-1,len(Reg_res['reg_var'])))
    plt.show()

def Linear_reg_duels(Genre_list,data):
    '''
    This function takes in argumnet Genre_list which is all the genres you want to compare between them and data wich is your dataset.
    It runs multiple linear regressions each time by tacking as a reference one element from the list Genre_list. 
    For each linear regression we keep only the three genres with the highest coefficient and the three genres with the lowest. We give three points to the best, two points to the second best 
    and 1 point to the third best. Then we return two matrices with the refernce genre on the y axis and the best or worst genre in the x axis. 
    '''

    n = len(Genre_list)
    res_pos = np.zeros((n,n))
    res_neg = np.zeros((n,n))
    for genre in Genre_list : 
        genre_str ='"' +genre+'"'
        #We do the linear regression 
        Reg_res = Linear_reg_results(data,Genre_list,genre_str)
        Reg_res = Reg_res.sort_values(by='reg_coef',ascending=False)

        Reg_res['reg_var'] = Reg_res['reg_var'].str.replace('C(Movie_genres, Treatment('+genre_str+'))[T.', '')
        Reg_res['reg_var'] = Reg_res['reg_var'].str.replace(']', '')
        best_1 = Reg_res['reg_var'].iloc[0]
        best_2 = Reg_res['reg_var'].iloc[1]
        best_3 = Reg_res['reg_var'].iloc[2]
        worst_1 = Reg_res['reg_var'].iloc[-1]
        worst_2 = Reg_res['reg_var'].iloc[-2]
        worst_3 = Reg_res['reg_var'].iloc[-3]
        if Reg_res['reg_coef'].iloc[0] > 0 and Reg_res['Lower_confidence'].iloc[0] >0 : 
            res_pos[map(Genre_list,genre)][map(Genre_list,best_1)] += 3 
        
        if Reg_res['reg_coef'].iloc[1] > 0 and Reg_res['Lower_confidence'].iloc[1] >0 : 
            res_pos[map(Genre_list,genre)][map(Genre_list,best_2)] += 2 

        if Reg_res['reg_coef'].iloc[2] > 0 and Reg_res['Lower_confidence'].iloc[2] >0 : 
            res_pos[map(Genre_list,genre)][map(Genre_list,best_3)] += 1 

        if Reg_res['reg_coef'].iloc[-1] < 0 and Reg_res['Higher_confidence'].iloc[-1] < 0 : 
            res_neg[map(Genre_list,genre)][map(Genre_list,worst_1)] += -3 
        
        if Reg_res['reg_coef'].iloc[-2] < 0 and Reg_res['Higher_confidence'].iloc[-2] < 0 : 
            res_neg[map(Genre_list,genre)][map(Genre_list,worst_2)] += -2 
        
        if Reg_res['reg_coef'].iloc[-3] < 0 and Reg_res['Higher_confidence'].iloc[-3] < 0 : 
            res_neg[map(Genre_list,genre)][map(Genre_list,worst_3)] += -1 
            
    return res_pos, res_neg 









#Functions used for the pair matching 

def score(lst1,lst2):
    '''
    Evaluates the distance between two lists 
    '''
    if len(lst1) == 0 or len(lst2) == 0 : 
        return 0
    intersect = 0 
    for elem in lst1 : 
        if elem in lst2 : 
            intersect += 1
    return intersect/max(len(lst1),len(lst2))

def matching(genre1, genre2, df):

    '''
    Matches movies of genre 1 with movies of genre 2 whith similar languages and similar country of origin 
    Returns the dataset containign all the matched samples 
    '''
    #arbitrary treshold to assure that the movies we are mathcing have a sensible similarity 
    treshold = 1.5
    df_genre1 = df[df['Movie_genres']==genre1]
    df_genre2 = df[df['Movie_genres']==genre2]
    G = nx.Graph()
    for idx1, movie1 in df_genre1.iterrows() : 
        for idx2, movie2 in df_genre2.iterrows() : 
            if movie2['Wikipedia movie ID'] == movie1['Wikipedia movie ID'] :
                continue

            similarity = score(movie1['Movie languages'],movie2['Movie languages']) + score(movie1['Movie countries'],movie2['Movie countries'])
            if similarity >= treshold : 
                G.add_weighted_edges_from([(movie1['Wikipedia movie ID'], movie2['Wikipedia movie ID'], similarity)])


    
    matching = nx.max_weight_matching(G)
    matched = [i[0] for i in list(matching)] + [i[1] for i in list(matching)]

    return df[df['Wikipedia movie ID'].isin(matched) & df['Movie_genres'].isin([genre1,genre2])]



def Significance_of_genre(data,genre_lst,genre1,genre2):
    '''
    Matches movies of genre1 and genre2 together before running a linear regression to asses or not if the two genres have a meaninful influence on the succes of a movie
    '''

    reg_data = data[data['Movie_genres'].isin(genre_lst)]
    Matched = matching(genre1,genre2,reg_data)
    genre_str ='"' +genre1+'"'
    print('Movie_box_office_revenue_scaled ~ C(Movie_genres, Treatment('+genre_str+'))')
    matched_reg = smf.ols(formula='Movie_box_office_revenue_scaled ~ C(Movie_genres, Treatment('+genre_str+'))', data=Matched).fit() 

    p_val = matched_reg.pvalues[1]
    coef = matched_reg.params.values[1]
    if p_val<0.005: 
        if coef <0 : 
            print(genre2 + ' drives higher sucess than '+ genre1 )
        if coef>0: 
            print(genre1 + ' drives higher sucess than '+ genre2 )
    else : 
        print("The matching doesn't allow us to say if their is a significant differences between " + genre1 +' and '+genre2)
    return p_val 


