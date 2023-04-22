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

# compare two number sets and ensure that their elements are different by at least 1.
# we can do this by sorting them numerically and them comparing them until a single element
# differs. When that happens, return true. Otherwise return false.
def check_that_cards_are_unique( first_set, second_set ):
    first_set.sort()
    second_set.sort()

    for index, val in enumerate(first_set):

        if( first_set[index] != second_set[index]):
            return(True)

    # If we never found a mismatching index, then these two sets of values
    # Are the same.
    return( False )

def generate_loteria_cards( number_of_cards ):

    # Loteria cards have 16 spaces and 54 images that those spaces can be.
    number_of_images     = 16
    total_to_choose_from = 54
    set_of_loteria_cards = list()

    # Loop through number of loteria cards to be generated.
    for card_index in range(0,number_of_cards):
        
        current_card =  generate_random_set( number_of_images, total_to_choose_from )

        set_of_loteria_cards.append(current_card)

        # Add logic here to test for uniqueness between the currently generated set and all the previous ones.
        # This is a brute force approach that can get slow.
        # With the small set being generated in this project... this probably doesn't matter... 
        if( len( set_of_loteria_cards ) > 1 ):
            
            # TODO move this all to its own function.

            # Get the most recently generated set.
            current_set = set_of_loteria_cards[card_index]

            for test_index in range(0,card_index):
                
                # Get the set to test agaist the current set.
                test_set = set_of_loteria_cards[test_index]
            
                # Compare them to check that they are unique.
                are_unique = check_that_cards_are_unique( current_set, test_set)
            
                # If they aren't unique... then the current set is bad and needs to be regenerated.
                if( are_unique == False ):
                    print("Matching pair")
                    print( current_set )
                    print( test_set)
                    pdb.set_trace()

    return( set_of_loteria_cards )

def create_all_loteria_card_images( set_of_loteria_cards ):

    card_width  = 12000
    card_height = 14000

    for card_index, card_contents in enumerate( set_of_loteria_cards ):
        
        # Gonna have to decide on a height and width for these cards.
        create_loteria_card_image( card_index, card_contents, card_width, card_height )

# Creates one instance of a loteria card and saves it as a png.
def create_loteria_card_image( card_number, card_contents, card_width, card_height ):

    # Create a window
    root = Tk()

    # create a canvas to draw on.
    canvas = Canvas(root, width=card_width, height=card_height)

    # no idea what this does yet.
    canvas.pack()

    # open the image of megaman.
    img = PhotoImage(file='megaman.png')

    # Will find a way to dynamically set these based in card_width and card_height.
    canvas.create_text( 300, 10, text="Loteria",                  font=("Helvetica", "15", "bold") )
    canvas.create_text( 900, 10, text="Card " + str(card_number), font=("Helvetica", "15", "bold") )
    # Draw the image onto the canvas nine times at nine different spots.
    canvas.create_image( 200, 250, image=img )
    canvas.create_image( 575, 250, image=img )
    canvas.create_image( 950, 250, image=img )

    canvas.create_image( 200, 675, image=img )
    canvas.create_image( 575, 675, image=img )
    canvas.create_image( 950, 675, image=img )

    canvas.create_image( 200, 1100, image=img )
    canvas.create_image( 575, 1100, image=img )
    canvas.create_image( 950, 1100, image=img )

    # update the canvas to make sure the images show.
    canvas.update()

    # save the generated image
    canvas_to_png( canvas, "Card_" + str(card_number) )

# Start by making a proof of concept that will show we can display images
# a grid and then save off that image.
if __name__ == "__main__":


    pdb.set_trace()

    # Generate a set of cards. Basically an array of arrays.
    # Where the first index is a loteria card and the second index is the 
    # contents of that card, which are 16 numbers representing an image index which 
    # will be used later to actually generate the card.
    set_of_loteria_cards = generate_loteria_cards( 30 )

    # create the cards based on the set_of_loteria_cards array.
    #create_all_loteria_card_images( set_of_loteria_cards )
    