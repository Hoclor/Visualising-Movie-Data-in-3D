# PadX/PadY pads from both sides
# Cells in rows/columns fill up, e.g. set row1 and row5 pushes row5 into the position of row2. Define the empty rows with minwidth
# Contents that overfill a cell pushes the entire column/row to be wider, not just that cell

import pandas as pd
import numpy as np
import vtk

# Read the movielens dataset in using pandas
movies = pd.read_csv('movielens_dataset/movies.csv')
