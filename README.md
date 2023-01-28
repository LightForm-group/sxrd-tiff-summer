sxrd-tiff-summer
-----------

A Python notebook for summing and subtracting synchrotron diffraction pattern images, using the scikit-image package. The notebook can be used to sum together and average the intensity distribution from a series of synchrotron diffraction pattern images, to produce a single diffraction pattern image as a measurement of bulk crystallographic properties. Also includes a notebook for mapping a grid matrix of average and maximum intensity values recorded from individual diffraction pattern images.

The package works with diffraction pattern image data in the form of .tif or .tiff images. If the data is in the form of .cbf images then the images can be converted to tiff format using a notebook from the [pyFAI-integration-caking](https://github.com/LightForm-group/pyFAI-integration-caking) Python package.

Development
--------------

This package was developed by Christopher S. Daniel at The 
University of Manchester, UK, and was funded by the Engineering and Physical Sciences Research Council (EPSRC) via the LightForm programme grant (EP/R001715/1). LightForm is a 5 year multidisciplinary project, led by The Manchester University with partners at University of Cambridge and Imperial College, London (https://lightform.org.uk/).

Contents
-----------

**It is recommended the user works through the examples in the notebooks in the following order:**
    
1. `sxrd_tiff_summer.ipynb` A notebook for summing and subtracting synchrotron diffraction pattern images.

2. `sxrd_tiff_mapper.ipynb` A notebook for mapping a grid matrix of average and maximum intensity values recorded from individual diffraction pattern images.

*Note, the `example-data/` and `example-results/` folders contain data that can be used as an example analysis, but a clear external file structure should be setup to support the analysis of large synchrotron datasets.*

Installation and Virtual Environment Setup
-----------

Follow along by copying / pasting the commands below into your terminal (for a guide on using a python virtual environments follow steps 4-7).

**1. First, you'll need to download the repository to your PC. Open a unix command line on your PC and navigate to your Desktop (or GitHub repository):**
```unix
cd ~/Desktop
```
**2. In your teminal, use the following command to clone this repository to your Desktop:**
```unix
git clone https://github.com/LightForm-group/sxrd-tiff-summer.git
```
**3. Navigate inside `Desktop/sxrd-tiff-summer/` and list the contents using `ls`(macOS) or `dir`(windows):**
```unix
cd ~/Desktop/sxrd-tiff-summer/
```
**4. Next, create a python virtual environment (venv) which contains all of the python libraries required to use sxrd-tiff-summer.
Firstly, use the following command to create the venv directory which will contain the necessary libraries:**
```unix
python -m venv ~/Desktop/sxrd-tiff-summer/venv
```
**5. Your `sxrd-tiff-summer/` directory should now contain `venv/`. Install the relevant libraries to this venv by first activating the venv:**
```unix
source ~/Desktop/sxrd-tiff-summer/venv/bin/activate
```
*Note, the beginning of your command line should change from `(base)` to include `(venv)`.*

**6. Install the python libraries to this virtual environment using pip and the `requirements.txt` file included within the repository:**
```unix
pip install -r ~/Desktop/sxrd-tiff-summer/requirements.txt
```
**7. To ensure these installed correctly, use the command `pip list` and ensure the following packages are installed:**
```unix
pip list
# Check to ensure that all of the following are listed:
#numpy
#matplotlib
#scikit-image
#pathlib
#tqdm
#jupyter
#pyyaml
```
**8. If all in step 7 are present, you can now run the example notebooks.
Ensure the venv is active and use the following command to boot jupyter notebook (using all libraries installed in the venv).
Warning - using just `jupyter notebook` without `python -m` can result in using your default python environment (the libraries may not be recognised):**
```unix
python -m jupyter notebook
```
**9. Work through the notebooks and setup yaml text files for reproducible summing of diffraction pattern images across large synchrotron datasets.**

**10. When you're finished using the virtual environment, deactivate it!
This will avoid confusion when using different python libraries that are not installed within the virtual environment:**
```unix
deactivate
```

Required Libraries
--------------------

The required libraries are listed in requirements.txt