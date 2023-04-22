from tkinter import *
from PIL import Image
import random

import pdb

# Takes a canvas and converts it to a png image.
def canvas_to_png( canvas, filename_no_ext ):

    filename = filename_no_ext
    
    # Create a temporary post script file.
    canvas.postscript(file=filename + ".eps", colormode="color")

    # Use the image class to open the postscript file.
    img = Image.open(filename + ".eps")

    # use the image class to save the opened file as a png.
    img.save( filename + ".png", "png")

# Gets a number of samples from a range of values.
# For example: loteria cards have 16 different images from a possible set of 54 images
# calling this function like this
# generate_random_set( 16, 54 ) will generate 16 random numbers from the values 0-53
def generate_random_set( number_of_samples, range_of_values ):

    # create our range of possible values.    
    values       = list(range(0, range_of_values))

    # Select number_of_samples of them randomly
    returnValues = random.sample(values, number_of_samples)

    return( returnValues )
    # Get a random number from the values array

    # Remove that value from the values array

    # Repeat until we hit number_of_samples.

    # conveniently, this is what random.sample does.

# Start by making a proof of concept that will show we can display images
# a grid and then save off that image.
if __name__ == "__main__":


    # Create a window
    root = Tk()

    # create a canvas to draw on.
    canvas = Canvas(root, width=1200, height=1400)

    # no idea what this does yet.
    canvas.pack()

    # open the image of megaman.
    img = PhotoImage(file='megaman.png')

    # Draw the image onto the canvas nine times at nine different spots.
    canvas.create_image(200,250,image=img)
    canvas.create_image(575,250,image=img)
    canvas.create_image(950,250,image=img)

    canvas.create_image(200,675,image=img)
    canvas.create_image(575,675,image=img)
    canvas.create_image(950,675,image=img)

    canvas.create_image(200,1100,image=img)
    canvas.create_image(575,1100,image=img)
    canvas.create_image(950,1100,image=img)

    # update the canvas to make sure the images show.
    canvas.update()

    # save the generated image
    canvas_to_png( canvas, "testing123" )

    # Update the canvas and show the image.
    #root.mainloop()

    print("hello world")