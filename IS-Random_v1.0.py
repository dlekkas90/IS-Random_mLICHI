#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 23:32:47 2019

@author: dlekkas
"""

import os
import random
from PIL import Image
import cv2

print '\n', ' P R O G R A M  I N I T I A L I Z E D . . .', '\n'*2

print '+---------------------------- IS-Random v1.0 ------------------------------+' 
print '|                                                                          |'
print '|                        IMAGE SUBSAMPLE RANDOMIZER                        |' 
print '|                                                                          |'
print '|             [ Conceived and Coded by Damien Lekkas (c) 2019 ]            |'
print '|                                                                          |'
print '+--------------------------------------------------------------------------+', '\n'


image_file = raw_input(' > SPECIFY NAME OF IMAGE FILE TO RANDOMLY SAMPLE: ')
subsample_n = input(' > SPECIFY THE NUMBER OF RANDOM SUBSAMPLES TO GENERATE: ')

print ' > . . . GENERATING ', subsample_n, ' SUBSAMPLES OF SIZE 256x256 PIXELS FROM', image_file + '.'

img = Image.open(image_file)

img_width, img_height = img.size

random_regions = []

region_id = 1
while len(random_regions) < subsample_n:
    
    x_start = random.randint(0, img_width-256)
    y_start = random.randint(0, img_height-256)
    
    slice_parameters = (x_start, y_start, x_start+256, y_start+256)
    region_slice = img.crop(slice_parameters)
    region_slice = img.crop(slice_parameters)
    region_slice.save('region_slice_test.tif')
    region_slice_data = cv2.imread('region_slice_test.tif')
    white_space_count = 0
    for y in range(256):
        for x in range(256):
            if region_slice_data[y][x][0] > 240 and region_slice_data[y][x][1] > 240 and region_slice_data[y][x][2] > 240:
                white_space_count += 1
    
    if white_space_count / (256.0*256.0) < 0.5:
        random_regions.append(region_slice)
        region_slice.save('./input_images/' + image_file + '_region_slice_' + str(region_id) + '.tif')
        region_id += 1
    
   
os.remove('region_slice_test.tif')

print '\n', ' > SUBSAMPLES GENERATED AND SAVED TO INPUT_FILES SUBDIRECTORY.'

print '\n'*2, 'P R O G R A M  T E R M I N A T E D', '\n' 
       