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
        self.init_window(cols=4, rows=4) # Use a 5x5 grid in the main frame

        self.init_data()

        # Default metric
        self.metric = 'mean_rating'

        
    # Creation of init_window
    def init_window(self, rows=5, cols=5):
        # Set the title of the master widget
        self.master.title("Visualization coursework - pbqk24")
        cell_height = 900//rows
        cell_width = 1600//cols

        # Set up a dict for button sizing arguments to use for all (standard) buttons
        button_size_args = {
            'height': 8,
            'width': 32,
            'font': ("Courier", 14),
            'bg': '#aaa',
            'activebackground': '#666',
            'wraplength': 32*10
        }
        optionmenu_size_args = {
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
        quitButton = Button(self, text="Quit", command=self.client_exit, **button_size_args)
        # Place the button in the window
        quitButton.grid(column=cols-1, row=rows-1)

        # Create a button instance
        gridButton = Button(self, text="Grid 2D", command=self.grid_2D, **button_size_args)
        # Place the button in the window
        gridButton.grid(column=0, row=3)

        # Create a button instance
        ptCloudButton = Button(self, text="Point Cloud", command=self.point_cloud, **button_size_args)
        # Place the button in the window
        ptCloudButton.grid(column=1, row=3)

        # Create a button instance
        glyphButton = Button(self, text="Glyphs", command=self.glyphs_at_points, **button_size_args)
        # Place the button in the window
        glyphButton.grid(column=2, row=3)

        # Create a button instance
        testButton = Button(self, text="Test", command=self.vtk_movie_popularity_circular_chart, **button_size_args)
        # Place the button in the window
        testButton.grid(column=3, row=2)

        # Create a button instance
        ratingsByGenreButton = Button(self, text="Visualization 1:\nRating distribution statistics by Genre\n\n(Select metric below)", command=self.vtk_ratings_by_genre, **button_size_args)
        # Place the button in the window
        ratingsByGenreButton.grid(column=0, row=0)

        # Create a drop down list to choose the metric for the above visualization
        self.vis1_rating_list = StringVar(self.master)
        self.vis1_rating_list.set('Mean rating')

        vis1_rating = OptionMenu(self, self.vis1_rating_list, "Mean rating", "Median rating", "Highest rating", "Lowest rating")
        vis1_rating.config(**optionmenu_size_args)
        # Place the drop down list in the window
        vis1_rating.grid(column=0, row=1)
        self.vis1_rating_list.trace('w', self.updateMetric)

        # Create a button instance
        genreGraphButton = Button(self, text="Visualization 2:\nHow different Genres are connected through movies\n\n(Select genres below, or run with none selected)", command=self.vtk_genre_graph, **button_size_args)
        # Place the button in the window
        genreGraphButton.grid(column=1, row=0)

        genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

        # Create two drop down lists to choose genres from for the above visualization
        self.vis2_genre1_list = StringVar(self.master)
        self.vis2_genre1_list.set('None')

        vis2_genre1 = OptionMenu(self, self.vis2_genre1_list, 'None', *genres)
        vis2_genre1.config(**optionmenu_size_args)
        # Place the drop down list in the window
        vis2_genre1.grid(column=1, row=1)
        self.vis2_genre1_list.trace('w', self.updateGenre)

        # Second drop down list
        self.vis2_genre2_list = StringVar(self.master)
        self.vis2_genre2_list.set('None')

        vis2_genre2 = OptionMenu(self, self.vis2_genre2_list, 'None', *genres)
        vis2_genre2.config(**optionmenu_size_args)
        # Place the drop down list in the window
        vis2_genre2.grid(column=1, row=2)
        self.vis2_genre2_list.trace('w', self.updateGenre)


    # Gathering of data
    def init_data(self):
        self.movies, self.tags, self.ratings = de.read_dataset()

        self.aggregate_ratings = []

        self.rating_stats_by_genre = []

        self.genre_popularity = []

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

        # Draw the horizontal lines
        # for y in range(height):
        #     for x in range(width):
        #         if(x < width - 1):
        #             line = vtk.vtkLine()
        #             line.GetPointIds().SetId(0, x + width*y)
        #             line.GetPointIds().SetId(1, x + width*y + 1)
        #             lines.InsertNextCell(line)

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

        # txt = vtk.vtkTextActor()
        # txt.SetInput("Text here")
        # txtprop=txt.GetTextProperty()
        # txtprop.SetFontFamilyToArial()
        # txtprop.SetFontSize(18)
        # txtprop.SetColor(1,1,1)
        # txt.SetDisplayPosition(20,30)
        # renderer.AddActor(txt)

        # Add the actors to the scene
        renderer.AddActor(label_actor)
        renderer.AddActor(line_actor)
        renderer.AddActor(points_actor)
        renderer.AddActor(triangulated_actor)
        renderer.SetBackground(colors.GetColor3d("SlateGray")) # Background color green

        # Render and interact
        renderWindow.Render()
        renderWindowInteractor.Start()

    def vtk_movie_popularity_circular_chart(self):
        if len(self.genre_popularity) == 0:
            self.genre_popularity = de.get_genre_popularity_over_time(self.movies, self.ratings)
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

        # Generate a point on each unit vector that corresponds to that unit vector's genre's popularity for a given time
        year = 1997 - 1996 # year 1996 = index 0
        year_popularity = self.genre_popularity[year] # Get the dict for this year
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

        # Add the points and lines to the dataset
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
        
        # Create a mapper and actor for the points
        # points_mapper = vtk.vtkPolyDataMapper()
        # points_mapper.SetInputConnection(glyphFilter.GetOutputPort())

        # points_actor = vtk.vtkActor()
        # points_actor.SetMapper(points_mapper)
        # points_actor.GetProperty().SetPointSize(3)
        # points_actor.GetProperty().SetColor(colors.GetColor3d("Black"))

        # Create a renderer, render window, and interactor
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # Add the actors to the scene
        # renderer.AddActor(label_actor)
        renderer.AddActor(line_actor)
        renderer.AddActor(pop_line_actor)
        renderer.SetBackground(colors.GetColor3d("SlateGray")) # Background color green

        # Render and interact
        renderWindow.Render()
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

        # create a rendering window and renderer
        ren = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)

        # create a renderwindowinteractor
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # create source
        src = vtk.vtkPointSource()
        src.SetCenter(0, 0, 0)
        src.SetNumberOfPoints(50)
        src.SetRadius(5)
        src.Update()

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(src.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d('Yellow'))

        actor.GetProperty().SetPointSize(5)

        # Add axes
        transform = vtk.vtkTransform()
        transform.Translate(1.0, 0.0, 0.0)

        axes = vtk.vtkAxesActor()
        #  The axes are positioned with a user transform
        axes.SetUserTransform(transform)

        # properties of the axes labels can be set as follows
        # this sets the x axis label to red
        # axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(colors.GetColor3d("Red"));

        # the actual text of the axis label can be changed:
        axes.SetXAxisLabelText("test")
        axes.SetYAxisLabelText("testY")
        axes.SetZAxisLabelText("testZ")


        # assign actors to the renderer
        ren.AddActor(actor)
        ren.AddActor(axes)
        ren.SetBackground(colors.GetColor3d('RoyalBLue'))

        # enable user interface interactor
        iren.Initialize()
        renWin.Render()
        iren.Start()

    def grid_2D(self):
        """Generate a 2D grid in 3D space
        """
        colors = vtk.vtkNamedColors()
        # Provide some geometry.
        xResolution = 10
        yResolution = 10
        aPlane = vtk.vtkPlaneSource()
        aPlane.SetXResolution(xResolution)
        aPlane.SetYResolution(yResolution)
        size = xResolution * yResolution + 1

        # Create cell data.
        cellData = vtk.vtkFloatArray()
        for i in range(0, xResolution * yResolution):
            cellData.InsertNextValue(i)
        aPlane.Update()  # Force an update so we can set cell data.
        aPlane.GetOutput().GetCellData().SetScalars(cellData)


        # Set up the actor and mapper.
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(aPlane.GetOutputPort())
        mapper.SetScalarModeToUseCellData()
        mapper.SetScalarRange(0, size)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()

        # Setup render window, renderer, and interactor.
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(actor)
        renderer.SetBackground(colors.GetColor3d('SlateGray'))
        renderWindow.Render()
        renderWindowInteractor.Start()

    def vtk_generate_cube(self):
        # create polygonal cube geometry
        #   here a procedural source object is used,
        #   a source can also be, e.g., a file reader
        cube = vtk.vtkCubeSource()
        cube.SetBounds(-1,1,-1,1,-1,1)

        # map to graphics library
        #   a mapper is the interface between the visualization pipeline
        #   and the graphics model
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube.GetOutputPort()) # connect source and mapper

        # an actor represent what we see in the scene,
        # it coordinates the geometry, its properties, and its transformation
        aCube = vtk.vtkActor()
        aCube.SetMapper(mapper)
        aCube.GetProperty().SetColor(0,0.7,0.7) # cube color green
        
        # a renderer and render window
        ren1 = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren1)

        # an interactor
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # add the actor to the scene
        ren1.AddActor(aCube)
        ren1.SetBackground(0.5,0.5,0.5) # Background color white

        # render an image (lights and cameras are created automatically)
        renWin.Render()

        # begin mouse interaction
        iren.Start()


# Spawn the GUI
root = Tk()


# Default size of the window
root.geometry("1600x900")

app = Window(root)
root.mainloop()