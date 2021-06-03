import os, sys # init lib - used to call all other - don't change
# #################################################################
# Minesweeper Game - v1.0 - python 3.9.5
#
# 2021 by Mathias Stritzke
# #################################################################

# get current directory
absFilePath = os.path.abspath(__file__)
path, filename = os.path.split(absFilePath) 

# import lib's from plugins\import.py - imports all plugins
lib_file = (path + "\plugins")
sys.path.append(lib_file)
from plugin import *

# import base classes from data\base.py - application
base_file = (path + "\data")
sys.path.append(base_file)
from application import *

# define path for image folder
image_folder = (path + "\images")

# define config folder and file
config_file = (path + "\cfg\cfg.ini")

# #################################################################
# program
# #################################################################
config_game_modi = ConfigParser()

# standard modi
config_game_modi["level1"] = {
    "no_of_colums": "15", 
    "no_of_rows": "10", 
    "no_of_bombs": "15"
}

config_game_modi["level2"] = {
    "no_of_colums": "20", 
    "no_of_rows": "15", 
    "no_of_bombs": "25"
}

config_game_modi["level3"] = {
    "no_of_colums": "30", 
    "no_of_rows": "20", 
    "no_of_bombs": "50"
}

config_game_modi["start_level"] = {
    "Level" : 1
}

try:
    # check for ini file is exist if not create on and write config_game_modi levels
    if os.path.isfile (config_file):
        # read from file 
        config_game_modi.read(config_file)
    else:
        with open(config_file, "a") as conf:
            config_game_modi.write(conf)
            conf.close()
        # read from file
        config_game_modi.read(config_file)

    # set game parameter
    start_level = config_game_modi["start_level"]
    if start_level["level"] == "Level1":
        level = 1
        config_game_parameter = config_game_modi["level1"]
    elif start_level["level"] == "Level2":
        level = 2
        config_game_parameter = config_game_modi["level2"]
    else:
        level = 3 
        config_game_parameter = config_game_modi["level3"]
        
    mines_no = int(config_game_parameter["no_of_bombs"])
    grid_size_x = int(config_game_parameter["no_of_colums"])
    # min size
    if grid_size_x < 15:
        grid_size_x = 15
    grid_size_y = int(config_game_parameter["no_of_rows"])

    Application_Show.parameter(mines_no, grid_size_x, grid_size_y, image_folder, config_file, level)
    Application_Show()
except Exception as ex:
    print(str(ex))