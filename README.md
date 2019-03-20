# Visualization
Code for Visualization assignment for `Visualization` submodule as part of `Software, Systems and Applications IV` module, taken in my fourth year of Computer Science at Durham University

# Running instructions:
Place the csv files (genome-scores.csv, genome-tags.csv, links.csv, movies.csv, ratings.csv, tags.csv) within a folder named 'movielens_dataset'. This should be done automatically when unzipping the submission.
To run the visualization GUI simply execute "python main.py" in the directory of main.py. Upon starting the program will load and process all data from the .csv files, this may take a few minutes (should not be longer than 5).
After this, all visualizations will be ready to run. The GUI consists of a series of visualizations on the left, and a knowledge discovery interface on the top right. The visualizations can be customised/steered using the input widgets beneath them.
Please note: the GUI may occasionally freeze on complicated tasks (mostly for knowledge discovery). If you leave it be it will eventually finish (within a minute). This is handled in the code.

# Description:
In this project I have produced three 3D visualizations to visualise the Movielens dataset. The first is a plot showing the distribution of ratings for each genre of movies. The user can select between mean, median, highest, and lowest rating when plotting.
The second and third visualisations are circular charts displaying the relative popularity of each genre of movies in each year, the first measured using number of reviews submitted (popularity amongst viewers), the second by the number of movies produced of that genre (popularity amongst movie creators). This is animated to show the change over time. The user can select the framerate and the starting frame (freeze frame if fps = 0), and can display overall data for all years.

For knowledge discovery, a set of fields are added to the GUI to allow the user to input the IDs of any two movies. The system then computes a difference index for those two movies (based on the data in genome-scores.csv), and outputs this difference. It also finds a third movie which is more similar to both movies than they are to each other (i.e. it 'bridges the gap' between the two input movies).

