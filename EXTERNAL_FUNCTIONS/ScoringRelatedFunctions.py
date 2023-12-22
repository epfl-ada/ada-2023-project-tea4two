import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import isnan

"""
This file contains the main functions used to score pools of movies depending on the parity, diversity, 
age and height distribution.
"""


####################################
#####  Scoring functions   #########
####################################


def scoring_function(value, target, p, sigma):
    """ Scoring function.
    
    @arg
        value : value between 0 and 1, given by the pool of movie (e.g. frequency)
        target : corresponding target value between 0 and 1, given by statistic on real world
        p : the higher it is, the longer the plateau near the central value is
        sigma : the higher it is, the stronger the thresholding is
    
    @output
        score : between 0 (if value very far from target) and 1 (if value==target)
                The score is not linearly linked with the diffence |value - target|:
                for instance, the score is about 0.5 if a difference of 15% is observed between value and target.
    """
    dist = value-target
    x = 0.5+dist
    if (x<0 or x>1):
        return 0
    return (np.exp(-sigma*np.abs(2*x-1)**p)*np.cos(np.pi/2*(2*x-1)))

def standardized_score(score, min_score=0, max_score=0):
    """
    Return the normalized score with the following cutoff : 1 if @score >= @max_score
                                                            0 if @score <= @min_score
    """
    standardized_score=(score-min_score)/(max_score-min_score)
    if standardized_score<0:
        standardized_score=0
    elif standardized_score>1:
        standardized_score=1
    return standardized_score



def parity_score(pool, ref, p=3, sigma=20):
    
    """
    Return a value between 0 (if only one gender) and 1 (if parity is exactly the same as in @ref),
    using the scoring_function with parameters @p and @sigma.
    """
    
    p_F_ref = ref['F'] # reference value for women proportion
    p_F = pool['Actor gender'].dropna().apply(lambda x: x=="F").mean() #proportion of women in the movie pool

    return {'par':scoring_function(p_F,p_F_ref,p,sigma)}






def diversity_score(pool, ref=None):
    """
    Comute the number of ethnicities over the total number of actors.
    If >75%, the score returns 1.
    If <25%, the score returns 0.
    """
    div_pool=pool.dropna(subset=['Ethnicity'])
    score=0
    nb_eth = div_pool.groupby('Ethnicity').count().shape[0]
    nb_act = div_pool.shape[0]
    if nb_act!=0:
        score = nb_eth/nb_act

    return {'div':standardized_score(score,min_score=0.25,max_score=0.75)}


 



def age_score(pool, ref, p=2.5, sigma=500):
    """
    function to evaluate the difference between the age distribution of the actors in the movie
    and the real distribution, using the scoring_function with parameters @p and @sigma.

    @arguments
        pool : dataframe containing the pool of movie that will be scored
        ref : tool containing the reference for age distribution
        p : the higher it is, the longer the plateau near the central value is
        sigma : the higher it is, the stronger the thresholding is

    @outputs
        age_sc = unitarized age score evaluation. If equal 1, the distribution is exactly the ref

    """
    # Creation of age ranges
    age_ranges = range(0,80,5)
    Nb_bin = len(age_ranges)
    
    # Separation of the pool depending on the gender
    pool_M = pool[pool["Actor gender"]=='M']
    pool_F = pool[pool["Actor gender"]=='F']
    
    # Recuperation of reference frequencies for each age range depending on the gender
    freq_ref_M = ref['M']
    freq_ref_F = ref['F']
    weights = [5,5,5,5,1,1,1,1,1,3,3,3,3,5,5,5,5]
    
    # Recuperation of men proportion in the pool for gender weighting
    p_M = pool['Actor gender'].apply(lambda x: x=="M").mean()
    age_sc_M=0
    if p_M!=0:
        cmu_age_M = pool_M['Actor age at movie release'].dropna()
        freq_cmu_M = np.histogram(cmu_age_M, bins = age_ranges, density = True)
        for i in range(Nb_bin-1):
            age_sc_M += scoring_function(freq_cmu_M[0][i],freq_ref_M[i],p,sigma)*weights[i]
        age_sc_M = age_sc_M/sum(weights)
    
    age_sc_F=0
    if p_M!=1:
        cmu_age_F = pool_F['Actor age at movie release'].dropna()
        freq_cmu_F = np.histogram(cmu_age_F, bins = age_ranges, density = True)
        age_sc_F = 0
        for i in range(Nb_bin-1):
            age_sc_F += scoring_function(freq_cmu_F[0][i],freq_ref_F[i],p,sigma)*weights[i]
        age_sc_F = age_sc_F/sum(weights)
    
    return {'AGE':p_M*age_sc_M+(1-p_M)*age_sc_F}



def rescued_age_score(pool, ref, p=2.5, sigma=500,
                      min_score=0.12, max_score=0.35):
    """
    Apply a standardization to age_score to center and widen the distribution's spread.
    The initial distribution is considered to goes from @min_score to @max_score.
    """
    score = age_score(pool,ref,p,sigma)['AGE']
    return {'age':standardized_score(score,min_score,max_score)}







def height_score(pool, ref, p=3, sigma=50):
    """
    Function to evaluate the difference between the age distribution of the actors in the movie
    and the real distribution.
    Do the histogram area difference (it then also penalize too high representation of some ages),
    using the scoring_function with parameters @p and @sigma.

    @arguments
        pool : dataframe containing the pool of movie that will be scored
        ref : tool containing the reference for age distribution
        p : the higher it is, the longer the plateau near the central value is
        sigma : the lower it is, the stronger the thresholding is

    @outputs
        hei_sc = unitarized height score evaluation.

    """
    # Creation of height ranges
    hei_ranges = range(142,193,3)
    Nb_bin = len(hei_ranges)
    
    # Separation of the pool depending on the gender
    pool_M = pool[pool["Actor gender"]=='M']
    pool_F = pool[pool["Actor gender"]=='F']
    
    # Reference frequencies for each height range depending on the gender
    freq_ref_M = ref['M']
    freq_ref_F = ref['F']
    weights = [3,3,3,3,2,2,1,1,1,2,2,2,3,3,3,3,3]
    
    # Recuperation of men proportion in the pool for gender weighting
    p_M = pool['Actor gender'].apply(lambda x: x=="M").mean()
    hei_sc_M=0
    if p_M!=0:
        cmu_hei_M = pool_M['Actor height'].dropna()*100
        freq_cmu_M = np.histogram(cmu_hei_M, bins = hei_ranges, density = True)
        for i in range(Nb_bin-1):
            hei_sc_M += scoring_function(freq_cmu_M[0][i],freq_ref_M[i],p,sigma)*weights[i]
        hei_sc_M = hei_sc_M/sum(weights)
    
    hei_sc_F = 0
    if p_M!=1:
        cmu_hei_F = pool_F['Actor height'].dropna()*100
        freq_cmu_F = np.histogram(cmu_hei_F, bins = hei_ranges)

        for i in range(Nb_bin-1):
            hei_sc_F += scoring_function(freq_cmu_F[0][i],freq_ref_F[i],p,sigma)*weights[i]
        hei_sc_F = hei_sc_F/sum(weights)
    
    return {'HEI':p_M*hei_sc_M+(1-p_M)*hei_sc_F}



def rescued_height_score(pool, ref, p=3, sigma=50,
                         min_score=0.5, max_score=0.9):
    """
    Apply a standardization to height_score to center and widen the distribution's spread.
    The initial distribution is considered to goes from @min_score to @max_score.
    """
    score = height_score(pool,ref,p,sigma)['HEI']
    
    return {'hei':standardized_score(score,min_score,max_score)}







## Weighting of each score for the final aggregation
# standard weights
par_w = 2
div_w = 2
age_w = 1
hei_w = 1

weights_dic={'par':par_w, 'div':div_w, 'age':age_w, 'hei':hei_w}

def representativeness_score(pool, ref, weights=weights_dic):
    """
    Weighting and aggregation of every single score to produce the final score of @pool, 
    between 0 (the movie clearly do not represent our civilization) and 100 (it perfectly
    fits to @ref values).
    The criteria that are taken into account are given in @weights.
    """

    scores={}
    agg_score=0
    weights_sum=0
    for key in weights:
        if key=='div':
            score = function_dic[key](pool)[key]
        else: 
            score = function_dic[key](pool,ref[key])[key]
        scores[key]=score
        agg_score+=weights[key]*score
        weights_sum+=weights[key]

    agg_score = agg_score/weights_sum
    if isnan(agg_score):
        agg_score=0
    scores['tot']=int(agg_score*100)
    
    return scores


function_dic={'par':parity_score,
              'div':diversity_score,
              'AGE':age_score,
              'age':rescued_age_score,
              'HEI':height_score,
              'hei':rescued_height_score,
              'tot':representativeness_score}



############################################################
##  Functions to fid score distribution of numerous pools ##
############################################################


POOL_SIZE = 20
N_TEST = 1000

def defined_movie_pool(movies_id, df):
    """
    Extract the actors of movies whose id is in @movies_id.
    """
    pool = df[df['Wikipedia movie ID'].isin(movies_id)]
    return pool


def random_movie_pool(film_pool_size, df):
    """
    Extract the actors of @pool_size random movies.
    """
    movies_id = np.random.choice(df['Wikipedia movie ID'].unique(),
                                  size=film_pool_size, replace=False)
    return defined_movie_pool(movies_id, df)

def scores_distribution(score_id, df, ref, n_test=N_TEST, pool_size=POOL_SIZE, plot=True):
    """
    Plot the distribution of scores according to @score_function.
    Extract @n_test pools of @pool_size movies and assess the corresponding score.
    """
    scores_list={'pool':[]}
    score_function = function_dic[score_id]
    for i in range(n_test):
        if (i%10000==0 and i!=0):
            print("n_test = "+i)
        P = random_movie_pool(pool_size, df)
        if score_id=='tot':
            dic = score_function(P, ref)
        else:
            dic = score_function(P, ref[score_id])
        for key in dic:
            if key not in scores_list:
                scores_list[key]=[]
            scores_list[key].append(dic[key])
        scores_list['pool'].append(P['Wikipedia movie ID'].unique())
    
    if plot:
        for key in dic:
            if key!='pool':
                plt.hist(scores_list[key],bins=10)
                plt.title(f"{function_dic[key].__name__} distribution for {n_test} random pools of {pool_size} movies")
                plt.xlabel(f"{function_dic[key].__name__} result")
                plt.ylabel("Number of occurences")
                plt.show()

    return scores_list



###########################################################
#######  Functions to find optimal pools of movies  #######
###########################################################


def improvement(df, ref, initial_movies_id, old_score):
    """
    This function takes the pool with @initial_movies, with a score of @old_score,
    screen for each movie in our dataset and find the movie that increase at most the score.
    
    Outputs :
        @best_movie_id : a list containing movie id of the initial_movies plus the new movie id
        
        @new_sc : the new score of the pool @best_movie_id
        
    """
    best_movies_id = initial_movies_id
    diff_max = -100
    movie_count=0
    for movie_id in df['Wikipedia movie ID'].unique():
        if movie_id not in best_movies_id:
            movie_count+=1
            new_movies_id = initial_movies_id+[movie_id]
            actors_pool = defined_movie_pool(new_movies_id, df)
            new_score = representativeness_score(actors_pool, ref)['tot']
            diff= new_score-old_score
            if diff>diff_max:
                best_movies_id = new_movies_id
                diff_max=diff
                #print(f"The old score was {old_score}, the new one is {new_score},"+
                #      f" obtained by adding the movie {movie}.")
    new_sc = old_score+diff_max
    return best_movies_id,


def best_pool(df, ref, initial_size=10, final_size=20):
    """
    Improving a random very good pool of @initial_size movies by applying the function 'improvement'
    until the number of movies in the pool is @final_size.
    """
    final_pool0 = [19845179, 1635059, 2363899, 10780834, 1598832, 9976121,1745419, 1332050, 22565598, 68078,
               17470965, 256713, 28224334, 10771128, 1940449, 24863901, 20334086, 30575, 8309714, 6792375]
    final_pool1 = [13439139, 25698427, 2507687, 4360088, 28150124, 24028744, 11929259, 303039, 2231977, 20603201,
               12576817, 20334086, 571383, 1940449, 4459059, 22697314, 8309714, 30575, 5566878, 33933454]
    final_pool2 = [768526, 28224334, 12244463, 1131021, 4750927, 27718464, 25901625, 642694, 7680880, 35938622,
               4939088, 17981954, 22747963, 2980843, 30012817, 16958933, 10771128, 22916442, 20334086, 5026441]
    final_pool3 = [8495088, 2367208, 6900343, 21211657, 3461278, 23325348, 2363899, 11843126, 1172681, 76630,
               13285237, 26057620, 1829909, 14075290, 23318059, 165106, 20334086, 33933454, 16852170, 217793]
    final_pool4 = [2292864, 32291194, 26852809, 779774, 3466113, 766887, 607444, 18410798, 1954484, 21591619,
               4018288, 6302550, 20334086, 33933454, 2797638, 1940449, 24863901, 580994, 30462894, 29585091]
    final_pool5 = [5006061, 571383, 617063, 17671802, 16852170, 17365387, 443011, 13610284, 461353, 3954298,
               1531473, 22916442, 5664063, 14075290, 8309714, 20334086, 33933454, 19115982, 16958933, 1940449]
    final_pool6 = [1470810, 7902455, 5243359, 10048256, 11048780, 11036762, 5118135, 431562, 4018288, 33410925,
               20334086, 24863901, 32832210, 4459059, 1940449, 5894429, 14075290, 5566878, 15670779, 33933454]
    final_pool7 = [23243012, 62668, 2184642, 35527324, 8425973, 4922371, 2563837, 12009929, 13779507, 591310,
               5566878, 21639537, 9653770, 20334086, 1940449, 14075290, 10771128, 33933454, 5664063]
    final_pool8 = [483745, 3788150, 17789399, 5230818, 7432079, 8246088, 1599839, 3414692, 4294005, 2964227, 
               10771128, 8309714, 5894429, 20334086, 14075290, 1940449, 4459059, 1717731, 33933454, 30462894]
    final_pool9 = [19890229, 2581365, 73412, 161897, 3779953, 25829166, 1717731, 3037946, 4299492, 1745413,
               8940771, 14075290, 10771128, 20334086, 8309714, 30575, 571383, 4459059, 320502, 5664063]
    final_pool10 = [5071341, 8388013, 6742643, 5496661, 1367413, 15809123, 14644393, 133622, 5897288, 25359124,
                171559, 4744688, 4939088, 20334086, 33933454, 26057620, 5894429, 320502, 24863901, 27634924]

    '''

    BROKEN ON MERGED VERSION
    WE USED BACKUPS MADE ON A WORKING VERSION

    #Getting scores for pools of initial_size movies
    n_test=1000
    scores = scores_distribution('tot', df, ref, n_test=n_test, pool_size=initial_size,plot=False)

    # extracting the first pool with the maximal score
    max_score = max(scores['tot'])
    max_index = scores['tot'].index(max_score)
    initial_movies_id = scores['pool'][max_index]

    print(f'The maximal score is {max_score}, corresponding to the following pool : {initial_movies_id}.')
    
    for i in range(final_size-initial_size):
        initial_movies_id, max_score=improvement(df, ref, initial_movies_id, max_score)
        print(f"Improvement {i+1} : adding movie {initial_movies_id[-1]} gives a new score of {max_score}.")
    return initial_movies_id
    '''

    return final_pool3


#########################################
#####  Function for genre study #########
#########################################

def most_common_movieIDents(lst, n=5):
    """
    Returns the @n most numerous movie genres in @list, as well as their multiplicities
    """
    counter = Counter(lst)
    return counter.most_common(n)


