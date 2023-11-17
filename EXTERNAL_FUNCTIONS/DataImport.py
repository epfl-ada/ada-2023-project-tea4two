import os
import json
import pandas as pd

def OpenMainMovieDatasetDF(PATH):
    '''
    This function opens the dataframes stored in the file with location PATH
    '''
    
    character_file = os.path.join(PATH, 'character.metadata.tsv')
    movie_file = os.path.join(PATH, 'movie.metadata.tsv')
    name_file = os.path.join(PATH, 'name.clusters.txt')
    plot_file = os.path.join(PATH, 'plot_summaries.txt')
    tvtrop_file = os.path.join(PATH, 'tvtropes.clusters.txt')

    movie_col = ["Wikipedia movie ID", "Freebase movie ID", "Movie name", "Movie release date",
                  "Movie box office revenue", "Movie runtime", "Movie languages", "Movie countries",
                  "Movie genres"]

    character_col = ["Wikipedia movie ID", "Freebase movie ID", "Movie release date", "Character Name", "Actor DOB",
                     "Actor gender", "Actor height", "Actor ethnicity", "Actor Name",
                     "Actor age at movie release", "Freebase character map"]
    name_col = ["Character Name", "Freebase character map"]

    plot_col = ["Wikipedia movie ID", "Plot"]

    characterDF = pd.read_table(character_file, names=character_col, index_col=False)
    movieDF = pd.read_table(movie_file, names=movie_col, index_col=False)
    nameDF = pd.read_csv(name_file, sep="\t", names=name_col, index_col=False)
    plotDF = pd.read_csv(plot_file, sep="\t", names=plot_col, index_col=False)

    tvtrop_f = open(tvtrop_file)
    lines = tvtrop_f.readlines()
    tvtrop_f.close()
    tvtropDF = pd.DataFrame(columns=["stereotype", "char", "movie", "id", "actor"])
    for line in lines:
        char_type, dico = line.split("\t")
        dico = json.loads(dico)
        dico["stereotype"] = char_type
        tvtropDF = pd.concat([tvtropDF, pd.DataFrame([dico])], ignore_index=True)

    return characterDF, movieDF, nameDF, plotDF, tvtropDF


def FillMissingValues(target_df, source_df, target_column, source_column):
    # Calculate percentage of missing values before filling
    before_fill_percentage = target_df[target_column].isnull().mean() * 100
    
    target_df[target_column] = target_df[target_column].fillna(source_df[source_column])

    # Calculate percentage of missing values after filling
    after_fill_percentage = target_df[target_column].isnull().mean() * 100

    # Calculate the percentage improvement
    improvement_percentage = before_fill_percentage - after_fill_percentage

    # Print the results
    print(f"Percentage of missing values before fill: {before_fill_percentage:.2f}%")
    print(f"Percentage of missing values after fill: {after_fill_percentage:.2f}%")
    print(f"Percentage improvement: {improvement_percentage:.2f}%")

    return target_df