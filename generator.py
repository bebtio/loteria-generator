from PIL import Image, ImageDraw, ImageFont
import math
import random
import os
import argparse

import pdb

###########################################################################
# Main function:
# Reads in arguments from the command line and
# generates Loteria cards based on that input.
###########################################################################
def main():

    parser = argparse.ArgumentParser( 
                                      prog="LoteriaCardGenerator",
                                      description="Takes a directory filled with images and generates a given number of Loteria cards based on those images."
                                    )

    parser.add_argument( "-n", "--num_cards_to_generate" , type=int, default=1       , help="The number of loteria cards that will be generated."                                                          )
    parser.add_argument( "-l", "--load_path"             , type=str, default="images", help="The path where the images used to generate loteria cards are expected to be."                                 )
    parser.add_argument( "-s", "--save_path"             , type=str, default="output", help="The path where the generated cards will be stored."                                                           )
    parser.add_argument( "-x", "--card_width"            , type=int, default=595*2   , help="The width of the Loteria card in pixels."                                                                     )
    parser.add_argument( "-y", "--card_height"           , type=int, default=842*2   , help="The height of the Loteria card in pixels."                                                                    )
    parser.add_argument( "-d", "--num_deck_pages"        , type=int, default=1       , help="The number of pages to split the deck pages into."                                                            )
    parser.add_argument( "-i", "--num_images_on_card"    , type=int, default=16      , help="The number of images that will appear on each card. Must be a perfect square. If you want it to look good."   )
    
    args = parser.parse_args()

    # Run the generator.
    create_all_loteria_card_images( args.num_cards_to_generate, args.load_path, args.save_path, args.card_width, args.card_height, args.num_images_on_card )
    create_loteria_draw_pile( args.card_width, args.card_height, args.load_path, args.save_path, args.num_deck_pages )

###########################################################################
# create_all_loteria_card_images:
# Description: Generates all Loteria cards based on the inputs.
# num_cards_to_generate: The number of unique Loteria cards to generate.
# load_path:             The path where the images used to make the cards
#                        are stored.
# save_path:             The location to save the generated cards.
# card_width:            The width in pixels to make the cards.
# card_height:           The height in pixels to make the cards.
###########################################################################
def create_all_loteria_card_images( num_cards_to_generate: int, load_path: str, save_path: str, card_width: int, card_height: int, num_images_on_card: int ):
    
    # Load the images from the location which they are stored.
    images = load_loteria_images( load_path )
   
    # Generate a set of cards. Basically an array of arrays of integers.
    # Where the first index is a Loteria card and the second index is the 
    # contents of that card, which are 16 integers representing an image index which 
    # will be used later to actually pull a card from the images list.
    set_of_loteria_cards = generate_loteria_card_image_indices( num_cards_to_generate, num_images_on_card, len(images) )

    images_to_make = list()
    
    # Loop through each of the numerical representations of each Loteria card.
    for card_index, x in enumerate( set_of_loteria_cards ):

        # Pull out the integers that represent each image and store them in the images_to_make list.
        for image_index in x:

            images_to_make.append( images [image_index] )

        # Pass the card index, the images for this Loteria card, and the card dimensions to the function
        # that will generate a single Loteria card.
        create_single_loteria_card_image( save_path , card_index, images_to_make, card_width, card_height )
        
        # Erase the contents of the list containing the images for the
        # current Loteria card and repeat until all cards are generated.
        images_to_make.clear()

###########################################################################
# load_loteria_images:
# Description:    Loads the images from a given path.
# path_to_images: The path where the images are stored.
#
# image_list: The list of images that were loaded.
###########################################################################
def load_loteria_images( path_to_images: str ) -> list():
    
    # Empty list to store the images that are being loaded.
    image_list = list()

    # Loop through the path and find all the images.
    for root, dirs, files in os.walk( path_to_images ):
        for file in files:

            # Get the absolute path of the current image.
            p = os.path.join( root, file )
            p = os.path.abspath( p )

            # Open it as an image object.
            img = Image.open( p )
            image_list.append( img )

    # Return all the images found.
    return( image_list )

###########################################################################
# generate_loteria_card_image_indices:
# Description:     Generates a list of indices for each card that will be generated.
# Each list of of indices will contain number_of_images number of integers from the
# range of 0-total_number_of_images. Each list will then be used index into another
# list of containing image objects to paste onto an image that will represent a single
# Loteria card. 
# 
# For example, Loteria cards traditionally have 16 images from a possible
# 54. If you want to generate 4 Loteria cards, function will return 4 lists,
# each containing 16 integers in the range frome 0 to 53, each number in that range
# representing one of the 54 possible Loteria cards.
#                  
# number_of_cards: The number of Cards to generate indices for.
# number_of_images: The number of images that will go onto a single Loteria card.
# total_number_of_images: The total number of images that are available to choose from.
###########################################################################
def generate_loteria_card_image_indices( number_of_cards: int, number_of_images: int, total_number_of_images: int ) -> list:

    # Loteria cards have 16 spaces and 54 images that those spaces can be.
    set_of_loteria_cards = list()

    # Loop through number of loteria cards to be generated.
    current_card =  generate_random_set( number_of_images, total_number_of_images )
    set_of_loteria_cards.append( current_card )

    current_card =  generate_random_set( number_of_images, total_number_of_images )
    set_of_loteria_cards.append( current_card )
    
    card_index = 1

    # Keep generating cards until the number of unique cards is what is requested.
    # Before doing that, we need to check that we can even generate that many unique cards.
    if( False == check_if_number_of_cards_possible( number_of_cards, number_of_images, total_number_of_images ) ):
        print("Error: The number of Loteria cards requested cannot be generated with the number of images given" )
        exit()
        
    while card_index < number_of_cards - 1:
    
        # Loop through number of loteria cards to be generated.
        current_card =  generate_random_set( number_of_images, total_number_of_images )

        # Add logic here to test for uniqueness between the currently generated set and all the previous ones.
        # This is a brute force approach that can get slow.
        # With the small set being generated in this project... this probably doesn't matter... 
        if( len( set_of_loteria_cards ) > 1 ):
            
            # Get the most recently generated set.
            current_set = current_card

            are_unique = True

            for test_index in range( 0, card_index ):
                
                # Get the set to test agaist the current set.
                test_set = set_of_loteria_cards[ test_index ]
            
                # Compare them to check that they are unique.
                are_unique = check_that_cards_are_unique( current_set, test_set )
            
                # If they aren't unique... then the current set is bad and needs to be regenerated.
                # break out of the current loop and re-generate.
                if( are_unique == False ):
                    break

            # Only add if card is unique.
            if( are_unique ):
                set_of_loteria_cards.append( current_card )
                card_index += 1

    return( set_of_loteria_cards )

###########################################################################
# check_if_number_of_cards_possible.
# Description: Checks that it is possible to unique generate the number of cards
# requested from the list of images given.
# number_of_cards:        The number of loteria cards to generate.
# number_of_images:       Number of images that will go onto a single loteria card.
# total_number_of_images: Total number of images passed to this program to generate loteria cards.
###########################################################################
def check_if_number_of_cards_possible( number_of_cards: int, number_of_images: int, total_number_of_images: int   ) -> bool:

    # Performs 
    #    n!
    # -------
    # k!(n-k)!    
    # Which computes the number of ways you can uniquely pick k number of items from a set of n things with out repitition.
    possible_combinations = math.factorial( total_number_of_images ) / (math.factorial( number_of_images ) * math.factorial( total_number_of_images-number_of_images) )
    
    # If the number of loteria cards requested exceeds this computed value, then we can't 
    # generate enough unique cards to meet user requirements.
    if( number_of_cards > possible_combinations ):
        return( False )
    else: 
        return( True )

###########################################################################
# generate_random_set.
# Description: Samples a set of number_of_samples integers from the range
# range_of_values and returns that set of numbers as a list. 
# number_of_samples: Number of values to pull from range_of_values.
# range_of_values:   Set of possible values the samples can be.
###########################################################################
def generate_random_set( number_of_samples: int, range_of_values: int ) -> list:

    # create our range of possible values.    
    values       = list( range( 0, range_of_values ) )

    # Select number_of_samples of them randomly
    returnValues = random.sample( values, number_of_samples )

    return( returnValues )

###########################################################################
# check_that_cards_are_unique
# Description: Compares two number sets and checks that their elements are different by at least 1.
# we can do this by sorting them numerically and them comparing them until a single element
# differs. When that happens, the set is unique and return true. Otherwise return false.
# first_set:  First set of numbers to perform comparison.
# second_set: Second set of numbers to perform comparison.
###########################################################################
def check_that_cards_are_unique( first_set: list, second_set: list ) -> bool:

    # Make copies so we don't modify the original when we sort.
    first = first_set.copy()
    second = second_set.copy()

    # Sort the sets so we can compare them element by element.
    first.sort()
    second.sort()

    # Compare sets element by element. 
    # The only way these are not unique is if we iterate over the whole set
    # and we never find a mismatching pair.
    # enumerate works here because first_set and second_set will be the same size.
    for index, val in enumerate ( first ):
        
        # As soon as we find a mismatching pair, return.
        if( first[ index ] != second[ index ]):
            return( True )

    # If we never found a mismatching index, then these two sets of values
    # Are the same.
    return( False )

###########################################################################
# create_single_loteria_card_image
# Description: Currently creates only 4x4 loteria cards with 16 images in them.
# Creates one instance of a Loteria card and saves it as a png.
# save_path:     The path to save the Loteria card.
# card_number:   The number to print onto the header of the card.
# card_contents: The list of images that will be printed onto the card.
# card_width:    The width of the card in pixels.
# card_height:   The height of the card in pixels.
###########################################################################
def create_single_loteria_card_image( save_path: str, card_number: int, card_contents: list, card_width: int, card_height: int ):

    # Set the images to a local variable.
    images = card_contents

    # Create the Loteria card image which the pictures will be paste onto.
    loteria_image = Image.new( "RGB", ( card_width, card_height ), color="white" )

    # The header a fraction of the card height.
    header_size = int( card_height * .04 )

    # Make the part of the card that displays the Loteria images the total height of the card
    # minues the size of the header.
    image_display_height = card_height-header_size

    # Draw the text that goes into the header.
    draw_card_text( "Carta " + str( card_number + 1 ), loteria_image, 5, 0 )
    draw_card_text( "Feliz 50 años Veronica!", loteria_image, card_width * .25, 0 )
    draw_card_text( "Loteria", loteria_image, card_width * .85, 0 )

    # Paste the Loteria images into the the Loteria card in a 4x4 grid.
    loteria_image = paste_grid_of_images( loteria_image, card_contents, card_width, image_display_height, 0, header_size, 4, 4 )

    # Save the image.
    card_filename = "Card_" + str( card_number + 1 )
    save_loteria_card_as_pdf( loteria_image, save_path, card_filename )

###########################################################################
# paste_grid_of_images
# Description: Takes an image and a list of sub images. Pastes the sub images
# onto the main_image in a grid pattern.
# main_image:       The main image. Sub images will be pasted onto this.
# images_to_paste:  The list of images that will be pasted onto the main image.
# paste_area_width: The width of the area, in pixels, that the pasting will cover.
# paste_area_height:The height of the area, in pixels, that the pasting will cover.
# x_offset:         The x position where the pasting will begin.
# y_offset:         The y position where the pasting will begin.
# num_x_elements:   The number of x ( row )elements to sub divide the paste area.
# num_y_elements:   The number of y ( column ) elements to sub divide the paste area.
###########################################################################
def paste_grid_of_images( main_image, images_to_paste: list, paste_area_width: int, paste_area_height: int, x_offset = 0, y_offset= 0, num_x_elements = 4, num_y_elements = 4 ):
    
    # Force each image to be 1/4 the size of the card dimensions.
    paste_image_width         = ( paste_area_width // num_x_elements )
    paste_image_height        = ( paste_area_height // num_y_elements ) 
        
    # Make the spacing between pictures to be the size of an image plus.
    x_spacing = paste_image_width 
    y_spacing = paste_image_height

    # Loop over the positions indices and add the pictures to the Loteria card image.
    for row in range( num_y_elements ):
        for col in range( num_x_elements ):
            
            # Compute the linear index of the image.
            image_index = ( row * num_x_elements ) + col 

            # Pull out the image and resize it to fit within a 4x4 grid on the
            # Loteria card.
            # If we ask for more images than exist in the images_to_paste list, set the current image
            # to a blank image.
            if( image_index >= len( images_to_paste ) ):
                img = Image.new( "RGB", ( paste_image_width, paste_image_height ), color="white" )
            else:
                img  = images_to_paste[ image_index ]
            
            # Resive the image from its native dimensions to dimensions that will
            # fit our grid.
            img  = img.resize( ( paste_image_width, paste_image_height ) )

            # Compute the x ( width positioning ) and the y, ( height positioning )
            # of each image onto the Loteria page.
            x = x_spacing * col
            y = y_spacing * row + y_offset

            # Paste the current image.
            main_image.paste( img,  ( x, y ) )

    return( main_image )

###########################################################################
# draw_card_text
# Description: Draws card text  onto the image at position ( x_pos, y_pos )
# text:  The text to draw on the image.
# image: The image to draw text on.
# x_pos: The x position to draw the text.
# y_pos: The y position to draw the text.
###########################################################################
def draw_card_text( text: str, image: Image, x_pos: int, y_pos: int ):
        
        font = ImageFont.truetype( "/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-Regular.ttf", 56, encoding="unic" )
        
        ImageDraw.Draw( image ).text( ( x_pos, y_pos ), text, fill=(0,0,0,255), font=font )

###########################################################################
# save_loteria_card_as_pdf
# Description:   saves the image as a pdf.
# loteria_image: The image object to save.
# save_path:     The location to save the image.
# filename:      The filename to give the saved file.
###########################################################################
def save_loteria_card_as_pdf( loteria_image, save_path: str, filename: str ):
    
    # Make the output directory if it does not exist.
    os.makedirs( save_path,  exist_ok=True )
    
    # Create the output file name.
    output_file_name = save_path + "/" + filename +".pdf"
    
    # Call the save function.
    loteria_image.save( output_file_name,'PDF', quality=100)

###########################################################################
# save_loteria_draw_pile
# Description: Takes all the images that make up this loteria game and
# saves them to a number of pages, evenly spaced out.
# WIP
###########################################################################
def create_loteria_draw_pile( image_width: int, image_height: int, load_path: list, save_path: str, number_of_pages: int ):
    
    # Load the images and count the number of cards available.
    loteria_card_images = load_loteria_images( load_path )
    number_of_cards = len( loteria_card_images )
    
    
    # Based on how many pages are requested, divide the cards up between pages as
    # evenly as possible.
    cards_per_page  = int( math.ceil( number_of_cards / number_of_pages ) )

    page_images = list()

    for i in range(0, number_of_cards, cards_per_page ):
        page_images.append( loteria_card_images[i:i + cards_per_page] )

    # In order to display the image across all pages with even heights and widths
    # we must paste a square grid.
    # Compute the necessary number of elements on each row and column to complete
    # a square grid if we don't have enough images to fill each page.
    next_square_value = 2
    while( math.pow(next_square_value, 2 ) < cards_per_page ):
        next_square_value += 1
    

    # Make a new image for the draw pile.
    draw_pile_image = Image.new( "RGB", ( image_width, image_height ), color="white" )

    for draw_pile_id, curr_draw_pile in enumerate( page_images ):

        # Draw a square grid 
        image = paste_grid_of_images( draw_pile_image, page_images[ draw_pile_id ], image_width, image_height, 0,0, next_square_value, next_square_value )

        output_file_name = save_path + "/" + "Deck_" + str( draw_pile_id + 1 ) + ".pdf"
        image.save( output_file_name, 'PDF', quality=100 )

if __name__ == "__main__":
    main()
