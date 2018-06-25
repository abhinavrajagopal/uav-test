### Basic UAV path analyser

##### Simple script to obtain metadata of UAV path from a video footage and store the data in a file. Additional feature includes generating a kml of the drone path.

Dependencies to be installed : 

  * pysrt - Python library to edit and create SubRip files.
  * simplekml -  Python package to generate KML with as little effort as possible.
  * piexif - Python package to simplify exif manipulations.
  * geopy - Geocoding library for Python.
                             
                              
These can be installed with the package manager pip.

This application reads a SRT file wihch contains the GPS coordinates at the timestamps where the UAV was present over the area.
It creates a map of images in a directory which are linked to their specific coordinates from the footage.
Then, a CSV is created which contains the list of image file names that are calculated within the radius of the drone path from the video.
A kml is also created of the drone path throughout the video.

Additionally it reads a CSV file with points of interest and coordinates and creates another CSV that generates image file names within a specific point of interest of radius.

Parameters taken by the application : 

- vid_radius : This obtains data of the drone path from the video within a given radius.

- poi_radius : This obtains the data for the other csv file which calculates the specific coordinates within a given radius.

Usage : `python app.py 100 300`


