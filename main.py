#'Cause I'm sweet as cinnamon
#Don't know what to say to him
#Told you I would change
#But the years have proved me wrong
#When you told me I should grow up
#I thought that I would throw up
#Funny how a simple phrase can push me off the edge
#'Cause I'm bitter like cinnamon
#I can't bear to look at him
#Help me take my mind just to focus on my steps
#When you told me I should grow up
#I thought that I would throw up
#Funny how a simple phrase can push me off the edge

# UGA 3rd Anniversary Ditherer by soreikomori

from PIL import Image
import json
import hitherdither
import os

# PixelPlace Palette loading
id_dict = {"#FFFFFF": 0,"#C4C4C4": 1,"#A6A6A6": 60,"#888888": 2,"#6F6F6F": 61,"#555555": 3,"#3A3A3A": 62,"#222222": 4,"#000000": 5,"#003638": 39,"#006600": 6,"#477050": 40,"#1B7400": 49,"#22B14C": 7,"#02BE01": 8,"#51E119": 9,"#94E044": 10,"#34EB6B": 51,"#98FB98": 41,"#75CEA9": 50,"#CAFF70": 58,"#FBFF5B": 11,"#E5D900": 12,"#FFCC00": 52,"#C1A162": 57,"#E6BE0C": 13,"#E59500": 14,"#FF7000": 42,"#FF3904": 21,"#E50000": 20,"#CE2939": 43,"#FF416A": 44,"#9F0000": 19,"#4D082C": 63,"#6B0000": 18,"#440414": 55,"#FF755F": 23,"#A06A42": 15,"#633C1F": 17,"#99530D": 16,"#BB4F00": 22,"#FFC49F": 24,"#FFDFCC": 25,"#FF7EBB": 54,"#FFA7D1": 26,"#EC08EC": 28,"#BB276C": 53,"#CF6EE4": 27,"#7D26CD": 45,"#820080": 29,"#591C91": 56,"#330077": 46,"#020763": 31,"#5100FF": 30,"#0000EA": 32,"#044BFF": 33,"#013182": 59,"#005BA1": 47,"#6583CF": 34,"#36BAFF": 35,"#0083C7": 36,"#00D3DD": 37,"#45FFC8": 38,"#B5E8EE": 48}

#region # Logic Layer

def load_palette():
    """Loads the palette from a JSON file.
    
    Returns
    -------
    hitherdither.palette.Palette
        The loaded palette.
    """
    hitherPalette = []
    for key in id_dict:
        hitherPalette.append(key)
    return hitherdither.palette.Palette(hitherPalette)

def image_exists(imageName):
    """Checks if the image file exists in the current directory.
    
    Parameters
    ----------
    imageName : str
        The name of the image file without the extension.
    """
    try:
        global image_path
        image_path = os.path.join(os.getcwd(), imageName)
        os.path.isfile(image_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file '{imageName}' not found. Please check the file name and try again.")

def load_image(image_path):
    """Loads an image from a file.
    
    Parameters
    ----------
    image_path : str
        Path to the image file.
        
    Returns
    -------
    PIL.Image.Image
        The loaded image.
    """
    return Image.open(image_path)

def transparency_handler(image):
    """If the image has transparency, save the transparent part as another image to use later, then save the original image as RGB for dithering.
    
    Parameters
    ----------
    image : PIL.Image.Image
        The image to be processed.
    
    Returns
    -------
    PIL.Image.Image
        The processed image.
    """
    transparent_image = None
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        image = image.convert("RGBA")
        # Save the transparent part as another image
        transparent_image = Image.new('RGBA', image.size, (255, 255, 255, 0))
        transparentChannel = image.getchannel('A')
        for x in range(image.width):
            for y in range(image.height):
                if transparentChannel.getpixel((x, y)) == 0:
                    # Replace all transparent pixels with #FFDFCC
                    transparent_image.putpixel((x, y), (255, 223, 204, 255))
        image = image.convert('RGB')
    return image, transparent_image

def dither(image, palette, method_number):
    """Applies dithering to the image using the specified method.

    Parameters
    ----------
    image : PIL.Image.Image
        The image to be dithered.
    palette : hitherdither.palette.Palette
        The palette to be used for dithering.
    method : str
        The dithering method to be used. Options are 'floyd-steinberg', 'atkinson', 'jarvis-judice-ninke', 'stucki', 'burkes', 'sierra3', and 'sierra2'.

    Returns
    -------
    PIL.Image.Image
        The dithered image.
    """
    methods = {'1': 'floyd-steinberg', '2': 'atkinson', '3': 'jarvis-judice-ninke', '4': 'stucki', '5': 'burkes', '6': 'sierra3', '7': 'sierra2'}
    method = methods.get(method_number, None)
    try:
        # Convert image to RGB mode if it has transparency
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = image.convert('RGB')
        # Ensure the image is in RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return hitherdither.diffusion.error_diffusion_dithering(image, palette, method=method)
    except Exception as e:
        print(f"Error during dithering: {e}")
        return None

def save_image(image, filename):
    """Saves the image to a file.
    
    Parameters
    ----------
    image : PIL.Image.Image
        The image to be saved.
    filename : str
        The name of the file to save the image to.
    """
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        image = image.convert('RGB')  # Convert to RGB mode for JPEG
    image.save(filename)

def get_hex_color(r, g, b):
    """Converts a pixel to hex color format.
    
    Parameters
    ----------
    r : int
        Red channel value.
    g : int
        Green channel value.
    b : int
        Blue channel value.
        
    Returns
    -------
    str
        Hex color string in the format #RRGGBB.
    """
    return '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()

def extract_pixels(image_dithered):
    """Extracts pixel data from the dithered image.
    
    Parameters
    ----------
    image_dithered : PIL.Image.Image
        The dithered image.
        
    Returns
    -------
    list
        List of pixel values.
    """
    if image_dithered.mode in ('RGBA', 'LA') or (image_dithered.mode == 'P' and 'transparency' in image_dithered.info):   
        pixels = list(image_dithered.convert('RGBA').getdata())
    else:
        # Convert to RGB if not already in that mode
        image_dithered = image_dithered.convert('RGB')
        pixels = list(image_dithered.getdata())
    return pixels

def get_arraystring(image_dithered, pixels, id_dict):
    """Writes the pixel data to a string in a specific format.
    
    Parameters
    ----------
    image_dithered : PIL.Image.Image
        The dithered image.
    pixels : list
        List of pixel values.
    id_dict : dict
        Dictionary mapping hex colors to IDs.
    
    Returns
    -------
    str
        The formatted pixel data as a string.
    """
    result = []
    result.append("[")
    for row in range(image_dithered.height):
        result.append("[")
        for col in range(image_dithered.width):
            # Get the pixel value at (row, col)
            pixel = pixels[row * image_dithered.width + col]
            if len(pixel) == 4:
                # If the pixel has an alpha channel, ignore it
                r, g, b, _ = pixel[:3]
            else:
                # If the pixel is RGB, unpack it directly
                r, g, b = pixel
            hex_color = get_hex_color(r, g, b)
            # Check if the hex color exists in the dictionary
            if hex_color in id_dict:
                # Get the ID from the dictionary
                id_value = id_dict[hex_color]
                # Check if this is the last pixel in the row
                if col == image_dithered.width - 1:
                    result.append(f"{id_value}")
                else:
                    result.append(f"{id_value},")
            else:
                print(f"Color {hex_color} not found in dictionary.")
        # Check if this is the last row
        if row == image_dithered.height - 1:
            result.append("]")
        else:
            result.append("],")
    result.append("]")
    return ''.join(result)

def write_to_file(arraystring, filename):
    """
    Writes the pixel data to a file in a specific format.

    Parameters
    ----------
    arraystring : str
        The pixel data as a string.
    filename : str
        The name of the file to save the pixel data to.
    """
    with open(filename, 'w') as f:
        f.write(arraystring)

def transparency_fixer(arraystring, transparent_image, id_dict):
    """
    Receives the final arraystring and the transparent image, then goes through the transparent image and gets an arraystring for it (where it will only find #FFDFCC).
    Once it has the transparent image's arraystring, it replaces whichever pixel in the original arraystring with 255 that corresponds to the transparent pixel in the transparent image.
    For example, if the original arraystring is: [[0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1]] and the transparent image's arraystring is [[25,25,25,25,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,25,25,25,25]], then the final arraystring will be [[255,255,255,255,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,255,255,255,255]].
    
    Parameters
    ----------
    arraystring : str
        The array string to be processed.
    transparent_image : PIL.Image.Image
        The transparent image to be used for replacement.
    id_dict : dict
        Dictionary mapping hex colors to IDs.

    Returns
    -------
    str
        The processed array string with transparent pixels replaced.
    """
    # Convert image to RGB mode if it has transparency
    if transparent_image.mode in ('RGBA', 'LA') or (transparent_image.mode == 'P' and 'transparency' in transparent_image.info):
        transparent_image = transparent_image.convert('RGB')
    # Ensure the image is in RGB mode
    if transparent_image.mode != 'RGB':
        transparent_image = transparent_image.convert('RGB')
    # Get arraystring
    pixels = extract_pixels(transparent_image)
    trArraystring = get_arraystring(transparent_image, pixels, id_dict)
    # Replacement
    # Convert the arraystring to a list of lists
    arraystring = arraystring[1:-1].split("],")
    arraystring = [row[1:-1].split(",") for row in arraystring]
    # Convert the transparent arraystring to a list of lists
    trArraystring = trArraystring[1:-1].split("],")
    trArraystring = [row[1:-1].split(",") for row in trArraystring]
    # Replace the pixels in the original arraystring with 255 where the transparent image has 255
    for row in range(len(arraystring)):
        for col in range(len(arraystring[row])):
            if trArraystring[row][col] != '0':
                arraystring[row][col] = '255'
    # Convert the arraystring back to a string
    finalstring = "["
    for row in range(len(arraystring)):
        finalstring += "["
        for col in range(len(arraystring[row])):
            if col == len(arraystring[row]) - 1:
                finalstring += arraystring[row][col]
            else:
                finalstring += arraystring[row][col] + ","
        # Check if this is the last row
        if row == len(arraystring) - 1:
            finalstring += "]"
        else:
            finalstring += "],"
    return finalstring+"]"
    

#endregion # Logic Layer

#region # View Layer 

def main():
    print("UGA 3rd Anniversary Ditherer")
    print("by soreikomori <3")
    print("") # -------------------
    # Palette loading
    print("Loading palette...")
    palette = load_palette()
    print("Palette loaded.")
    print("") # -------------------
    # Image name loop
    print("Enter the image name with the extension. It should be right next to this exe.")
    print("Example: image.png")
    print("The image should be resized firsthand.")
    while True:
        imageName = input("Image name: ")
        # Get the image file with the correct extension
        try:
            image_exists(imageName)
            break
        except FileNotFoundError as e:
            print(e)
    print("") # -------------------
    # Load the image
    print("Loading image...")
    image = load_image(image_path)
    image, transparentImage = transparency_handler(image)
    print("Image loaded.")
    print("") # -------------------
    # Dithering
    ditherAccepted = False
    while not ditherAccepted:
        print("You can try https://ditherit.com/ to check out all the dithering methods. Choose one that you like.")
        print("There's a custom palette that you can import from the #anniversary-info channel for maximum accuracy in pixelplace.")
        print("Select a dithering method:")
        print("1. Floyd-Steinberg (Recommended!)")
        print("2. Atkinson")
        print("3. Jarvis-Judice-Ninke")
        print("4. Stucki")
        print("5. Burkes")
        print("6. Sierra3")
        print("7. Sierra2")
        while True:
            method = input("Dithering method (1-9): ")
            if method in ['1', '2', '3', '4', '5', '6', '7']:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 7.")
        print("Dithering...")
        dithered_image = dither(image, palette, method)
        if dithered_image is None:
            print("Dithering failed! Please try again, maybe with another method.")
            print("")
        else:
            print("Dithering complete.")
            print("") # -------------------
            # Save the dithered image
            print("Saving dithered image...")
            splitFilename = imageName.split(".")
            imageNameRaw = splitFilename[0]
            extension = "." + splitFilename[1]
            ditheredFilename = f"{imageNameRaw}_dithered{extension}"
            save_image(dithered_image, ditheredFilename)
            print(f"Dithered image saved as {ditheredFilename}.")
            print("Take a look. Do you like it?")
            print("If you don't like it, then you will be taken to the dithering method selection screen.")
            while True:
                ditherAcceptedInput = input("Do you want to continue? (y/n): ")
                if ditherAcceptedInput in ['y', 'Y', 'yes', 'Yes']:
                    ditherAccepted = True
                    break
                elif ditherAcceptedInput in ['n', 'N', 'no', 'No']:
                    ditherAccepted = False
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
    print("") # -------------------
    # Generate array
    print("Generating array for pixelplace...")
    pixels = extract_pixels(dithered_image)
    arrayFilename = f"{imageNameRaw}_array.txt"
    arraystring = get_arraystring(dithered_image, pixels, id_dict)
    if transparentImage is not None:
        arraystring = transparency_fixer(arraystring, transparentImage, id_dict)
    write_to_file(arraystring, arrayFilename)
    print(f"Array generated. You can see it over at {arrayFilename}.")
    print("") # -------------------
    # End of program
    print("Thanks for using my tool! Any bugs just ping me.")
    input("Press Enter to exit...") 
#endregion # View Layer
main()