import pandas as pd
import numpy as np
import vtk
from tkinter import *
from vtk.util.colors import *

# Create the GUI
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window(cols=5, rows=5) # Use a 5x5 grid in the main frame

        

    # Creation of init_window
    def init_window(self, rows=5, cols=5):
        # Set the title of the master widget
        self.master.title("Visualization coursework - pbqk24")
        cell_height = 900//rows
        cell_width = 1600//cols

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
        quitButton = Button(self, text="Quit", command=self.client_exit, height=5, width=20)
        # Place the button in the window
        quitButton.grid(column=4, row=4)

        # Create a button instance
        quitButton = Button(self, text="Cube", command=self.vtk_generate_cube, height=5, width=20)
        # Place the button in the window
        quitButton.grid(column=0, row=4)

        # Create a button instance
        quitButton = Button(self, text="Sphere", command=self.vtk_sphere_lighting, height=5, width=20)
        # Place the button in the window
        quitButton.grid(column=1, row=4)


    def client_exit(self):
        exit()

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

    def vtk_sphere_lighting(self):
        # create a rendering window and renderer
        ren = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)

        # create a renderwindowinteractor
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0,0,0)
        source.SetRadius(5.0)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(hot_pink)
        actor.GetProperty().SetSpecularColor(1, 1, 1)
        actor.GetProperty().SetSpecular(0.3)
        actor.GetProperty().SetSpecularPower(20)
        actor.GetProperty().SetAmbient(0.2)
        actor.GetProperty().SetDiffuse(0.8)

        # assign actor to the renderer
        ren.AddActor(actor)

        # enable user interface interactor
        iren.Initialize()
        renWin.Render()
        iren.Start()


# Spawn the GUI
root = Tk()


# Default size of the window
root.geometry("1600x900")

app = Window(root)
root.mainloop()