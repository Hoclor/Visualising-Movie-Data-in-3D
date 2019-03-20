# PadX/PadY pads from both sides
# Cells in rows/columns fill up, e.g. set row1 and row5 pushes row5 into the position of row2. Define the empty rows with minwidth
# Contents that overfill a cell pushes the entire column/row to be wider, not just that cell

# Visualization ideas:
# Let user select two movies, produce 2D graph plot of people who have rated both movies and with their ratings
# (allows investigation of correlation between movies)
#
# Plot a 3D scatter plot, one vertex for each genre, edges connecting genres with size correlating to how many movies have both those genres
# Computational steering: Select two genres, plot 3D scatter plot of movies with those two genres and a third (for every other genre)
#
import pandas as pd
import numpy as np
from tkinter import *
import time


# Data extraction and filtering

def read_dataset(nrows= 30000000):
    if nrows <= 27000000:
        print("Reading and filtering limited dataset from csv files")
    else:
        print("Reading and filtering dataset from csv files")
    # Read the movielens dataset in using pandas
    movies = pd.read_csv('movielens_dataset/movies.csv', nrows=nrows)
    tags = pd.read_csv('movielens_dataset/tags.csv', nrows=nrows)
    ratings = pd.read_csv('movielens_dataset/ratings.csv', nrows=nrows)

    # Clean the data - only tags has some null values
    tags = tags.dropna()

    # Separate the movies titles into titles and years
    movies['year'] = movies['title'].str.extract('.*\(([0-9]*)\).*', expand = False)
    movies['title'] = movies['title'].str.extract('(.*) \([0-9]*\).*', expand = False)

    # Convert the genres field from a string of genres to individual columns
    # list of all genres
    genres_unique = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    genres_unique = pd.DataFrame(movies.genres.str.split('|').tolist()).stack().unique()
    genres_unique = pd.DataFrame(genres_unique, columns=['genre']) # Format into DataFrame to store later
    movies = movies.join(movies.genres.str.get_dummies().astype(bool))
    movies.drop('genres', inplace=True, axis=1)
    # Drop the '(no genres listed)' column
    if '(no genres listed)' in movies.columns:
        movies.drop('(no genres listed)', inplace=True, axis=1)

    # Modify timestamps to be in terms of years
    ratings.timestamp = pd.to_datetime(ratings.timestamp, unit='s')
    ratings.timestamp = ratings.timestamp.dt.year
    

    # Modify timestamps to be in terms of years
    tags.timestamp = pd.to_datetime(tags.timestamp, unit='s')
    tags.timestamp = tags.timestamp.dt.year


    return movies, tags, ratings

def get_genome_data():
    print("Reading genome data")
    genome_scores = pd.read_csv('movielens_dataset/genome-scores.csv')
    genome_tags = pd.read_csv('movielens_dataset/genome-tags.csv')
    return genome_scores, genome_tags

# Count occurrences of each genre
def get_genre_counts(movies, genres):
    # Dict of genre occurences
    genre_occurrences = {}
    for g in genres:
        genre_occurrences[g] = len(movies[movies[g] == True])

    # Convert the dict into a list of genre, occurrences pairs, sorted by occurrences
    genre_list = list([key, val] for key, val in genre_occurrences.items())
    genre_list.sort(key = lambda x:x[1], reverse=True)

    return genre_list

# Produce lowest, highest, mean, median, stddev, and number of movie ratings for each movie
def get_ratings_stats(movies, ratings):
    print("Producing aggregate ratings")
    # Generate a new dataframe to store the aggregate ratings in
    aggregate_ratings = pd.DataFrame()
    aggregate_ratings['movieId'] = movies['movieId']
    aggregate_ratings['min_rating'] = 0
    aggregate_ratings['max_rating'] = 0
    aggregate_ratings['mean_rating'] = 0
    aggregate_ratings['median_rating'] = 0
    aggregate_ratings['std_dev'] = 0
    aggregate_ratings['number_of_ratings'] = 0

    # Join ratings and movies on movieId
    rm = ratings.join(movies.set_index('movieId'), on='movieId')

    def get_stats(row):
        id = row['movieId']
        this_ratings = rm[rm['movieId'] == id]['rating']
        if len(this_ratings) > 0:
            row['min_rating', 'max_rating', 'mean_rating', 'median_rating', 'std_dev', 'number_of_ratings'] = \
                [np.min(this_ratings), np.max(this_ratings), np.mean(this_ratings), np.median(this_ratings), np.std(this_ratings), len(this_ratings)]
        return row

    aggregate_ratings = aggregate_ratings.apply(get_stats, axis=1)

    # Join movies and ratings on movieId
    # rm = ratings.join(movies.set_index('movieId'), on='movieId')
    # # Loop over movieId
    # for id in aggregate_ratings.movieId.values:
    #     this_ratings = rm[rm['movieId'] == id]['rating']
    #     if len(this_ratings) > 0:
    #         aggregate_ratings.loc[aggregate_ratings['movieId'] == id, ['min_rating', 'max_rating', 'mean_rating', 'median_rating', 'std_dev', 'number_of_ratings']] = \
    #             [np.min(this_ratings), np.max(this_ratings), np.mean(this_ratings), np.median(this_ratings), np.std(this_ratings), len(this_ratings)]

    # Return the new dataframe holding aggregated ratings data
    return aggregate_ratings

def get_rating_stats_by_genre(movies, aggregate_ratings, genres):
    print("Producing rating distributions")
    # Construct a list of number of movies for each genre in each rating 'bucket' (0.5 to 1, 1 to 1.5, ..., 4.5 to 5.0), inclusive below (except 4.5 to 5.0 range which is inclusive on both sides)
    metrics = ['min_rating', 'max_rating', 'mean_rating', 'median_rating']

    # Dict of genre score distributions
    genre_counts = {}
    for g in genres:
        genre_counts[g] = {}
        for metric in metrics:
            genre_counts[g][metric] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Join movies and aggregate_ratings on movie Id
    movies = movies.join(aggregate_ratings.set_index('movieId'), on='movieId')

    # Loop over each movie
    for index, row in movies.iterrows():
        # Skip if movie has no ratings
        if row['number_of_ratings'] == 0:
            continue
        # Repeat for each metric
        for metric in metrics:
            # Get this movie's bucket for this metric
            rating = row[metric]
            index = int(((rating*2)//1)) - 1# This doubles the rating, then floors it, i.e. (0.5->0.99... become 1, 1.0-> 1.499.. become 2, etc.), then subtracts 1 so indices are 0, 1, ...
            if index == 9:
                index -= 1 # Fixes a rating of 5 returning an out of range index of 9
            # Add one at this index for each genre tag this movie has
            for g in genres:
                genre_counts[g][metric][index] += row[g]

    # Normalise the list to produce proportional results
    for genre in genre_counts.keys():
        for metric in metrics:
            if sum(genre_counts[genre][metric]) > 0:
                genre_counts[genre][metric] = [genre_counts[genre][metric][i]/sum(genre_counts[genre][metric]) for i in range(len(genre_counts[genre][metric]))]

    # Return the list of score distributions by genre
    return genre_counts


# Count occurrences of each tag
def tag_occurrences(movies, tags):
    # Get a list of all tags
    tag_labels = set()
    for tag in tags['tag'].values:
        tag_labels = tag_labels.union(set([tag]))

    # Dict of tag occurences
    tag_occurrences = {}
    for t in tag_labels:
        tag_occurrences[t] = 0

    for tag in tags['tag'].values:
            tag_occurrences[tag] += 1

    # Convert the dict into a list of tag, occurrences pairs, sorted by occurrences
    tag_list = list([key, val] for key, val in tag_occurrences.items())
    tag_list.sort(key = lambda x:x[1], reverse=True)

    return tag_list

# For a given genre, get the top movies from that genre by mean rating (where number of ratings > 1)
def get_top_movies_by_genre(movies, aggregate_ratings, genre, number=10):
    # Get the list of movies of this genre
    genre_movies = movies[movies[genre]]
    # Join this list with the aggregate_ratings list
    genre_movies = genre_movies.join(aggregate_ratings.set_index('movieId'), on='movieId')
    # Only consider movies with at least 2 ratings
    genre_movies = genre_movies.loc[genre_movies['number_of_ratings'].apply(lambda x: x >= 2)]
    # Sort the new dataframe by the mean rating, descending
    genre_movies = genre_movies.sort_values('mean_rating', ascending=False)
    # Return the top 10 from this list
    return genre_movies.head(number)

# Gets the popularity of each genre (counted as the number of ratings submitted about movies of that genre) as a function over time
def get_genre_popularity_by_reviews_over_time(movies, ratings):
    print("Gathering genre popularity metrics (reviews)")
    # Join ratings and movies on movieId
    rating_movies = ratings.join(movies.set_index('movieId'), on='movieId')
    # List of all movie genres - not including [no genre listed]
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    # Create a list of timestamps (years from 1996 to 2018 inclusive), each list holds the number of ratings for each genre in that timestamp
    popularity = []
    for i in range(1996, 2019):
        year_dict = {}
        for g in genres:
            counts = len(rating_movies[(rating_movies['timestamp'] == i) & (rating_movies[g])])
            year_dict[g] = counts
        popularity.append(year_dict)
    return popularity

# Gets the popularity of each genre (counted as the number of movies of that genre released) as a function over time
# Only gathers data for years in range [1930, 2018] as before this there's too few movies in the dataset to produce a good view (<100)
def get_genre_popularity_by_releases_over_time(movies):
    print("Gathering genre popularity metrics (releases)")
    # List of all movie genres - not including [no genre listed]
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    # Create a list of timestamps (years from 1930 to 2018 inclusive), each list holds the number of movies for each genre in that year
    popularity = []
    for i in range(1930, 2019):
        year_dict = {}
        for g in genres:
            counts = len(movies[(movies['year'] == str(i)) & (movies[g])])
            year_dict[g] = counts
        popularity.append(year_dict)
    return popularity
