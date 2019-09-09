#!/usr/bin/env python

"""utils.py Utility Files"""

__author__      = "David Li"
__copyright__   = "Copyright 2019"

import re
import yaml
from os import makedirs, listdir
from os.path import isfile, exists
from datetime import date, datetime
# See https://www.python.org/dev/peps/pep-0257/
# https://stackoverflow.com/questions/27593227/listing-png-files-in-folder
def get_pred_imgs(directory='predict'):
    """ get predictions from prophet

    Input --- directory folder to be scanned for images
    Output --- list of relative file paths from root 
    """
    filelist=listdir(directory)
    for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".png")):
            filelist.remove(fichier)
    # print(filelist)
    # properly create list of files
    new_list = []
    for rel_file_path in filelist:
        new_list.append('{}/{}'.format(directory, rel_file_path))
    return new_list

def mkdir_new(folder_name='2019-01-03'):
    """
    Makes a new directory if it doesn't already exist
    """
    if not exists(folder_name):
        makedirs(folder_name)

# perhaps rename to parse_config???
def get_config(default_file = 'config.yml'):
    exists = isfile('../config.yml')
    if exists:
        config_file = '../config.yml'
        # Store configuration file values
    else:
        # Keep presets
        config_file = default_file
    with open(config_file, 'r') as ymlfile:
        # Latest version
        if hasattr(yaml, 'FullLoader'):
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # PyYaml 3.
        else:
            cfg = yaml.load(ymlfile)
    return cfg

# Error handling
# Situation 1: \textcolor{%s ...
# Situation 2: \textcolor{%s}{%s ...
# Dealing with Situation 2 before 1.
def fix_broken_regex(line):
    # Assuming line has unmatched brackets
    # re.sub(r'([a-z]\[\d+)',r'\1]',line)
    #
    fixed_line = re.sub(r'(\{\w+...$)',r'\1}',line)
    return fixed_line

# re.sub(r'([a-z]\[\d+)',r'\1]',mystr)
# Check if brackets are matched
def matched_brackets(str):
    count = 0
    for i in str:
        if i == "{":
            count += 1
        elif i == "}":
            count -= 1
        if count < 0:
            return False
    return count == 0

def unix2_ISO8601(x): 
    try:
        return datetime.utcfromtimestamp(int(x)).strftime('%Y-%m-%d')
    except Exception as e:
        # new_time = time.ctime(int(x)).strftime('%Y-%m-%d')
        # print(time)
        # This needs to be point on graph, 1950-01-01 is such a plot
        time= "1950-01-01"
        return time

# Calculate values ago year
def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.today().replace(day=1,month=1)
    try:
        curr_date = from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        curr_date = from_date.replace(month=2, day=28,
                                 year=from_date.year-years)
    return curr_date.strftime('%Y-%m-%d')