#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:49:20 2019

@author: dlekkas
"""
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from glob import glob

print '\n', ' P R O G R A M  I N I T I A L I Z E D . . .', '\n'*2

print '+----------------------------- mLICHI v1.0 --------------------------------+' 
print '|                                                                          |'
print '|          MEAN LINEAR INTERCEPT CALCULATOR FOR HISTOLOGICAL IMAGES        |' 
print '|                                                                          |'
print '|             [ Conceived and Coded by Damien Lekkas (c) 2019 ]            |'
print '|                                                                          |'
print '+--------------------------------------------------------------------------+', '\n'

if not os.path.exists('./input_images/'):
    os.makedir('./input_images/')
    print '> CREATED NEW SUBDIRECTORY FOR INPUT IMAGES IN YOUR CURRENT WORKING DIRECTORY.'
    print '> ADD IMAGES TO PROCESS IN THE ./input_images DIRECTORY AND RESTART PROGRAM.'
    print '\n'*2
    print 'P R O G R A M  T E R M I N A T E D', '\n'
    exit()

if not os.path.exists('./output_images/'):
    os.makedir('./output_images/')        

read_dir = './input_images/*'
input_files = []

for f in glob(read_dir):
    input_files.append(f)

process_flag = 'y'
while process_flag == 'y':
    MLI_data_out = open('MLI_data_out.txt', 'a+')
    
    print '+------------------- AVAILABLE FILES ------------------+'
    for f in range(len(input_files)):
        print '|' + str(f+1) + ': ' + input_files[f].split('/')[-1].ljust(51) + '|'
    print '+------------------------------------------------------+', '\n'

    if len(input_files) == 0:
        print '> NO INPUT FILES AVAILABLE IN INPUT_IMAGES DIRECTORY! '
        print '> RESTART PROGRAM WITH FILES PLACED IN APPROPRIATE DIRECTORY.'
        print '\n'*2
        print 'P R O G R A M  T E R M I N A T E D', '\n'

    file_select = -1
    while file_select not in range(len(input_files)+1) or file_select == 0:
        file_select = raw_input('> SPECIFY NUMBER OF FILE TO ANALYZE: ')
        file_select = int(file_select)
        if file_select not in range(len(input_files)+1) or file_select == 0:
            print '\t' + '> IMPROPER FILE SELECTION. RE-SELECT FILE WITH APPROPRIATE NUMBER. ', '\n'
    
    input_file = input_files[file_select-1]

    plt.ion()
    img = mpimg.imread(input_file)
    imgplot = plt.imshow(img)
    plt.show(block=False)
    num_rows = len(img)
    num_cols = len(img[0])

    print '\n'
    print '> SET SCALE FOR DISTANCE CALIBRATION: '

    calibration_flag = 'n'

    while calibration_flag == 'n':
        microns = raw_input('\t' + '> INDICATE SCALE BAR LENGTH IN MICRONS: ')
        pixel_length = raw_input('\t' + '> INDICATE NUMBER OF PIXELS THAT SPAN THE LENGTH SPECIFIED: ')
        calibration_flag = raw_input('\t' + '> PROCEED WITH ' + pixel_length + ' PIXELS EQUIVALENT TO ' + microns + ' MICRONS (y/n)? ')

    microns = float(microns)
    pixel_length = float(pixel_length)

    print '\n' + '> SPECIFY REGION OF IMAGE FOR ANALYSIS: '

    top_left_coords = ''
    while ',' not in top_left_coords or len(top_left_coords) < 3:
        top_left_coords = raw_input('\t' + '> SPECIFY TOP LEFT COORDINATES AS "COLUMN, ROW": ') 
    
        if ',' not in top_left_coords or len(top_left_coords) < 3:
            print '\t' + '> IMPROPER INPUT FORMAT! RE-ENTER COORDINATES.'

    top_left_coords = [int(top_left_coords.split(',')[0]), int(top_left_coords.split(',')[1])]

    bottom_right_coords = ''
    while ',' not in bottom_right_coords or len(bottom_right_coords) < 3:
        bottom_right_coords = raw_input('\t' + '> SPECIFY BOTTOM RIGHT COORDINATES AS "COLUMN, ROW": ') 
    
        if ',' not in bottom_right_coords or len(bottom_right_coords) < 3:
            print '\t' + '> IMPROPER INPUT FORMAT! RE-ENTER COORDINATES.'

    bottom_right_coords = [int(bottom_right_coords.split(',')[0]), int(bottom_right_coords.split(',')[1])]

    top_right_coords = [bottom_right_coords[0], top_left_coords[1]]

    bottom_left_coords = [top_left_coords[0], bottom_right_coords[1]]

    imgplot = plt.imshow(img)
    plt.plot([top_left_coords[0], top_right_coords[0]], [top_left_coords[1], top_right_coords[1]], 'y-')
    plt.plot([top_left_coords[0], bottom_left_coords[0]], [top_left_coords[1], bottom_left_coords[1]], 'y-')
    plt.plot([bottom_left_coords[0], bottom_right_coords[0]], [bottom_left_coords[1], bottom_right_coords[1]], 'y-')
    plt.plot([top_right_coords[0], bottom_right_coords[0]], [top_right_coords[1], bottom_right_coords[1]], 'y-')
    plt.show(block=False)

    print '\n'
    num_test_lines = input('> INDICATE DESIRED NUMBER OF TEST LINES FOR SELECTED REGION: ')
    print '\n'

    step_size = (bottom_left_coords[1] - top_left_coords[1]) / (num_test_lines+1)
    test_line_y1_coords = [row for row in range(top_left_coords[1] + step_size, bottom_left_coords[1]-step_size+1, step_size)]
    test_line_y2_coords = test_line_y1_coords
    test_line_x1_coord = top_left_coords[0]
    test_line_x2_coord = top_left_coords[0] + ((top_right_coords[0] - top_left_coords[0]) / 3)

    guard_line_y1_coords = test_line_y1_coords
    guard_line_y2_coords = test_line_y2_coords
    guard_line_x1_coord = test_line_x2_coord + 1
    guard_line_x2_coord = top_right_coords[0]

    img = mpimg.imread(input_file)
    imgplot = plt.imshow(img)
    plt.plot([top_left_coords[0], top_right_coords[0]], [top_left_coords[1], top_right_coords[1]], 'y-')
    plt.plot([top_left_coords[0], bottom_left_coords[0]], [top_left_coords[1], bottom_left_coords[1]], 'y-')
    plt.plot([bottom_left_coords[0], bottom_right_coords[0]], [bottom_left_coords[1], bottom_right_coords[1]], 'y-')
    plt.plot([top_right_coords[0], bottom_right_coords[0]], [top_right_coords[1], bottom_right_coords[1]], 'y-')

    for line in range(len(test_line_y1_coords)):
        plt.plot([test_line_x1_coord, test_line_x2_coord], [test_line_y1_coords[line], test_line_y2_coords[line]], 'k-')
        plt.plot([guard_line_x1_coord, guard_line_x2_coord], [guard_line_y1_coords[line], guard_line_y2_coords[line]], linestyle='dashed', color='cyan')


    plt.show(block=False)
    plt.savefig('./output_images/' + input_file.split('/')[-1].split('.')[0] + '_analysis_section.tif', dpi=1000)   


    test_lines_pixel_colors_list = []
    for line in range(len(test_line_y1_coords)):
        test_line_pixels = []
        for col in range(test_line_x1_coord, test_line_x2_coord):
            test_line_pixels.append(img[test_line_y1_coords[line]][col])
    
        pixel_colors = []    
        for pixel in test_line_pixels:
            if pixel[0] > 230 and pixel[1] > 230 and pixel[2] > 230:
                pixel_colors.append('W')
            elif pixel[0] < 230 and pixel[1] < 230 and pixel[2] < 230:
                pixel_colors.append('R')
            else:
                pixel_colors.append('?') 
    
        for color in range(len(pixel_colors)):
            if pixel_colors[color] == '?':
                pixel_colors[color] = pixel_colors[color-1]
    
        test_lines_pixel_colors_list.append(pixel_colors)

    region_check = 0
    for pixel in test_lines_pixel_colors_list[0]:
        if pixel == 'R':
            region_check += 1

    if region_check == 0:
        print '> INVALID/UNINFORMATIVE REGION. ANALYSIS CANNOT PROCEED.'
        raw_input('> PRESS ANY KEY TO EXIT.' )
        exit()
    
    guard_lines_pixel_colors_list = []
    for line in range(len(guard_line_y1_coords)):
        guard_line_pixels = []
        for col in range(guard_line_x1_coord, guard_line_x2_coord):
            guard_line_pixels.append(img[guard_line_y1_coords[line]][col])
    
        pixel_colors = []    
        for pixel in guard_line_pixels:
            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
                pixel_colors.append('W')
            elif pixel[0] < 200 and pixel[1] < 200 and pixel[2] < 200:
                pixel_colors.append('R')
            else:
                pixel_colors.append('?') 
    
        for color in range(len(pixel_colors)):
            if pixel_colors[color] == '?':
                pixel_colors[color] = pixel_colors[color-1]
    
        guard_lines_pixel_colors_list.append(pixel_colors)
    
    distances = []
    line_start_pixels_x = []
    white_space_start_pixels_x = []

    white_space_count = 0
    line_count = 0
#COUNT WHITE SPACE BETWEEN RED ALVEOLAR WALLS FOR EACH TEST LINE
    for line in test_lines_pixel_colors_list: 
        white_spaces = []
        subline_start_pixels = []
        pixel_start = line.index('R')
        line_start_pixels_x.append(test_line_x1_coord + pixel_start)
        for color in range(pixel_start+1,len(line)):
            if line[color] == 'W' and line[color-1] == 'R':
                subline_start_pixels.append(color + test_line_x1_coord)
                white_spaces.append(1)
                white_space_count += 1
            elif line[color] == 'W' and line[color-1] == 'W':
                white_spaces[-1] += 1

#IF GUARD LINE ENDS IN AN ALVEOLAR SPACE, COUNT ADDITIONAL WHITESPACE PRESENT AT START OF GUARD LINE UNTIL HITTING A RED ALVEOLAR WALL
            if color == len(line) - 1 and line[color] == 'W':
            
                for color2 in range(len(guard_lines_pixel_colors_list[line_count])):
                
                    if guard_lines_pixel_colors_list[line_count][color2] == 'W':
                        white_spaces[-1] += 1
                    
                    elif guard_lines_pixel_colors_list[line_count][color2] == 'R':
                        break
    
        white_space_start_pixels_x.append(subline_start_pixels)          
        distances.append(white_spaces) 
        line_count += 1

    white_space_end_pixels_x = []
    white_space_start_pixels_y = []
    white_space_end_pixels_y = []  
     
    for line in range(len(white_space_start_pixels_x)):
        subline_end_pixels_x = []
        subline_end_pixels_y = []
    
        for start_pixel in range(len(white_space_start_pixels_x[line])):
            subline_end_pixels_x.append(white_space_start_pixels_x[line][start_pixel] + distances[line][start_pixel])            
            subline_end_pixels_y.append(test_line_y2_coords[line])
    
        white_space_end_pixels_x.append(subline_end_pixels_x)
        white_space_end_pixels_y.append(subline_end_pixels_y)
    
    white_space_start_pixels_y = white_space_end_pixels_y

    continue_flag = '?'

    while continue_flag != 'y' and continue_flag != 'n':
        continue_flag = raw_input('> PROCEED WITH ANALYSIS OF THIS REGION (y/n)? ' )    

        if continue_flag == 'n':
            print '\t' + '> PROGRAM WILL NOW EXIT. PLEASE RESTART PROGRAM TO RE-ANALYZE IMAGE.', '\n'*2
            print 'P R O G R A M  T E R M I N A T E D'
            exit()

    print '\n'        
    raw_input('> PRESS ENTER TO REVIEW AND FILTER PUTATIVE ALVEOLAR SPACES: ')

    filtered_alveolar_space_distances = []


    img = mpimg.imread(input_file)
    imgplot = plt.imshow(img)
    plt.plot([top_left_coords[0], top_right_coords[0]], [top_left_coords[1], top_right_coords[1]], 'm-')
    plt.plot([top_left_coords[0], bottom_left_coords[0]], [top_left_coords[1], bottom_left_coords[1]], 'm-')
    plt.plot([bottom_left_coords[0], bottom_right_coords[0]], [bottom_left_coords[1], bottom_right_coords[1]], 'm-')
    plt.plot([top_right_coords[0], bottom_right_coords[0]], [top_right_coords[1], bottom_right_coords[1]], 'm-')

    for ln in range(len(test_line_y1_coords)):
        plt.plot([test_line_x1_coord, test_line_x2_coord], [test_line_y1_coords[line], test_line_y2_coords[line]], 'k-')
        plt.plot([guard_line_x1_coord, guard_line_x2_coord], [guard_line_y1_coords[line], guard_line_y2_coords[line]], linestyle='dashed', color='cyan')


    for line in range(len(distances)):
        for space in range(len(distances[line])):
            plt.plot([white_space_start_pixels_x[line][space], white_space_end_pixels_x[line][space]], [white_space_start_pixels_y[line][space], white_space_end_pixels_y[line][space]], 'y-')
 
            decision = ''
            while decision != 'y' and decision != 'n':
                decision = raw_input('\t' + '> RETAIN HIGHLIGHTED SPACE FOR MLI CALCULATION (y/n)? ')
                if decision != 'y' and decision != 'n':
                    print '\t' + '> PLEASE ENTER A VALID RESPONSE (y/n).'
        
            if decision == 'y':
                filtered_alveolar_space_distances.append(distances[line][space])
                plt.plot([white_space_start_pixels_x[line][space], white_space_end_pixels_x[line][space]], [white_space_start_pixels_y[line][space], white_space_end_pixels_y[line][space]], 'g-')
            elif decision == 'n':
                plt.plot([white_space_start_pixels_x[line][space], white_space_end_pixels_x[line][space]], [white_space_start_pixels_y[line][space], white_space_end_pixels_y[line][space]], 'r-')    
   
    plt.savefig('./output_images/' + input_file.split('/')[-1].split('.')[0] + '_filtered_analysis.tif', dpi=1000)        

    print '\n', ' > THE TOTAL NUMBER OF ACCEPTED SPACES =', len(filtered_alveolar_space_distances)

    set_accepted_spaces = ''
    while set_accepted_spaces != 'y' and set_accepted_spaces != 'n':
        set_accepted_spaces = raw_input(' > PROCEED WITH MLI CALCULATION USING THIS NUMBER OF SPACES (y/n)? ')
        if set_accepted_spaces != 'y' and set_accepted_spaces != 'n':
            print '\t' + '> PLEASE ENTER A VALID RESPONSE (y/n).'
        
        if set_accepted_spaces == 'y':
            final_space_count = len(filtered_alveolar_space_distances)
        else:
            final_space_count = int(raw_input('\t' + ' > SPECIFY DESIRED NUMBER OF SPACES TO CONSIDER FOR MLI CALCULATION: '))            

    print '\n'
    print '+------------------------------ FINAL RESULTS -----------------------------+'
    print '|                                                                          |'
    print '| ' + 'TOTAL NUMBER OF CALCULATED SPACES: '.ljust(45) + (str(white_space_count).rjust(9)) + '                   |'
    print '| ' + 'TOTAL NUMBER OF ACCEPTED SPACES: '.ljust(45) + (str(len(filtered_alveolar_space_distances))).rjust(9) + '                   |'
    print '| ' + 'TOTAL NUMBER OF REJECTED SPACES: '.ljust(45) + (str(white_space_count - len(filtered_alveolar_space_distances))).rjust(9) + '                   |'
    print '|                                                                          |'
    print '| ' + 'TOTAL NUMBER OF SPACES FOR MLI: '.ljust(45) + (str(final_space_count)).rjust(9) + '                   |'  
    print '| ' + 'TOTAL ALVEOLAR DISTANCE: '.ljust(45) + str(round((float(sum(filtered_alveolar_space_distances))/pixel_length)*microns, 2)).rjust(9) + ' uM                |' 
    print '|                                                                          |'
    print '| ' + 'MEAN LINEAR INTERCEPT (MLI): '.ljust(45) + str(round(((float(sum(filtered_alveolar_space_distances))/final_space_count)/pixel_length)*microns, 2)).rjust(9) + ' uM                |'
    print '|                                                                          |'
    print '+--------------------------------------------------------------------------+', '\n'
    
    raw_input(' > IMAGE ANALYSIS COMPLETE! PRESS ENTER TO WRITE RESULTS TO STANDARD OUT. ')
    print '\n'
    
    MLI_data_out.write(str(input_file.split('/')[-1]).ljust(30) + '\t' + str(round(((float(sum(filtered_alveolar_space_distances))/final_space_count)/pixel_length)*microns, 2)) + ' uM' + '\n')
    
    
    process_flag = raw_input(' > ANALYZE ANOTHER IMAGE IN THE IMAGE INPUT DIRECTORY (y/n)? ')
    while process_flag != 'y' and process_flag != 'n':
        process_flag = raw_input('\t' + '> PLEASE ENTER A VALID RESPONSE (y/n). ')

    MLI_data_out.close()
    plt.close()    

print '\n'*2, 'P R O G R A M  T E R M I N A T E D', '\n'  