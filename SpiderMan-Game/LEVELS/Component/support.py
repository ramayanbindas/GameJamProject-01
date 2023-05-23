"""This module contain supportive functonality needed for the game.

	Supported image formats in Pygame include BMP, GIF (non-animated), JPEG,
	LBM (and PBM, PGM, PPM), PCX, PNG, PNM, SVG (limited support, using Nano SVG),
	TGA (uncompressed), TIFF, WEBP, and XPM.

	Some of the functions provided by this module are:
	-`loadPyImageInList`:- return list of pyimages by taking a path as argument
	-`loadPyImageInDict`:- return dict of pyimages by taking a path as argument
	-`filterWithExtension`:-return the file of specific extension from given path contains

	These functions can be used to load images in different formats,
	organize them into lists or dictionaries, and filter files based on specific extensions.

"""
import pygame
import os
from sys import exit

"CONSTANTS"
PYIMGFORMAT = ("BMP", "GIF", "JPEG","LBM",
	"PCX","PNG","PNM","SVG",".TGA","TIFF","WEBP",
	"XPM")
"Local Variable"
pygame_image_list = []
pygame_image_dict = {}

# print(os.getcwd())
def loadPyImgInList(path: str, alpha: bool= True, ext: tuple=PYIMGFORMAT) -> list[pygame.Surface]:
	"""This function automaticaly load the images contain in a directory.
	
	:param path: The path of the directory where the images are located. 
		The function expects the images to be directly present in the specified directory
		or its subdirectories.
    :param alpha: A boolean flag indicating whether to call `pygame.image.convert_alpha()`
	    on the loaded images. Set it to True for transparency support, and False otherwise.
    :param ext: An optional parameter specifying a specific file extension to filter the images.
	    If provided, only files with the specified extension will be loaded.
	    If None, default image format will be loaded.
        For furture information about image formate visit. "https://www.pygame.org/docs/ref/image.html"
    :return: A list of Pygame surfaces representing the loaded images.

    Note: Ensure that the images in the specified directory match the expected format and have the
	    correct file extensions.

	"""
	img_files = getFilesWithExt(path, ext)
	pyimg_list = []

	if not img_files:
		raise ValueError("No imgae present with the extension " + ext)

	# Loding all the images from the directory with provided extension.
	for img in img_files:
		filename = os.path.join(path, img)
		if alpha:
			pyimg = pygame.image.load(filename).convert_alpha()
		else:
			pyimg = pygame.image.load(filename).convert()

		pyimg_list.append(pyimg)

	return pyimg_list

def loadPyImgInDict(path: str, key: str=None, alpha: bool= True,
				 ext: tuple=PYIMGFORMAT) -> dict[str: list[pygame.Surface]]:
	"""This funtion automatically load all the images present in the directory  and returns
		a `dict` of key-value pairs.

	:param path: The path of the directory where the images are located. The function expects
		the images to be directly present in the specified directory or its subdirectories.
    :param key: An optional parameter specifying a specific key to pair with the list of images.
	    If provided, each key-value pair in the resulting `dict` will have the specified key.
    :param alpha: A boolean flag indicating whether to call `pygame.image.convert_alpha()` on the loaded images.
		Set it to True for transparency support, and False otherwise.
    :param ext: An optional parameter specifying a specific file extension to filter the images. If provided,
        only files with the specified extension will be loaded. If None, default image format will be loaded.
        For furture information about image formate visit. "https://www.pygame.org/docs/ref/image.html"
    :return: A dict of key-value pairs where each key is a string and each value is a list of Pygame surfaces.

    Note: Ensure that the images in the specified directory match the expected format and have the correct file extensions.
    """
	pyimg_dict = {}

	# Load PyImg into Dict Logic
	if not key:
		if "/" in path:
			key = path.split("/")[-1]
		elif "\\" in path:
			key = path.split("\\")[-1]

	pyimg_dict[key] = loadPyImgInList(path, alpha, ext)
	return pyimg_dict

def getFilesWithExt(path: str, ext: tuple=PYIMGFORMAT) -> list:
	"""This function manily helpful for retriving specific files for the directory.

	:param path: path of the directory where to look the certain files.
	:param ext: extenstion of file to specify what type of file is to be retirve. if `no extension
		provided` than it loads the images of extension supported by the pygame image module.
		For furthur information about the default extension visit "https://www.pygame.org/docs/ref/image.html".
		And if `ext is "dir"` than it return all the list of directories name present in that directory and if
		`ext is None` it returns list of name of all the files present in the directory including images,
		directories and other file formats.
	 :returns: A list of file names in the directory based on the specified filtering criteria or `empty list`
		 if no such file present.
   
	"""
	files = os.listdir(path)
	if not isinstance(ext, tuple): raise TypeError("Type of ext must be `tuple`")

	ext = [e.upper() for e in ext if e is not None] # if ext is None than it return a empty list
	# print(ext)

	if ext and "DIR" not in ext and ext != []:
		return [file for file in files if file.split(".")[-1].upper() in ext]
	elif "DIR" in ext: # logic for filtering directories
		return [file for file in files if os.path.splitext(file)[1] == ""]
	elif ext == []:
		return files

	# return files

if __name__ == "__main__":
	path_ = "C:\\Users\\Public\\Desktop_\\Cool Projects\\WebSlinger Gravity Chronicles\\SpiderMan-Game\\LEVELS\\Source\\Player"
	print(getFilesWithExt(path_, ("dir", )))