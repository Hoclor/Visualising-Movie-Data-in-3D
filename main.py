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
            'wraplength': 32*14
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
        ratingsByGenreButton = Button(self, text="Visualization 4:\nView Rating Statistics by Genre\n\n(Select metric below)", command=self.vtk_ratings_by_genre, **button_size_args)
        # Place the button in the window
        ratingsByGenreButton.grid(column=3, row=1)

        # Create a drop down list to choose the metric for the above visualization
        self.ratingMetricList = StringVar(self.master)
        self.ratingMetricList.set('Mean rating')
        
        ratingMetricMenu = OptionMenu(self, self.ratingMetricList, "Mean rating", "Median rating", "Highest rating", "Lowest rating")
        ratingMetricMenu.config(**optionmenu_size_args)
        # Place the drop down list in the window
        ratingMetricMenu.grid(column=3, row=2)
        self.ratingMetricList.trace('w', self.updateMetric)

    # Gathering of data
    def init_data(self):
        print("Reading dataset from csv files")
        self.movies, self.tags, self.ratings = de.read_dataset()

        self.aggregate_ratings = []

        self.rating_stats_by_genre = []

        print("Done initializing data")

    def client_exit(self):
        exit()

    def test(self):
        pass

    def vtk_ratings_by_genre(self):
        # Produce rating distributions if they are not already stored
        if(len(self.aggregate_ratings) == 0):
            print("Producing aggregate ratings")
            self.aggregate_ratings = de.get_ratings_stats(self.movies, self.ratings)
        if len(self.rating_stats_by_genre) == 0:
            print("Producing rating distributions")
            self.rating_stats_by_genre = de.get_rating_stats_by_genre(self.movies, self.aggregate_ratings)
        
        # Read which metric to use
        metric = self.metric

        genre_list = list(self.rating_stats_by_genre.keys())

        # Set up labels for the X and Y axes
        width = len(genre_list)
        height = 9

        # Data structures for labels
        pd = vtk.vtkPolyData()
        pts = vtk.vtkPoints()
        verts = vtk.vtkCellArray()
        label = vtk.vtkStringArray()
        label.SetName('label')

        # Y axis labels
        for y in range(height):
            pts.InsertNextPoint(-1, y, 0)
            verts.InsertNextCell(1)
            verts.InsertCellPoint(y)
            label.InsertNextValue(str((y+1)*0.5) + '-' + str((y+2)*0.5)) # Construct labels as '0.5-1.0'
        # Add Y axis title
        pts.InsertNextPoint(-2, (height-1)/2, 0)
        verts.InsertNextCell(1)
        verts.InsertCellPoint(height)
        label.InsertNextValue("Scores")

        # X axis labels
        for x in range(width):
            pts.InsertNextPoint(x, -1, 0)
            verts.InsertNextCell(1)
            verts.InsertCellPoint(x)
            label.InsertNextValue(genre_list[x])
        # Add X axis title
        pts.InsertNextPoint((width-1)/2, -2, 0)
        verts.InsertNextCell(1)
        verts.InsertCellPoint(width)
        label.InsertNextValue("Genre")

        pd.SetPoints(pts)
        pd.SetVerts(verts)
        pd.GetPointData().AddArray(label)

        hier = vtk.vtkPointSetToLabelHierarchy()
        hier.SetInputData(pd)
        hier.SetLabelArrayName('label')
        hier.GetTextProperty().SetColor(0.0, 0.0, 0.0)

        lmapper = vtk.vtkLabelPlacementMapper()
        lmapper.SetInputConnection(hier.GetOutputPort())
        # lmapper.SetShapeToRoundedRect()
        # lmapper.SetBackgroundColor(1.0, 1.0, 0.7)
        # lmapper.SetBackgroundOpacity(0.8)
        # lmapper.SetMargin(3)

        lactor = vtk.vtkActor2D()
        lactor.SetMapper(lmapper)


        colors = vtk.vtkNamedColors()
        # Create the points in the grid
        points = vtk.vtkPoints()
        for x in range (width):
            for y in range (height):
                z = self.rating_dist_by_genre[genre_list[x]][y]
                points.InsertNextPoint(x, y, z)

        # Add the grid points to a polydata object
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        glyphFilter = vtk.vtkVertexGlyphFilter()
        glyphFilter.SetInputData(polydata)
        glyphFilter.Update()

        # Create a mapper and actor
        pointsMapper = vtk.vtkPolyDataMapper()
        pointsMapper.SetInputConnection(glyphFilter.GetOutputPort())

        pointsActor = vtk.vtkActor()
        pointsActor.SetMapper(pointsMapper)
        pointsActor.GetProperty().SetPointSize(3)
        pointsActor.GetProperty().SetColor(colors.GetColor3d("Red"))

        # Triangulate the grid points
        delaunay = vtk.vtkDelaunay2D()
        delaunay.SetInputData(polydata)
        delaunay.Update()

        # Create a mapper and actor
        triangulatedMapper = vtk.vtkPolyDataMapper()
        triangulatedMapper.SetInputConnection(delaunay.GetOutputPort())

        triangulatedActor = vtk.vtkActor()
        triangulatedActor.SetMapper(triangulatedMapper)

        # Create a renderer, render window, and interactor
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # Add the actors to the scene
        renderer.AddActor(lactor)
        renderer.AddActor(pointsActor)
        renderer.AddActor(triangulatedActor)
        renderer.SetBackground(colors.GetColor3d("Green")) # Background color green

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
        """Generate a 2D grid in 3D space of 
        """
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