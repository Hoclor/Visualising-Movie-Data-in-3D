import random
import pandas as pd
import numpy as np
from tkinter import *
import vtk
from vtk.util.colors import *

import data_extraction as de

# Create the GUI
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_data()

        self.init_window(cols=4, rows=4) # Use a 5x5 grid in the main frame


        # Vis 1
        # Default metric
        self.metric = 'mean_rating'

        # Vis 2
        # Default framerate
        self.framerate = 5
        # Default starting year
        self.year = 1930
        # Default metric
        self.popMetric = 'Releases'
        
    # Creation of init_window
    def init_window(self, rows=5, cols=5):
        # Set the title of the master widget
        self.master.title("Visualization coursework - pbqk24")
        cell_height = 900//rows
        cell_width = 1600//cols

        # Set up a dict for button sizing arguments to use for all (standard) buttons
        self.button_size_args = {
            'height': 8,
            'width': 32,
            'font': ("Courier", 14),
            'bg': '#aaa',
            'activebackground': '#666',
            'wraplength': 32*10
        }
        self.optionmenu_size_args = {
            'height': 6,
            'width': 24,
            'font': ("Courier", 12),
            'bg': '#aaa',
            'activebackground': '#666',
            'wraplength': 32*12
        }

        # Set the widget to fill the entire root window
        self.pack(fill=BOTH, expand=1)

        # Set up a grid in the widget
        for col in range(cols):
            self.grid_columnconfigure(col, minsize=cell_width)
        for row in range(rows):
            self.grid_rowconfigure(row, minsize=cell_height)

        for row in range(rows):
            for col in range(cols):
                Label(self, text='').grid(column=col, row=row)

        # Create a button instance
        quitButton = Button(self, text="Quit", command=self.client_exit, **self.button_size_args)
        # Place the button in the window
        quitButton.grid(column=cols-1, row=rows-1)

        # Create a button instance
        gridButton = Button(self, text="Grid 2D", command=self.grid_2D, **self.button_size_args)
        # Place the button in the window
        gridButton.grid(column=0, row=3)

        # Create a button instance
        ptCloudButton = Button(self, text="Point Cloud", command=self.point_cloud, **self.button_size_args)
        # Place the button in the window
        ptCloudButton.grid(column=1, row=3)

        # Create a button instance
        testButton = Button(self, text="Test", command=self.vtk_movie_popularity_by_releases_circular_chart, **self.button_size_args)
        # Place the button in the window
        testButton.grid(column=3, row=2)

        # Create a button instance
        ratingsByGenreButton = Button(self, text="Visualization 1:\nRating distribution statistics by Genre\n\n(Select metric below)", command=self.vtk_ratings_by_genre, **self.button_size_args)
        # Place the button in the window
        ratingsByGenreButton.grid(column=0, row=0)

        # Create a drop down list to choose the metric for the above visualization
        self.vis1_rating_list = StringVar(self.master)
        self.vis1_rating_list.set('Mean rating')

        vis1_rating = OptionMenu(self, self.vis1_rating_list, "Mean rating", "Median rating", "Highest rating", "Lowest rating")
        vis1_rating.config(**self.optionmenu_size_args)
        # Place the drop down list in the window
        vis1_rating.grid(column=0, row=1)
        self.vis1_rating_list.trace('w', self.updateMetric)

        # Create a button instance
        genreGraphButton = Button(self, text="Visualization 2:\nHow different Genres are connected through movies\n\n(Optional: Select one or two genres below)", command=self.vtk_genre_graph, **self.button_size_args)
        # Place the button in the window
        genreGraphButton.grid(column=1, row=0)

        genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

        # Create two drop down lists to choose genres from for the above visualization
        self.vis2_genre1_list = StringVar(self.master)
        self.vis2_genre1_list.set('None')

        vis2_genre1 = OptionMenu(self, self.vis2_genre1_list, 'None', *genres)
        vis2_genre1.config(**self.optionmenu_size_args)
        # Place the drop down list in the window
        vis2_genre1.grid(column=1, row=1)
        self.vis2_genre1_list.trace('w', self.updateGenre)

        # Second drop down list
        self.vis2_genre2_list = StringVar(self.master)
        self.vis2_genre2_list.set('None')

        vis2_genre2 = OptionMenu(self, self.vis2_genre2_list, 'None', *genres)
        vis2_genre2.config(**self.optionmenu_size_args)
        # Place the drop down list in the window
        vis2_genre2.grid(column=1, row=2)
        self.vis2_genre2_list.trace('w', self.updateGenre)

        # Create a button instance
        circularChartButton = Button(self, text="Visualization 3:\nHow the relative popularity of Genres changes over time\n(Optional: Select a year and framerate below)\nSelect the metric:\n(releases (1930-2018) or reviews (1996-2018))", command=self.vtk_pop_handler, **self.button_size_args)
        # Place the button in the window
        circularChartButton.grid(column=2, row=0)

        # Create a drop down list to choose the year for the above visualization
        self.vis3_year_list = StringVar(self.master)
        self.vis3_year_list.set('1930')

        year_options = [str(i) for i in range(1930, 2019, 10)]
        year_options.insert(0, 'Total')
        year_options.append('2019')

        vis3_year = OptionMenu(self, self.vis3_year_list, *year_options)
        vis3_year.config(**self.optionmenu_size_args)
        # Place the drop down list in the window
        vis3_year.grid(column=2, row=1)
        self.vis3_year_list.trace('w', self.updateYear)

        # Create a drop down list to choose the year for the above visualization
        self.vis3_framerate_list = StringVar(self.master)
        self.vis3_framerate_list.set('5 FPS')
        framerate_options = ['Static', '1 FPS', '2 FPS', '3 FPS', '5 FPS', '10 FPS', '20 FPS', 'One Loop per Second']

        vis3_framerate = OptionMenu(self, self.vis3_framerate_list, *framerate_options)
        vis3_framerate.config(**self.optionmenu_size_args)
        # Place the drop down list in the window
        vis3_framerate.grid(column=2, row=2)
        self.vis3_framerate_list.trace('w', self.updateFramerate)

        # Create a drop down list to choose the metric for the above visualization
        self.vis3_metric_list = StringVar(self.master)
        self.vis3_metric_list.set('Releases')

        vis3_metric = OptionMenu(self, self.vis3_metric_list, "Releases", "Reviews")
        vis3_metric.config(**self.optionmenu_size_args)
        # Place the drop down list in the window
        vis3_metric.grid(column=2, row=3)
        self.vis3_metric_list.trace('w', self.updatePopMetric)

    # Gathering of data
    def init_data(self):
        self.movies, self.tags, self.ratings = de.read_dataset()

        self.aggregate_ratings = []
        self.rating_stats_by_genre = []

        self.genre_popularity_by_reviews = de.get_genre_popularity_by_reviews_over_time(self.movies, self.ratings)
        self.genre_popularity_by_releases = de.get_genre_popularity_by_releases_over_time(self.movies)

        self.genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

        print("Done initializing data")

    def client_exit(self):
        exit()

    def updateMetric(self, *args):
        metric_string = self.vis1_rating_list.get()
        if metric_string == 'Mean rating':
            self.metric = 'mean_rating'
        elif metric_string == 'Median rating':
            self.metric = 'median_rating'
        elif metric_string == 'Highest rating':
            self.metric = 'max_rating'
        elif metric_string == 'Lowest rating':
            self.metric = 'min_rating'
        else:
            print("Unexpected metric value: {}".format(metric_string))

    def updateGenre(self, *args):
        pass

    def updateYear(self, *args):
        year = self.vis3_year_list.get()
        # Update the displayed value - necessary if this is called directly (from updatePopMetric)
        self.vis3_year_list.set(year)
        self.year = 0 if year == 'Total' else int(year)

    def updateFramerate(self, *args):
        val = self.vis3_framerate_list.get()
        # Dict holding framerates depending on first two character of val
        rates = {'St': 0, '1 ': 1, '2 ': 2, '3 ': 3, '5 ': 5, '10': 10, '20': 20, 'On': -1}
        self.framerate = rates[val[0:2]]

    def updatePopMetric(self, *args):
        self.popMetric = self.vis3_metric_list.get()
        if self.popMetric == 'Reviews':
            # Replace the year selection button
            # Create a drop down list to choose the year for the above visualization
            self.vis3_year_list = StringVar(self.master)
            self.vis3_year_list.set('1996')

            year_options = [str(i) for i in range(1996, 2019)]
            year_options.insert(0, 'Total')

            vis3_year = OptionMenu(self, self.vis3_year_list, *year_options)
            vis3_year.config(**self.optionmenu_size_args)
            # Place the drop down list in the window
            vis3_year.grid(column=2, row=1)
            self.vis3_year_list.trace('w', self.updateYear)
        else:
            # Create a drop down list to choose the year for the above visualization
            self.vis3_year_list = StringVar(self.master)
            self.vis3_year_list.set('1930')

            year_options = [str(i) for i in range(1930, 2019, 10)]
            year_options.insert(0, 'Total')
            year_options.append('2019')

            vis3_year = OptionMenu(self, self.vis3_year_list, *year_options)
            vis3_year.config(**self.optionmenu_size_args)
            # Place the drop down list in the window
            vis3_year.grid(column=2, row=1)
            self.vis3_year_list.trace('w', self.updateYear)
        # call the updateYear function
        self.updateYear()

    def test(self):
        pass

    def vtk_ratings_by_genre(self):
        # Produce rating distributions if they are not already stored
        if(len(self.aggregate_ratings) == 0):
            self.aggregate_ratings = de.get_ratings_stats(self.movies, self.ratings)
        if len(self.rating_stats_by_genre) == 0:
            self.rating_stats_by_genre = de.get_rating_stats_by_genre(self.movies, self.aggregate_ratings, self.genres)

        # Read which metric to use
        metric = self.metric
        
        genre_list = list(self.rating_stats_by_genre.keys())
        genre_list.sort()

        # Set up labels for the X and Y axes
        width = len(genre_list)
        height = 9

        # Data structures for labels
        label_pd = vtk.vtkPolyData()
        label_points = vtk.vtkPoints()
        label_verts = vtk.vtkCellArray()
        label = vtk.vtkStringArray()
        label.SetName('label')

        # Y axis labels
        for y in range(height):
            label_points.InsertNextPoint(-1, y, 0)
            label_verts.InsertNextCell(1)
            label_verts.InsertCellPoint(y)
            label.InsertNextValue(str((y+1)*0.5) + '-' + str((y+2)*0.5)) # Construct labels as '0.5-1.0'
        # Add Y axis title
        label_points.InsertNextPoint(-2, (height-1)/2, 0)
        label_verts.InsertNextCell(1)
        label_verts.InsertCellPoint(height)
        label.InsertNextValue("Scores")

        # X axis labels
        for x in range(width):
            label_points.InsertNextPoint(x, -1, 0)
            label_verts.InsertNextCell(1)
            label_verts.InsertCellPoint(x)
            label.InsertNextValue(genre_list[x])
        # Add X axis title
        label_points.InsertNextPoint((width-1)/2, -2, 0)
        label_verts.InsertNextCell(1)
        label_verts.InsertCellPoint(width)
        label.InsertNextValue("Genre")

        # Add chart title
        label_points.InsertNextPoint((width-1)/4, height + 2, 2)
        label_verts.InsertNextCell(1)
        label_verts.InsertCellPoint(width + height)
        label.InsertNextValue("Distribution of {} (in ranges of 0.5) of Movies by Genre".format(self.vis1_rating_list.get()))

        label_pd.SetPoints(label_points)
        label_pd.SetVerts(label_verts)
        label_pd.GetPointData().AddArray(label)

        hier = vtk.vtkPointSetToLabelHierarchy()
        hier.SetInputData(label_pd)
        hier.SetLabelArrayName('label')
        hier.GetTextProperty().SetColor(0.0, 0.0, 0.0)

        label_mapper = vtk.vtkLabelPlacementMapper()
        label_mapper.SetInputConnection(hier.GetOutputPort())
        label_mapper.SetPlaceAllLabels(True)
        # label_mapper.SetShapeToRoundedRect()
        # label_mapper.SetBackgroundColor(1.0, 1.0, 0.7)
        # label_mapper.SetBackgroundOpacity(0.8)
        # label_mapper.SetMargin(3)

        label_actor = vtk.vtkActor2D()
        label_actor.SetMapper(label_mapper)

        # Done preparing labels, now prepare the points and lines

        lines = vtk.vtkCellArray()

        colors = vtk.vtkNamedColors()
        # Create the points in the grid and lines joining them vertically
        points = vtk.vtkPoints()
        for x in range(width):
            for y in range(height):
                z = self.rating_stats_by_genre[genre_list[x]][metric][y] * 10 # Scale z axis up by 10
                points.InsertNextPoint(x, y, z)
                if(y < height - 1):
                    line = vtk.vtkLine()
                    line.GetPointIds().SetId(0, height*x + y)
                    line.GetPointIds().SetId(1, height*x + y + 1)
                    lines.InsertNextCell(line)

        # Add the grid points to a polydata object
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        glyphFilter = vtk.vtkVertexGlyphFilter()
        glyphFilter.SetInputData(polydata)
        glyphFilter.Update()

        # Create a Polydata to store all the lines in
        linesPolyData = vtk.vtkPolyData()

        # Add the points and lines to the dataset
        linesPolyData.SetPoints(points)
        linesPolyData.SetLines(lines)

        # Create a mapper and actor for the lines
        line_mapper = vtk.vtkPolyDataMapper()
        line_mapper.SetInputData(linesPolyData)

        line_actor = vtk.vtkActor()
        line_actor.SetMapper(line_mapper)
        line_actor.GetProperty().SetLineWidth(1)
        line_actor.GetProperty().SetColor(colors.GetColor3d("Black"))
        
        # Create a mapper and actor for the points
        points_mapper = vtk.vtkPolyDataMapper()
        points_mapper.SetInputConnection(glyphFilter.GetOutputPort())

        points_actor = vtk.vtkActor()
        points_actor.SetMapper(points_mapper)
        points_actor.GetProperty().SetPointSize(3)
        points_actor.GetProperty().SetColor(colors.GetColor3d("Black"))

        ##### Point triangulation #####
        # Triangulate the grid points
        delaunay = vtk.vtkDelaunay2D()
        delaunay.SetInputData(polydata)
        delaunay.Update()

        outputPolyData = delaunay.GetOutput()


        ##### Colour mapping #####
        # From VTK coloured elevation map example
        bounds = 6*[0.0]
        outputPolyData.GetBounds(bounds)
        # Find min and max z
        minZ = bounds[4]
        maxZ = bounds[5]

        # Create the colour table
        # From https://stackoverflow.com/questions/51747494/how-to-visualize-2d-array-of-doubles-in-vtk
        colorSeries = vtk.vtkColorSeries()
        colorSeries.SetColorScheme(vtk.vtkColorSeries.CITRUS)
        colour_table = vtk.vtkColorTransferFunction()
        colour_table.SetColorSpaceToHSV()
        nColors = colorSeries.GetNumberOfColors()
        zMin = minZ
        zMax = maxZ
        for i in range(0, nColors):
            color = colorSeries.GetColor(i)
            color = [c/255.0 for c in color]
            t = zMin + float(zMax - zMin)/(nColors - 1) * i
            colour_table.AddRGBPoint(t, color[0], color[1], color[2])

        # Generate colours for each point based on the colour table
        colours = vtk.vtkUnsignedCharArray()
        colours.SetNumberOfComponents(3)
        colours.SetName("Colours")

        for i in range(0, outputPolyData.GetNumberOfPoints()):
            p = 3*[0.0]
            outputPolyData.GetPoint(i,p)

            dcolour = 3*[0.0]
            colour_table.GetColor(p[2], dcolour)

            colour=3*[0.0]
            for j in range(0,3):
                colour[j] = int(255*dcolour[j])

            try:
                colours.InsertNextTupleValue(colour)
            except AttributeError:
                # For compatibility with new VTK generic data arrays.
                colours.InsertNextTypedTuple(colour)

        outputPolyData.GetPointData().SetScalars(colours)

        # Create a mapper and actor
        triangulated_mapper = vtk.vtkPolyDataMapper()
        triangulated_mapper.SetInputData(outputPolyData)

        triangulated_actor = vtk.vtkActor()
        triangulated_actor.SetMapper(triangulated_mapper)

        # Create a renderer, render window, and interactor
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # Add the actors to the scene
        renderer.AddActor(label_actor)
        renderer.AddActor(line_actor)
        renderer.AddActor(points_actor)
        renderer.AddActor(triangulated_actor)
        renderer.SetBackground(colors.GetColor3d("SlateGray")) # Background color green

        # Render and interact
        renderWindow.Render()
        renderWindowInteractor.Start()


    def vtk_pop_handler(self):
        if self.popMetric == "Reviews":
            self.vtk_movie_popularity_by_reviews_circular_chart()
        else:
            self.vtk_movie_popularity_by_releases_circular_chart()

    def vtk_movie_popularity_by_reviews_circular_chart(self):
        # Compute unit vectors for all 18 genre delimeter lines
        unit_vectors = []
        i = 0
        while i < 360:
            unit_vectors.append([np.cos(i*np.pi/180), np.sin(i*np.pi/180)])
            i += 360/19
        # Remove the last unit vector added due to floating point rounding errors
        unit_vectors = unit_vectors[:-1]

        # Draw the delimeter lines
        lines = vtk.vtkCellArray()
        colors = vtk.vtkNamedColors()
        points = vtk.vtkPoints()
        # First point is origin
        points.InsertNextPoint(0, 0, 0)
        for index, unit_vector in enumerate(unit_vectors):
            z = 0 # Scale z axis up by 10
            points.InsertNextPoint(unit_vector[0], unit_vector[1], 0)
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, 0)
            line.GetPointIds().SetId(1, index + 1)
            lines.InsertNextCell(line)

        # Add labels to the delimeter lines - each corresponds to a genre
        # Data structures for labels
        label_pd = vtk.vtkPolyData()
        label_points = vtk.vtkPoints()
        label_verts = vtk.vtkCellArray()
        label = vtk.vtkStringArray()
        label.SetName('label')
        for index, unit_vector in enumerate(unit_vectors):
            label_points.InsertNextPoint(unit_vector[0]*1.1, unit_vector[1]*1.1, 0)
            label_verts.InsertNextCell(1)
            label_verts.InsertCellPoint(index)
            label.InsertNextValue(self.genres[index])

        label_pd.SetPoints(label_points)
        label_pd.SetVerts(label_verts)
        label_pd.GetPointData().AddArray(label)

        hier = vtk.vtkPointSetToLabelHierarchy()
        hier.SetInputData(label_pd)
        hier.SetLabelArrayName('label')
        hier.GetTextProperty().SetColor(0.0, 0.0, 0.0)

        label_mapper = vtk.vtkLabelPlacementMapper()
        label_mapper.SetInputConnection(hier.GetOutputPort())
        label_mapper.SetPlaceAllLabels(True)
        # label_mapper.SetShapeToRoundedRect()
        # label_mapper.SetBackgroundColor(1.0, 1.0, 0.7)
        # label_mapper.SetBackgroundOpacity(0.8)
        # label_mapper.SetMargin(3)

        label_actor = vtk.vtkActor2D()
        label_actor.SetMapper(label_mapper)

        # Generate a point on each unit vector that corresponds to that unit vector's genre's popularity for a given time
        year = self.year - 1996 # year 1996 = index 0
        if year < 0:
            # Total was set, so get the overall data for all years
            year_popularity = {genre: sum([self.genre_popularity_by_reviews[y][genre] for y in range(len(self.genre_popularity_by_reviews))]) for genre in self.genre_popularity_by_reviews[0]} # Get the dict for this year
            year_popularity = list(sorted(year_popularity.items())) # Convert the dict into a list of [key, value]
            year_pop_sum = sum([n[1] for n in year_popularity]) # Compute the total number of ratings submitted for this year
            normalised_year_popularity = list(map(lambda n : [n[0], (5*n[1]/year_pop_sum if year_pop_sum > 0 else n[1])], year_popularity)) # Normalised popularities (sum over genres = 1)
            print(max([n[1] for n in normalised_year_popularity]))
            # The maximum normalised_year_pop is <0.2 even when looking at all data combined, so multiply all pop values by 5 (to make the plot more readable)
        else:
            year_popularity = self.genre_popularity_by_reviews[year] # Get the dict for this year
        year_popularity = list(sorted(year_popularity.items())) # Convert the dict into a list of [key, value]
        year_pop_sum = sum([n[1] for n in year_popularity]) # Compute the total number of ratings submitted for this year
        normalised_year_popularity = list(map(lambda n : [n[0], (5*n[1]/year_pop_sum if year_pop_sum > 0 else n[1])], year_popularity)) # Normalised popularities (sum over genres = 1)
        # The maximum normalised_year_pop ever is <0.2, so multiply all pop values by 5 (to make the plot more readable)

        # Create points on each unit vector proportionately distant from origin to this genre's popularity for that year
        pop_lines = vtk.vtkCellArray()
        pop_points = vtk.vtkPoints()
        for index, unit_vector in enumerate(unit_vectors):
            pop_points.InsertNextPoint(unit_vector[0]*normalised_year_popularity[index][1], unit_vector[1]*normalised_year_popularity[index][1], 0)
            if index > 0:
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, index - 1)
                line.GetPointIds().SetId(1, index)
                pop_lines.InsertNextCell(line)
        # Add the last line that joins the last pop_point to the first pop_point
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, index)
        line.GetPointIds().SetId(1, 0)
        pop_lines.InsertNextCell(line)
        
        # Create a Polydata to store all the lines in
        linesPolyData = vtk.vtkPolyData()
        popLinesPolyData = vtk.vtkPolyData()

        # Add the lines to the dataset
        linesPolyData.SetPoints(points)
        linesPolyData.SetLines(lines)
        popLinesPolyData.SetPoints(pop_points)
        popLinesPolyData.SetLines(pop_lines)

        # Create a mapper and actor for the lines
        line_mapper = vtk.vtkPolyDataMapper()
        line_mapper.SetInputData(linesPolyData)
        pop_line_mapper = vtk.vtkPolyDataMapper()
        pop_line_mapper.SetInputData(popLinesPolyData)

        line_actor = vtk.vtkActor()
        line_actor.SetMapper(line_mapper)
        line_actor.GetProperty().SetLineWidth(1)
        line_actor.GetProperty().SetColor(colors.GetColor3d("Black"))

        pop_line_actor = vtk.vtkActor()
        pop_line_actor.SetMapper(pop_line_mapper)
        pop_line_actor.GetProperty().SetLineWidth(3)
        pop_line_actor.GetProperty().SetColor(colors.GetColor3d("Red"))
        
        # Write the current year on the bottom-left of the frame
        txt = vtk.vtkTextActor()
        txt.SetInput(str(year + 1996) if year >= 0 else '1996-2018')
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(60)
        txtprop.SetColor(1,1,1)
        txt.SetDisplayPosition(40,40)

        # Create a renderer, render window, and interactor
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # Add the actors to the scene
        renderer.AddActor(label_actor)
        renderer.AddActor(txt)
        renderer.AddActor(line_actor)
        renderer.AddActor(pop_line_actor)
        renderer.SetBackground(colors.GetColor3d("SlateGray")) # Background color green

        # Render and interact
        renderWindow.Render()
        renderWindowInteractor.Initialize() # Initialize first, then create timer events

        # Only set up animation if year != -1 (i.e. don't animate 'Total' display) and if framerate > 0
        if year >= 0 and self.framerate != 0:
            cb = vtkTimerCallback_vis3a(year)
            # Set all necessary data as fields in instance
            cb.line_actor = pop_line_actor
            cb.text_actor = txt
            cb.genre_popularity = self.genre_popularity_by_reviews
            cb.unit_vectors = unit_vectors
            renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
            if self.framerate == -1:
                # Set framerate to display the entire loop in 1s
                framerate = 1000//23
            else:
                framerate = 1000//self.framerate
            timerId = renderWindowInteractor.CreateRepeatingTimer(framerate)

        # Start the interaction and timer
        renderWindowInteractor.Start()

    def vtk_movie_popularity_by_releases_circular_chart(self):
        # Compute unit vectors for all 18 genre delimeter lines
        unit_vectors = []
        i = 0
        while i < 360:
            unit_vectors.append([np.cos(i*np.pi/180), np.sin(i*np.pi/180)])
            i += 360/19
        # Remove the last unit vector added due to floating point rounding errors
        unit_vectors = unit_vectors[:-1]

        # Draw the delimeter lines
        lines = vtk.vtkCellArray()
        colors = vtk.vtkNamedColors()
        points = vtk.vtkPoints()
        # First point is origin
        points.InsertNextPoint(0, 0, 0)
        for index, unit_vector in enumerate(unit_vectors):
            z = 0 # Scale z axis up by 10
            points.InsertNextPoint(unit_vector[0], unit_vector[1], 0)
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, 0)
            line.GetPointIds().SetId(1, index + 1)
            lines.InsertNextCell(line)

        # Add labels to the delimeter lines - each corresponds to a genre
        # Data structures for labels
        label_pd = vtk.vtkPolyData()
        label_points = vtk.vtkPoints()
        label_verts = vtk.vtkCellArray()
        label = vtk.vtkStringArray()
        label.SetName('label')
        for index, unit_vector in enumerate(unit_vectors):
            label_points.InsertNextPoint(unit_vector[0]*1.1, unit_vector[1]*1.1, 0)
            label_verts.InsertNextCell(1)
            label_verts.InsertCellPoint(index)
            label.InsertNextValue(self.genres[index])

        label_pd.SetPoints(label_points)
        label_pd.SetVerts(label_verts)
        label_pd.GetPointData().AddArray(label)

        hier = vtk.vtkPointSetToLabelHierarchy()
        hier.SetInputData(label_pd)
        hier.SetLabelArrayName('label')
        hier.GetTextProperty().SetColor(0.0, 0.0, 0.0)

        label_mapper = vtk.vtkLabelPlacementMapper()
        label_mapper.SetInputConnection(hier.GetOutputPort())
        label_mapper.SetPlaceAllLabels(True)
        # label_mapper.SetShapeToRoundedRect()
        # label_mapper.SetBackgroundColor(1.0, 1.0, 0.7)
        # label_mapper.SetBackgroundOpacity(0.8)
        # label_mapper.SetMargin(3)

        label_actor = vtk.vtkActor2D()
        label_actor.SetMapper(label_mapper)

        # Generate a point on each unit vector that corresponds to that unit vector's genre's popularity for a given time
        year = self.year - 1930 # year 1930 = index 0
        if year < 0:
            # Total was set, so get the overall data for all years
            year_popularity = {genre: sum([self.genre_popularity_by_releases[y][genre] for y in range(len(self.genre_popularity_by_releases))]) for genre in self.genre_popularity_by_releases[0]} # Get the dict for this year
            year_popularity = list(sorted(year_popularity.items())) # Convert the dict into a list of [key, value]
            year_pop_sum = sum([n[1] for n in year_popularity]) # Compute the total number of ratings submitted for this year
            normalised_year_popularity = list(map(lambda n : [n[0], (3*n[1]/year_pop_sum if year_pop_sum > 0 else n[1])], year_popularity)) # Normalised popularities (sum over genres = 1)
            print(max([n[1] for n in normalised_year_popularity]))
            # The maximum normalised_year_pop is <0.33 even when looking at all data combined, so multiply all pop values by 3 (to make the plot more readable)
        else:
            year_popularity = self.genre_popularity_by_releases[year] # Get the dict for this year
            year_popularity = list(sorted(year_popularity.items())) # Convert the dict into a list of [key, value]
            year_pop_sum = sum([n[1] for n in year_popularity]) # Compute the total number of ratings submitted for this year
            normalised_year_popularity = list(map(lambda n : [n[0], (3*n[1]/year_pop_sum if year_pop_sum > 0 else n[1])], year_popularity)) # Normalised popularities (sum over genres = 1)
            # The maximum normalised_year_pop ever is <0.33, so multiply all pop values by 3 (to make the plot more readable)

        # Create points on each unit vector proportionately distant from origin to this genre's popularity for that year
        pop_lines = vtk.vtkCellArray()
        pop_points = vtk.vtkPoints()
        for index, unit_vector in enumerate(unit_vectors):
            pop_points.InsertNextPoint(unit_vector[0]*normalised_year_popularity[index][1], unit_vector[1]*normalised_year_popularity[index][1], 0)
            if index > 0:
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, index - 1)
                line.GetPointIds().SetId(1, index)
                pop_lines.InsertNextCell(line)
        # Add the last line that joins the last pop_point to the first pop_point
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, index)
        line.GetPointIds().SetId(1, 0)
        pop_lines.InsertNextCell(line)
        
        # Create a Polydata to store all the lines in
        linesPolyData = vtk.vtkPolyData()
        popLinesPolyData = vtk.vtkPolyData()

        # Add the lines to the dataset
        linesPolyData.SetPoints(points)
        linesPolyData.SetLines(lines)
        popLinesPolyData.SetPoints(pop_points)
        popLinesPolyData.SetLines(pop_lines)

        # Create a mapper and actor for the lines
        line_mapper = vtk.vtkPolyDataMapper()
        line_mapper.SetInputData(linesPolyData)
        pop_line_mapper = vtk.vtkPolyDataMapper()
        pop_line_mapper.SetInputData(popLinesPolyData)

        line_actor = vtk.vtkActor()
        line_actor.SetMapper(line_mapper)
        line_actor.GetProperty().SetLineWidth(1)
        line_actor.GetProperty().SetColor(colors.GetColor3d("Black"))

        pop_line_actor = vtk.vtkActor()
        pop_line_actor.SetMapper(pop_line_mapper)
        pop_line_actor.GetProperty().SetLineWidth(3)
        pop_line_actor.GetProperty().SetColor(colors.GetColor3d("Red"))

        # Write the current year on the bottom-left of the frame
        txt = vtk.vtkTextActor()
        txt.SetInput(str(year + 1930) if year >= 0 else '1930-2018')
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(60)
        txtprop.SetColor(1,1,1)
        txt.SetDisplayPosition(40,40)

        # Create a renderer, render window, and interactor
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # Add the actors to the scene
        renderer.AddActor(label_actor)
        renderer.AddActor(txt)
        renderer.AddActor(line_actor)
        renderer.AddActor(pop_line_actor)
        renderer.SetBackground(colors.GetColor3d("SlateGray")) # Background color green

        # Render and interact
        renderWindow.Render()
        renderWindowInteractor.Initialize() # Initialize first, then create timer events

        # Only set up animation if year != -1 (i.e. don't animate 'Total' display) and if framerate > 0
        if year >= 0 and self.framerate != 0:
            cb = vtkTimerCallback_vis3b(year)
            # Set all necessary data as fields in instance
            cb.line_actor = pop_line_actor
            cb.text_actor = txt
            cb.genre_popularity = self.genre_popularity_by_releases
            cb.unit_vectors = unit_vectors
            renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
            if self.framerate == -1:
                # Set framerate to display the entire loop in 1s
                framerate = 1000//90
            else:
                framerate = 1000//self.framerate
            timerId = renderWindowInteractor.CreateRepeatingTimer(framerate)

        # Start the interaction and timer
        renderWindowInteractor.Start()

    def glyphs_at_points(self):
        colors = vtk.vtkNamedColors()

        points = vtk.vtkPoints()
        points.InsertNextPoint(0,0,0)
        points.InsertNextPoint(1,1,1)
        points.InsertNextPoint(2,2,2)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        # Create anything you want here, we will use a cube for the demo.
        sphereSource = vtk.vtkSphereSource()

        glyph3D = vtk.vtkGlyph3D()
        glyph3D.SetSourceConnection(sphereSource.GetOutputPort())
        glyph3D.SetInputData(polydata)
        glyph3D.Update()

        # Visualize
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph3D.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(actor)
        renderer.SetBackground(colors.GetColor3d("SlateGray")) # Background Slate Gray

        renderWindow.Render()
        renderWindowInteractor.Start()

    def point_cloud(self):
        colors = vtk.vtkNamedColors()

# Class used to animate visualization 3a (genre popularity by reviews)
class vtkTimerCallback_vis3a():
    def __init__(self, start_year = 1996):
        self.timer_count = start_year
    def execute(self, obj, event):
        # Animate the visualization
        self.timer_count = (self.timer_count + 1) % (2018-1996+1) # Once the entire sequence has been animated, restart from the beginning

        # Generate a point on each unit vector that corresponds to that unit vector's genre's popularity for a given time
        year_popularity = self.genre_popularity[self.timer_count] # Get the dict for this year
        year_popularity = list(sorted(year_popularity.items())) # Convert the dict into a list of [key, value]
        year_pop_sum = sum([n[1] for n in year_popularity]) # Compute the total number of ratings submitted for this year
        normalised_year_popularity = list(map(lambda n : [n[0], (5*n[1]/year_pop_sum if year_pop_sum > 0 else n[1])], year_popularity)) # Normalised popularities (sum over genres = 1)
        # The maximum normalised_year_pop ever is <0.2, so multiply all pop values by 5 (to make the plot more readable)

        # Create points on each unit vector proportionately distant from origin to this genre's popularity for that year
        pop_lines = vtk.vtkCellArray()
        pop_points = vtk.vtkPoints()
        for index, unit_vector in enumerate(self.unit_vectors):
            pop_points.InsertNextPoint(unit_vector[0]*normalised_year_popularity[index][1], unit_vector[1]*normalised_year_popularity[index][1], 0)
            if index > 0:
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, index - 1)
                line.GetPointIds().SetId(1, index)
                pop_lines.InsertNextCell(line)
        # Add the last line that joins the last pop_point to the first pop_point
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, index)
        line.GetPointIds().SetId(1, 0)
        pop_lines.InsertNextCell(line)
        # Create a Polydata to store all the lines in
        popLinesPolyData = vtk.vtkPolyData()
        # Add the lines to the dataset
        popLinesPolyData.SetPoints(pop_points)
        popLinesPolyData.SetLines(pop_lines)

        # Create a mapper and actor for the lines
        pop_line_mapper = vtk.vtkPolyDataMapper()
        pop_line_mapper.SetInputData(popLinesPolyData)
        # Set this new mapper as the mapper
        self.line_actor.SetMapper(pop_line_mapper)
        # Update the year text
        self.text_actor.SetInput(str(self.timer_count + 1996))
        # Get the interaction object
        iren = obj
        # Render the new frame
        iren.GetRenderWindow().Render()

# Class used to animate visualization 3b (genre popularity by releases)
class vtkTimerCallback_vis3b():
    def __init__(self, start_year = 1930):
        self.timer_count = start_year
    def execute(self, obj, event):
        # Animate the visualization
        self.timer_count = (self.timer_count + 1) % (2018-1930+1) # Once the entire sequence has been animated, restart from the beginning

        # Generate a point on each unit vector that corresponds to that unit vector's genre's popularity for a given time
        year_popularity = self.genre_popularity[self.timer_count] # Get the dict for this year
        year_popularity = list(sorted(year_popularity.items())) # Convert the dict into a list of [key, value]
        year_pop_sum = sum([n[1] for n in year_popularity]) # Compute the total number of ratings submitted for this year
        normalised_year_popularity = list(map(lambda n : [n[0], (3*n[1]/year_pop_sum if year_pop_sum > 0 else n[1])], year_popularity)) # Normalised popularities (sum over genres = 1)
        # The maximum normalised_year_pop ever is <0.33, so multiply all pop values by 3 (to make the plot more readable)

        # Create points on each unit vector proportionately distant from origin to this genre's popularity for that year
        pop_lines = vtk.vtkCellArray()
        pop_points = vtk.vtkPoints()
        for index, unit_vector in enumerate(self.unit_vectors):
            pop_points.InsertNextPoint(unit_vector[0]*normalised_year_popularity[index][1], unit_vector[1]*normalised_year_popularity[index][1], 0)
            if index > 0:
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, index - 1)
                line.GetPointIds().SetId(1, index)
                pop_lines.InsertNextCell(line)
        # Add the last line that joins the last pop_point to the first pop_point
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, index)
        line.GetPointIds().SetId(1, 0)
        pop_lines.InsertNextCell(line)
        # Create a Polydata to store all the lines in
        popLinesPolyData = vtk.vtkPolyData()
        # Add the lines to the dataset
        popLinesPolyData.SetPoints(pop_points)
        popLinesPolyData.SetLines(pop_lines)

        # Create a mapper and actor for the lines
        pop_line_mapper = vtk.vtkPolyDataMapper()
        pop_line_mapper.SetInputData(popLinesPolyData)
        # Set this new mapper as the mapper
        self.line_actor.SetMapper(pop_line_mapper)
        # Update the year text
        self.text_actor.SetInput(str(self.timer_count + 1930))
        # Get the interaction object
        iren = obj
        # Render the new frame
        iren.GetRenderWindow().Render()


# Spawn the GUI
root = Tk()

# Default size of the window
root.geometry("1600x900")

app = Window(root)
root.mainloop()
