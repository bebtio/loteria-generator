from PIL import Image, ImageDraw, ImageFont
import random
import math
import os
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
    pass

# Creates one instance of a loteria card and saves it as a png.
# I have no idea what the image sizes are going to be yet so force them to fit inside whatever
# dimensions I give.
def create_single_loteria_card_image( save_path: str, card_number: int, card_contents: list, card_width: int, card_height: int ):

    # get the images.
    images = card_contents
    
    header_size = int( card_height * .025 )
    # Force the picture to be 1/4 the size of the card dimensions.
    image_width  = int(card_width/4)
    image_height = int((card_height-header_size)/4) 
        
    # Make the spacing between pictures to be the size of an image.
    x_spacing = image_width
    y_spacing = image_height
    
    # Create the loteria card image which the pictures will be paste onto.
    loteria_image = Image.new("RGB", (card_width,card_height+header_size), color="white")

    
    draw_card_text( "Card " + str(card_number+1), loteria_image, 5,10)
    draw_card_text( "Loteria", loteria_image, 500, 10)
    

    # Loop over the positions and add the pictures to the loteria card image.
    for row in range(4):
        for col in range(4):
            
            image_index = row*4 + col 
            img  = images[image_index]
            img  = img.resize((image_width,image_height))

            x = x_spacing * col + 1
            y = y_spacing * row + 1 + header_size * 2

            loteria_image.paste( img, (x,y) )

    # Save the image.
    os.makedirs( save_path,  exist_ok=True )
    output_file_name = save_path + "/" + "Card_" +str(card_number+1)+".pdf"
    loteria_image.save( output_file_name,'PDF',quality=100)

def draw_card_text( text: str, image: Image, x_pos: int, y_pos: int ):
        #pdb.set_trace()
        font = ImageFont.truetype("/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-Regular.ttf",28,encoding="unic")
        ImageDraw.Draw(image).text((x_pos,y_pos), text, fill=(0,0,0,255), font=font )

def get_battlechip_images( filename='megaman_images/battlechips.png' ):
    img = Image.open(filename)

    image_height = 73
    image_width  = 67

    h_start = 0
    w_start = 1
    h_stop  = image_height
    w_stop  = image_width

    images = list()
    for i in range(6):
        for j in range(10):

            # Create the crop indices to pull out indivial sprites from the sprite sheet.
            curr_h_start = h_start      + image_height * i + i
            curr_w_start = w_start      + image_width  * j
            curr_h_stop  = image_height + image_height * i + i
            curr_w_stop  = image_width  + image_width  * j
    
            curr_img = img.crop( ( curr_w_start, curr_h_start , curr_w_stop ,curr_h_stop ) )
            images.append(curr_img)

    return( images )

# Get the images that will be used to generate loteria cards.
def get_loteria_images( path_to_images: str ) -> list():
    
    image_list = list()

    # Loop through the path and find all the images.
    for root, dirs, files in os.walk( path_to_images ):
        for file in files:

            # Get the absolute path of the current image.
            p = os.path.join(root,file)
            p = os.path.abspath(p)

            # Open it as an image object.
            img = Image.open(p)
            image_list.append(img)

    return(image_list)

# Start by making a proof of concept that will show we can display images
# a grid and then save off that image.
if __name__ == "__main__":


    # Load the images from the location which they are stored.

    images = get_loteria_images( "loteria_images" )
    
    # Generate a set of cards. Basically an array of arrays of integers.
    # Where the first index is a loteria card and the second index is the 
    # contents of that card, which are 16 integers representing an image index which 
    # will be used later to actually pull a card from the images list.
    set_of_loteria_cards = generate_loteria_cards( 4 )

    # create the cards based on the set_of_loteria_cards array.
    #create_all_loteria_card_images( set_of_loteria_cards )

    
    images_to_make = list()
    
    # Loop through each of the numerical representations of each loteria card.
    for card_index, x in enumerate(set_of_loteria_cards):

        # Pull out the integers that represent each image and store them in the images_to_make list.
        for image_index in x:
            images_to_make.append(images[image_index % 5])

        # Pass the card index, the images for this loteria card, and the card dimensions to the function
        # that will generate a single loteria card.
        create_single_loteria_card_image("test_loteria_cards", card_index, images_to_make, 595, 842 )
        
        # Erase the contents of the list containing the images for the
        # current loteria card and repeat until all cards are generated.
        images_to_make.clear()