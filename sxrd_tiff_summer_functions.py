import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
from skimage import io
import pathlib
from tqdm import tqdm
import os
import yaml
from typing import Tuple
from typing import List

def get_config(path: str) -> dict:
    """Open a yaml file and return the contents."""
    with open(path) as input_file:
        return yaml.safe_load(input_file)
    
def get_experiment_numbers(start: int, end: int, step: int) -> List[int]:
    """Return a list of sequential image numbers given start, end and step."""
    experiment_numbers = list(range(start, end + 1, step))
    return experiment_numbers

def extract_input(config_path: str):
    """Extract user inputs from yaml configuration file. 
    Extract input, output and background scattering file paths, 
    as well as a list of experiment numbers.
    
    :param config_path: path to the configuration file.
    
    :return: experiment numbers, input path for the .tiff images, 
    output path for the summed/averaged tiff image 
    - as strings and a list of integers.
    """
    config = get_config(config_path)
    start = config["experiment_numbers"]["start"]
    end = config["experiment_numbers"]["end"]
    step = config["experiment_numbers"]["step"]
    experiment_numbers = get_experiment_numbers(start, end, step)
    print("The series of experiment numbers is :", experiment_numbers, sep = '\n', end = '\n\n')

    input_path = config["file_paths"]["input_path"]
    print("The input path to the series of images is :", input_path, sep = '\n', end = '\n\n')

    output_path = config["file_paths"]["output_path"]
    print("The output path to save the adjusted image(s) is :", output_path, sep = '\n', end = '\n\n')
    
    background_scatter_path = config["file_paths"]["background_scatter_path"]
    print("The path to the background scatter image is :", background_scatter_path, sep = '\n', end = '\n\n')
    
    background_scatter_multiple = config["file_paths"]["background_scatter_multiple"]
    print("The value to multiply the background scatter intensity, to match the acquisition frequency of the data, is :", background_scatter_multiple, sep = '\n', end = '\n\n')
    
    return experiment_numbers, input_path, output_path, background_scatter_path, background_scatter_multiple
    
def avg_tiff_images(experiment_number: str, input_filepath: str, output_filepath: str, v_max: int):
    '''Sum up the intensities of all the tiff images contained in the input folder
    and save a single average tiff image to the output folder.
    
    :param experiment_number: input experiment number.
    :param input_filepath: input path to the series of tiff images.
    :param output_filepath: output path to save the single summed/averaged tiff image.
    :param v_max: intensity maxima for plotting the summed/averaged diffraction pattern image.
    '''
    image_list = sorted(pathlib.Path(input_filepath).glob("0*.tiff"))
    
    # set the image arrays to zero to prevent unusual memory allocation
    image_example = io.imread(image_list[1])
    image_array = np.zeros(shape=np.shape(image_example), dtype='int32')

    for image_path in tqdm(image_list):
        image_array = image_array + np.array(io.imread(image_path))

    image_array = image_array / len(image_list)
    # convert to integer 32 bit array
    image_array = image_array.astype('int32')
    plt.imshow(image_array, cmap='gray', vmin = 0, vmax = v_max)
    
    # check if the output directory exists and if not create it
    CHECK_FOLDER = os.path.isdir(f"{output_filepath}")

    if not CHECK_FOLDER:
        os.makedirs(f"{output_filepath}")
        print(f"Created folder : '{output_filepath}'.")

    else:
        print(f"'{output_filepath}' folder already exists.")

    # save the image
    io.imsave(f"{output_filepath}{experiment_number}_summed1.tiff", image_array)
    
    print(f"Written .tiff image to: '{output_filepath}'.")
    
def multiple_avg_tiff_images(experiment_numbers: List[int], input_path: str, output_path: str, v_max: int):
    '''Create input and output file paths for a list of experiments. 
    Sum up the intensities of all the tiff images contained in the input folders
    and save single average tiff images to the output folder.
    
    :param experiment_number: input experiment numbers.
    :param input_filepath: input path to the series of tiff images.
    :param output_filepath: output path to save the single summed/averaged tiff image.
    :param v_max: intensity maxima for plotting the summed/averaged diffraction pattern image.
    '''
    for experiment_number in experiment_numbers:
        
        experiment_number = str(experiment_number)
        input_filepath = input_path.format(experiment_number = experiment_number)
        output_filepath = output_path.format(experiment_number = experiment_number) 
        avg_tiff_images(experiment_number, input_filepath, output_filepath, v_max)
               
def subtract_tiff_images(experiment_number: str, background_scatter_filepath: str, background_scatter_multiple: int, input_filepath: str, output_filepath: str, v_max: int):
    '''Subtract a tiff image (such as an background scattering image) 
    from each of the tiff images contained in the input folder
    and save the subtracted tiff images to the output folder.
    
    :param experiment_number: input experiment number.
    :param background_scatter_filepath: path of the tiff image to subtract (such as an background scattering image).
    :param background_scatter_multiple: value to multiply the background scatter intensity, to match the acquisition frequency of the data.
    :param input_filepath: input path to the series of tiff images.
    :param output_filepath: output path to save the series of subtracted tiff images.
    :param v_max: intensity maxima for plotting the subtracted diffraction pattern image.
    '''
    image_list = sorted(pathlib.Path(input_filepath).glob("0*.tif"))
    number_of_images = len(image_list)
    
    # set the image arrays to zero to prevent unusual memory allocation
    image_example = io.imread(image_list[0])
    image_array = np.zeros(shape=np.shape(image_example), dtype='int32')
    background_scatter_image_array = np.zeros(shape=np.shape(image_example), dtype='int32')
    subtract_image_array = np.zeros(shape=np.shape(image_example), dtype='int32')
    new_image_array = np.zeros(shape=np.shape(image_example), dtype='int32')
    
    background_scatter_image_array = np.array(io.imread(background_scatter_filepath))
    subtract_image_array = background_scatter_multiple * background_scatter_image_array

    for image_path in tqdm(image_list):
        
        image_array = np.array(io.imread(image_path))
        new_image_array = image_array - subtract_image_array

        # convert to integer 32 bit array
        new_image_array = new_image_array.astype('int32')
    
        # check if the output directory exists and if not create it
        CHECK_FOLDER = os.path.isdir(f"{output_filepath}")

        if not CHECK_FOLDER:
            os.makedirs(f"{output_filepath}")
            print(f"Created folder : '{output_filepath}'.")

        # save the image
        output_stem = pathlib.Path(image_path).stem
        io.imsave(f"{output_filepath}{experiment_number}_subtracted_{output_stem}.tif", new_image_array)

    print(f"Written {number_of_images} tiff images to: '{output_filepath}'.", sep = '\n', end = '\n\n')
    print(f"The BACKGROUND SCATTER image, along with the BEFORE / AFTER subtraction images for the final image in the series, are shown below...", sep = '\n', end = '\n\n')

    plt.subplot(1, 3, 1)
    plt.imshow(subtract_image_array, cmap='gray', vmin = 0, vmax = v_max)
    plt.subplot(1, 3, 2)
    plt.imshow(image_array, cmap='gray', vmin = 0, vmax = v_max)
    plt.subplot(1, 3, 3)
    plt.imshow(new_image_array, cmap='gray', vmin = 0, vmax = v_max)
    plt.show()
    
def multiple_subtract_tiff_images(experiment_numbers: List[int], background_scatter_filepath: str, background_scatter_multiple: int, input_path: str, output_path: str, v_max: int):
    '''Create input and output file paths for a list of experiments. 
    Subtract a tiff image (such as an background scattering image) 
    from each of the tiff images contained in the input folder
    and save the subtracted tiff images to the output folder.
    
    :param experiment_number: input experiment number.
    :param background_scatter_filepath: path of the tiff image to subtract (such as an background scattering image).
    :param background_scatter_multiple: value to multiply the background scatter intensity, to match the acquisition frequency of the data.
    :param input_filepath: input path to the series of tiff images.
    :param output_filepath: output path to save the series of subtracted tiff images.
    :param v_max: intensity maxima for plotting the subtracted diffraction pattern image.
    '''
    for experiment_number in experiment_numbers:
        
        experiment_number = str(experiment_number)
        input_filepath = input_path.format(experiment_number = experiment_number)
        output_filepath = output_path.format(experiment_number = experiment_number)
        
        subtract_tiff_images(experiment_number, background_scatter_filepath, background_scatter_multiple, input_filepath, output_filepath,  v_max)