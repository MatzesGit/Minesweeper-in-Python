import os, sys # init lib - used to call all other - don't change
# #################################################################
# Minesweeper Game - v0.11 - python 3.9.5
#
# 2021 by Mathias Stritzke
# #################################################################

# #################################################################
# import lib's from plugins\import.py - imports all plugins
# #################################################################
absFilePath = os.path.abspath(__file__)
path, filename = os.path.split(absFilePath)
lib_file = (path + "\plugins")
sys.path.append(lib_file)
from plugin import *

# #################################################################
# import base classes from data\base.py - application
# #################################################################
absFilePath = os.path.abspath(__file__)
path, filename = os.path.split(absFilePath)

base_file = (path + "\data")
sys.path.append(base_file)
from application import *

# #################################################################
# define image folder
# #################################################################
absFilePath = os.path.abspath(__file__)
path, filename = os.path.split(absFilePath)

image_folder = (path + "\images")

# #################################################################
# program call
# #################################################################
try:
    # set game parameter
    mines_no = 30
    grid_size_x = 30 # colums
    grid_size_y = 20 # rows

    Application_Show.parameter(mines_no, grid_size_x, grid_size_y, image_folder)
    Application_Show()
except Exception as ex:
    print(str(ex))