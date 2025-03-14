## Overview

**Project Title**:
    Geiger Counter Altitude Data Analysis

**Project Description**:
    For a given set of Geiger Counter data and altitude data in the form of specific csv files, 
    reads, parses, and matches up given the times between the sets of data and plots the counts per minute
    (CPM) and the altitude, then plot the results.

**Project Goals**:
    Read the two input csv files correctly and match up the times, join the two sets, and plot them on
    a 2D graph.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Make sure GPSLOG00.TXT and geiger_altitude_data.csv are in the same folder as 
   GeigerData.py
2. (Optional) If you want to rename the output txt file (or disable it completely), manually
   change it in main under the save_data()/ comment it out.
3. Run file with python GeigerData.py

Instructions for using the software:

1. Simply run the python file to get console readings of the important values and display a 
    graph of the Altitude vs CPM.

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3 or Greater
* Libraries
*   - Pyplot from Matplotlib (current)
*   - csv (current)
*   - Pandas (current)

## Useful Websites to Learn More

I found these websites useful in developing this software:

* https://chatgpt.com/
* https://pandas.pydata.org/docs/user_guide/index.html

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Potentially Implement Classes
* [ ] Make the input able to be more general
* [ ] Compact code, if possible
* [ ] Implement better DEBUG functionality
* [ ] Abstract the code
#   G e i g e r _ C o u n t e r _ A l t i t u d e _ D a t a _ A n a l y s i s 
 
 