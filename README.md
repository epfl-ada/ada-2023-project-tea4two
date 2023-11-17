## TITLE

Legacy of Earth civilization based on a movie dataset.

## ABSTRACT

What if aliens tried to guess what our civilization/society looked like long after we disappeared, thanks to the only document they have access to: a dataset of movies?
First, we see things from their perspective and draw up a robot-portrait of the average person on Earth/. Having constructed an image in the manner of extraterrestrial historians, we ask ourselves to what extent this image is realistic and representative of current society
We continue by investigating possible correlations or causal links between the names of the actors and of the population. What is the true nature of data collected by the aliens, are they only seeing the description of our society or something deeper than that ? 
Last, we would be interested in producing graphs of relationships between countries in the world, given only the synopses of the movies.
This eventually enables us to wonder what data would be most useful to leave as a legacy for other civilizations to understand human society.


## RESEARCH QUESTIONS

•	What should the typical human look like, if the only information we had about them was this dataset?
•	What does the information on names obtained by the aliens say about our society? Is there a correlation between babies’ names and actors’ names in films? If yes, is it possible to determine whether one of them causes the other?
•	Can we infer the main relations between countries by analysing synopses, and draw a weighted map of countries with respect to how strongly they interact with each other?
•	Can we elaborate a metric system that would rate the likelihood/representativity of pools of movies on different criteria about the Earth population? 
•	Can we spot biases linked to the fact that most movies are either produced or occur in the USA?


## COMPLEMENTARY DATASETS

In order to better understand the nature of the data that the extraterrestrials have recovered, we are comparing our data set with other datasets describing the reality of our society. 
We use additional datasets, namely one about the babies' firstnames in the USA classified by year; about 7MB. We also use additional data about the US population, as regards distributions of ages, ethnicities, heights, genders. Such data is quite light and does not require a huge dataset. 
Our goal is to extract most of the main dataset so that with a dataset extended by few data, Aliens could be able to draw valuable insights about human society and for example, build a robot portrait
We also use additional data about the US population, as regards distributions of ages, ethnicities, heights, and genders. Such data is quite light and does not require huge dataset. 

## METHODS

For task 1 (robot portrait), we mostly analyse the means of features (if continuous, like height) or the most represented ones (if categorical, like occupations).
For task 2 (a metric system that rates pools of movies): we have defined a metric for each of our current criteria (height, age, gender, ethnicity), and we have the reference data for the USA, to which we can compare pools of movies.
For task 3 (influence of actors’ names on babies’ names): we will first investigate simple correlations. We consider only the 100 most famous movies (ranked with their box-office revenue). Have some names appeared after these movies? We can think of Leia which did not exist before the Star Wars first trilogy, but was given to a few thousand babies afterwards. Are there only a few highly noticeable examples, or can we also observe little increases for already popular names? To evaluate the real impact and confirm or infirm our assumptions, we should use statistical tools such as tests and p-values.
For task 4 (building a graph of the relationship of countries): We plan to analyse the synopses (strings) to look for synopses that mention several countries and value the interactions between them (any type they be). Assuming high interaction go on with geographical proximity (historically, countries were closely related to their neighbours), we can then produce a theoretical map of countries. 


## TIMELINE AND ORGANIZATION WITHIN THE TEAM

We separated the whole team into subgroups to focus on our different tasks. 
Within each subgroup, we have defined precise timelines to reach our respective objectives in time for Milestones 2 and 3. However, we keep discussing all together on the big picture to maintain a global consistency within our work. Task 4 has not been tackled yet for milestone 2, since it is more complex and may benefit from the ADA lesson about handling text data.

Task 1: 
- Milestone 2: Define the characteristics of interest for the robot portrait. Extract the information about these features, at a certain time and place.
- Milestone 3: Elaborate an evolving robot portrait that changes with years and regions.

Task 2: 
- Milestone 2: Selection of 4 test criteria: age, gender, height, ethnicity & Definition of the metric for each criterion & Evaluation of a few movies with this process
- Milestone 3: Final selection of representative criteria & Evaluation of pools of movies & Understanding of reasons why types/genres of movies rank higher or lower & Finding the ideal subset of the CMU dataset?

Task 3: 
- Milestone 2: For 400 names given in the USA, study of the frequency of the names given in the babies population and the actors population. Plot of visible correlations: which come first?
- Milestone 3: Refinement of this study by region and years groups. Also focus on common names, for which the analysis might be tenuous, whereas original names like Leia are much less easy to study. Also, use of precise assumptions and statistical tools answer the question of causal links: did some movies likely result in increasing number of babies named 'XX'?

Task 4: 
- Milestone 2: No analysis performed yet.
- Milestone 3: Extraction of the strings contained in the synopses to establish frequency relationships between two or more countries.


## Questions for TAs (optional)


