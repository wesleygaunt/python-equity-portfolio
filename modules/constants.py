
# -*- coding: utf-8 -*-
"""
Defines constants to be used throughout the project - ie API keys and data folders.
"""
import datetime
from sys import platform

if platform == 'win32':

    #Folders - set these up in advance. 
    DEFAULT_DATA_FOLDER = 'C:\\portfolio\\data'
    DEFAULT_PLOTS_FOLDER = 'C:\\portfolio\\plots'

    GUI_FOLDER = 'C:\\GitHub\\python-equity-portfolio\\GUI'
elif platform.startswith('linux'):
    DEFAULT_DATA_FOLDER = '/home/wes/portfolio/data'
    
    
    
MIN_DATE = datetime.datetime(year = 1970,month = 1,day = 1)