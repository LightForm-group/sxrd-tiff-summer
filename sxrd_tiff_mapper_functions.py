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

import sxrd_tiff_summer_functions as analysis

def extract_grid_input(config_path: str):
    """Extract additional user inputs from yaml configuration file. 
    Extract overall grid shape, as well as sample numbers and 
    starting and ending grid points for samples contained within 
    the diffraction pattern measurement grid.
    
    :param config_path: path to the configuration file.
    
    :return: grid shape as integers and sample numbers, 
    start points and end points as lists of integers and tuples.
    """
    config = analysis.get_config(config_path)
    shape_x = config["grid_info"]["shape_x"]
    shape_y = config["grid_info"]["shape_y"]
    print("The shape of the diffraction pattern measurement grid in X and Y is :", shape_x, shape_y, sep = '\n', end = '\n\n')
    
    sample_numbers = config["grid_info"]["sample_numbers"]
    print("The list of reference numbers for the samples contained within the measurement grid is: ", sample_numbers, sep = '\n', end = '\n\n')
    
    start_points = config["grid_info"]["start_points"]
    print("The list of starting measurement points (X,Y) for each of the numbered samples is: ", start_points, sep = '\n', end = '\n\n')
    
    end_points = config["grid_info"]["end_points"]
    print("The list of ending measurement points (X,Y) for each of the numbered samples is: ", end_points, sep = '\n', end = '\n\n')
    
    return shape_x, shape_y, sample_numbers, start_points, end_points
    
def grid_tiff_intensity(experiment_number: str, input_filepath: str, output_filepath: str, 
                        shape_x: int, shape_y: int, c_map: str = "Reds"):
    '''Calculate the maximum and average intensity from a series of diffraction
    pattern images and plot the values as a grid of spatial (X,Y) measurement points.
    
    :param experiment_number: input experiment number.
    :param input_filepath: input path to the series of tiff images.
    :param output_filepath: output path to save the intensity map.
    :param shape_x: number of diffraction measurement points along X.
    :param shape_y: number of diffraction measurement points along Y.
    :param c_map: colour scale for the intensity map.
    '''
    
    # define the plot parameters
    plt.rc('xtick', labelsize = 24)
    plt.rc('ytick', labelsize = 24)
    plt.rc('legend', fontsize = 20)
    plt.rc('axes', linewidth = 2)
    plt.rc('xtick.major', width = 2, size = 10)
    plt.rc('xtick.minor', width = 2, size = 5)
    plt.rc('ytick.major', width = 2, size = 10)
    plt.rc('ytick.minor', width = 2, size = 5)
    
    max_list = []
    avg_list = []
    
    # check if the output directory exists and if not create it
    CHECK_FOLDER = os.path.isdir(f"{output_filepath}")

    if not CHECK_FOLDER:
        os.makedirs(f"{output_filepath}")
        print(f"Created folder : '{output_filepath}'.")

    else:
        print(f"'{output_filepath}' folder already exists.")
    
    # load the diffraction pattern images and calculate the maximum and average intensity for each
    image_list = sorted(pathlib.Path(input_filepath).glob("0*.tif*"))
    
    for image_path in tqdm(image_list):
        image_array = io.imread(image_path)
        max_image = np.max(image_array)
        avg_image = np.average(image_array)
        
        max_list.append(max_image)
        avg_list.append(avg_image)
        
    # set max and min intensities for the maximum intensity map    
    v_min = min(max_list)
    v_max = max(max_list)
    
    # plot and save the maximum intensity map
    fig, ax = plt.subplots(figsize=(20, 10))
    max_array = np.array(max_list)
    shape = (shape_y, shape_x)
    image = ax.imshow(max_array.reshape(shape), interpolation='nearest', cmap = c_map, vmin = v_min, vmax = v_max, extent=[0,shape_x,shape_y,0])
    ax.minorticks_on()
    ax.set_xlabel("X", fontsize = 25)
    ax.set_ylabel("Y", fontsize = 25, rotation = 0, labelpad=50)
    ax.set_title("Maximum Intensity Map \n", fontsize = 25)
    plt.colorbar(image, ax=ax, location = 'bottom', shrink = 0.4)
    fig.tight_layout()
    fig.savefig(f"{output_filepath}{experiment_number}_MAX_intensity_map.png")
    
    print(f"Figure saved to: {output_filepath}{experiment_number}_MAX_intensity_map.png")

    # set max and min intensities for the average intensity map 
    v_min_avg = min(avg_list)
    v_max_avg = max(avg_list)
    
    # plot and save the average intensity map
    fig, ax = plt.subplots(figsize=(20, 10))
    avg_array = np.array(avg_list)
    shape = (shape_y, shape_x)
    image = ax.imshow(avg_array.reshape(shape), interpolation='nearest', cmap = c_map, vmin = v_min_avg, vmax = v_max_avg, extent=[0,shape_x,shape_y,0])
    ax.minorticks_on()
    ax.set_xlabel("X", fontsize = 25)
    ax.set_ylabel("Y", fontsize = 25, rotation = 0, labelpad=50)
    ax.set_title("Average Intensity Map \n", fontsize = 25)
    plt.colorbar(image, ax=ax, location = 'bottom', shrink = 0.4)
    fig.tight_layout()
    fig.savefig(f"{output_filepath}{experiment_number}_AVG_intensity_map.png")
    
    print(f"Figure saved to: {output_filepath}{experiment_number}_AVG_intensity_map.png")
    
    # calculate average intensity of all diffraction pattern images
    avg_mean = np.mean(avg_list)
    print(f"The average intensity of all diffraction pattern images in the series is: {avg_mean}")
    
def plot_grid_points(experiment_number: str, output_filepath: str,
                     start_points: list, end_points: list, 
                     shape_x: int, shape_y:int):
    '''Plot the chosen start and end points, for defining spatial 
    (X,Y) measurement points of different samples. 
    Save the plot to the output folder.
    
    :param experiment_number: input experiment number.
    :param output_filepath: output path to save plot.
    :param start_points: list of starting measurement points (X,Y) for each of the numbered samples.
    :param end_points: list of ending measurement points (X,Y) for each of the numbered samples.
    :param shape_x: length of the diffraction pattern measurement grid along X
    :param shape_y: length of the diffraction pattern measurement grid along Y
    '''
    
    # define the plot parameters
    plt.rc('xtick', labelsize = 24)
    plt.rc('ytick', labelsize = 24)
    plt.rc('legend', fontsize = 20)
    plt.rc('axes', linewidth = 2)
    plt.rc('xtick.major', width = 2, size = 10)
    plt.rc('xtick.minor', width = 2, size = 5)
    plt.rc('ytick.major', width = 2, size = 10)
    plt.rc('ytick.minor', width = 2, size = 5)

    x_points = []
    y_points = []

    # get x and y points
    for start_point, end_point in zip(start_points, end_points):
        x_points.append(start_point[0])
        x_points.append(end_point[0])
        y_points.append(start_point[1])
        y_points.append(end_point[1])

    # plot the x and y points    
    fig, ax = plt.subplots(1, 1, figsize = (12, 10))

    ax.minorticks_on()
    ax.plot(x_points, y_points, color = "red", linewidth = 0, marker = "x", markersize = 20)
    ax.set_xlabel("X", fontsize = 25)
    ax.set_ylabel("Y", fontsize = 25, rotation = 0, labelpad=50)
    ax.set_xlim(0,shape_x)
    ax.set_ylim(0,shape_y)
    ax.invert_yaxis()

    fig.tight_layout()

    # save the figure
    fig.savefig(f"{output_filepath}{experiment_number}_start-end_points_map.png")
    print(f"Figure saved to: {output_filepath}{experiment_number}_AVG_intensity_map.png")
    
def avg_tiff_images_grid(experiment_number: str, input_filepath: str, output_filepath: str, v_max: int,
                        sample_numbers: list, start_points: list, end_points: list, 
                        shape_x: int):
    '''Use a list of start and end points, defining the spatial (X,Y) 
    measurement points, to select different samples. Using these points, sum up 
    the intensities of different series of tiff images, for different samples, 
    from an input folder. Save a single average tiff image, for each sample, 
    to the output folders.
    
    :param experiment_number: input experiment number.
    :param input_filepath: input path to the entire series of tiff images.
    :param output_filepath: output path to save single summed/averaged tiff images for each sample.
    :param v_max: intensity maxima for plotting the summed/averaged diffraction pattern image.
    :param sample_numbers: list of reference numbers for samples contained within the measurement grid.
    :param start_points: list of starting measurement points (X,Y) for each of the numbered samples.
    :param end_points: list of ending measurement points (X,Y) for each of the numbered samples.
    :param shape_x: length of the diffraction pattern measurement grid along X 
    '''
    
    image_list = sorted(pathlib.Path(input_filepath).glob("0*.tif*"))

    # segment each sample in turn
    for sample_number, start_point, end_point in tqdm(zip(sample_numbers, start_points, end_points), 
                                                      total=len(sample_numbers)):

        # set the image arrays to zero to prevent unusual memory allocation
        image_example = io.imread(image_list[1])
        image_array = np.zeros(shape=np.shape(image_example), dtype='int32')
        sample_image_list = []

        for start_y in range(start_point[1],end_point[1]+1):
            for start_x in range(start_point[0],end_point[0]+1):
                # as tiffs are numbered sequentially along horizontal, calculate tiff number for each position
                width = shape_x
                tiff_number = (start_x+1)+(start_y*width)
                tiff_string = f"{tiff_number:05}"
                
                # find tiff number in path list and add it to the image array
                for image_path in image_list:
                     if str(image_path).find(tiff_string) != -1:
                            sample_image_list.append(image_path)
                            image_array = image_array + np.array(io.imread(image_path))
        
        # normalise the image array intensity
        image_array = image_array / len(sample_image_list)
        # convert to integer 32 bit array
        image_array = image_array.astype('int32')
        plt.imshow(image_array, cmap='gray', vmin = 0, vmax = v_max)

        # check if the output directory exists and if not create it
        output_filepath_sample = f"{output_filepath}sample_{sample_number}/"
        CHECK_FOLDER = os.path.isdir(output_filepath_sample)

        if not CHECK_FOLDER:
            os.makedirs(output_filepath_sample)
            print(f"Created folder : '{output_filepath_sample}'.")

        else:
            print(f"'{output_filepath_sample}' folder already exists.")

        # save the image
        io.imsave(f"{output_filepath_sample}{experiment_number}_summed1.tiff", image_array)

        print(f"Written .tiff image to: '{output_filepath_sample}'.")
        
        # write out a text file of contributory images
        output_text = f"{output_filepath_sample}sample_{sample_number}_image_list.txt"
        
        with open(output_text, 'w') as output_file:
            
            # write description header
            output_file.write(f"The summed tiff image for sample {sample_number} was created from the average intensity of the following diffraction pattern images... \n")

            # write image paths
            for i in range(0, len(sample_image_list)):
                output_file.write(f"{sample_image_list[i]}\n")

        print(f"Written .txt file to: '{output_text}'.")