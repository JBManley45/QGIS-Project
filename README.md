Python / QGIS Project

This is a standalone Python project working with QGIS using Anaconda as the python distribution. 

REQUIREMENTS:
Anaconda: Anaconda is a Python Distribution that includes many packages and tools. Install Anaconda & Anaconda Navigator - uses conda package and environment manager to create conda environments. 

QGIS: (not required for initial setup-this will help us have a UI to work with but to we'll be using the QGIS from Anaconda) QGIS is a free and open source geographic information system software. Install QGIS 3.34 

SETUP:
    Clone this repo

    Naviagte to Project Directory

    Create Environemnt with 'Anaconda Prompt'-Anaconda's CLI downloaded with Anaconda is the only way you can install QGIS. Navigator has some helpful UI but limited functionality. conda-forge is the channel we will download QGIS. pcraster, jupyter, matplotlib are common packages we may or may not use further in the project. Update 

        $ conda install -c conda-forge qgis / $ conda install conda-forge::qgis

    Install additional packages 
        $ conda install -c conda-forge pcraster jupyter matplotlib

    Set Environment Varibales
        Ensure 'PATH' and 'PYTHONPATH' environment variables are configured to include the directories containing QGIS binaries and python packages. This may or may not be required based on how you installed Anaconda. 

USAGE:
    CD into Activate your environemnt before running any scripts
        $conda activate 'name-of-my-environemnt'
    If using Anaconda Navigator select 'Home' and then select your VSCode or your chosen editor to open use your environment

    Test Connectivity
    Test that you can access QGIS modules and functionality within Python scripts. Restart of Anaconda/Vscode may be required after intitial install.

CONCLUSION:
    Anaconda - check your Python tab in your editor and ensure your in the correct environment.
    Git - check your status bar to ensure you are connected to Git 
    Python - run the 'testingbase.py', if no errors occur and you can see the library path displayed in your terminal with no errors then you're good to go. 

Helpful LINKS:
https://anaconda.org/conda-forge/qgis
https://www.anaconda.com/download
https://gisunchained.wordpress.com/2019/05/29/using-qgis-from-conda/
https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/intro.html#pythonapplications


Further developement:
python library to pass the data in and create the files - there might be a library for kmz files. 
find a library that can take in data and convert it to a kmz file if needed. Start looking at pyqgis for headless application. 

Provide to: tom and isaac - example csv file (lat long) and a png - data and output image.

Provide flow chart from csv to program (general/layment) what it does and where it goes and ends w email

1. readme - COMPLETE
2. git - COMPLETE
3. flow chart - IN PROGRESS

# QGIS-Project-Goals

Goal 1: pull in CSV file, create base layers, plob lat/lon, export image. 

Goal 2: pull in csv, apply water in RF freindly lids template, export Vzw only image.

Goal 3: apply water in RF freindly lid for Vzw only, ATT only, Vzw Primary, ATT Primary, and Coverage, export images. 

Goal 4: apply templates, apply base map styles, export images.

Goal 5: export images to csv, word doc, and or email draft

Goal 6: full map creation functionality