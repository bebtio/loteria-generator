from PIL import Image
import random
import math

import pdb



def generate_loteria_cards( number_of_cards: int ) -> list:

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
                # Currently just reports a message and continues.
                if( are_unique == False ):
                    print("Matching pair")
                    print( current_set )
                    print( test_set)
                    pdb.set_trace()

    return( set_of_loteria_cards )

# Gets a number of samples from a range of values.
# For example: loteria cards have 16 different images from a possible set of 54 images
# calling this function like this
# generate_random_set( 16, 54 ) will generate 16 random numbers from the values 0-53
def generate_random_set( number_of_samples: int, range_of_values: int ) -> list:

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
def check_that_cards_are_unique( first_set: list, second_set: list ) -> bool:
    first_set.sort()
    second_set.sort()

    for index, val in enumerate(first_set):

        if( first_set[index] != second_set[index]):
            return(True)

    # If we never found a mismatching index, then these two sets of values
    # Are the same.
    return( False )


def create_all_loteria_card_images( set_of_loteria_cards: list ):

    card_width  = 12000
    card_height = 14000

    for card_index, card_contents in enumerate( set_of_loteria_cards ):
        
        # Gonna have to decide on a height and width for these cards.
        create_single_loteria_card_image( card_index, card_contents, card_width, card_height )

# Creates one instance of a loteria card and saves it as a png.
# I have no idea what the image sizes are going to be yet so force them to fit inside whatever
# dimensions I give.
def create_single_loteria_card_image( card_number: int, card_contents: list, card_width: int, card_height: int ):

    # open the picture of megaman.
    img = Image.open('megaman.png')

    # Force the picture to be 1/4 the size of the card dimensions.
    image_width  = int(card_width/4)
    image_height = int(card_height/4) 
    img  = img.resize((image_width,image_height))
        
    # Make the spacing between pictures to be the size of an image.
    x_spacing = image_width
    y_spacing = image_height
    
    # Create the loteria card image which the pictures will be paste onto.
    loteria_image = Image.new("RGB", (card_width,card_height), color="white")

    # Loop over the positions and add the pictures to the loteria card image.
    for row in range(4):
        for col in range(4):
            
            x = x_spacing * col
            y = y_spacing * row

            loteria_image.paste( img, (x,y) )

    # Save the image.
    loteria_image.save("Card_" +str(card_number)+".pdf",'PDF',quality=100)


# Start by making a proof of concept that will show we can display images
# a grid and then save off that image.
if __name__ == "__main__":


    pdb.set_trace()

    # Generate a set of cards. Basically an array of arrays.
    # Where the first index is a loteria card and the second index is the 
    # contents of that card, which are 16 numbers representing an image index which 
    # will be used later to actually generate the card.
    
    #set_of_loteria_cards = generate_loteria_cards( 30 )

    # create the cards based on the set_of_loteria_cards array.
    #create_all_loteria_card_images( set_of_loteria_cards )
    
    create_single_loteria_card_image(1, None, 595, 842 )