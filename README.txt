Running instructions:
Place the csv files (genome-scores.csv, genome-tags.csv, links.csv, movies.csv, ratings.csv, tags.csv) within a folder named 'movielens_dataset'. This should be done automatically when unzipping the submission.
To run the visualization GUI simply execute "python main.py" in the directory of main.py. Upon starting the program will load and process all data from the .csv files, this may take a few minutes (should not be longer than 5).
After this, all visualizations will be ready to run. The GUI consists of some visualizations on the left, a knowledge discovery interface on the top right, and a quit button in the bottom right. The visualizations can be customised/steered using the input widgets beneath them.

Description:
In this project I have produced three 3D visualizations to visualise the Movielens dataset. The first is a plot showing the distribution of ratings for each genre of movies. The user can select between mean, median, highest, and lowest rating.
The second and third visualisations are circular charts displaying the relative popularity of each genre of movies in each year. This is animated to show the change over time. The user can select the framerate, the starting frame (freeze frame if fps = 0), and whether to look at user popularity (by number of ratings submitted), or producer popularity (by number of movies produced).

For knowledge discovery, a set of fields are added to the GUI to allow the user to input the IDs of any two movies. The system then computes a difference index for those two movies (based on the data in genomre-scores.csv), and outputs this difference. It also finds a third movie which is more similar to both movies than they are to each other (i.e. it 'bridges the gap' between the two input movies).

