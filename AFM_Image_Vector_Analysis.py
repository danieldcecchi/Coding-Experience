#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:34:28 2019

@author: danieldcecchi
"""

import numpy as np
import matplotlib.pyplot as plt

#This code is to analyze how the average direction of collagen changes over time image-to-image.
#Works best with data from FIJI
#The data that I used had x and y column names such as "X" and "Y" which is why the following code
#finds the index of X and Y.  If you want to use other file column names, then you will have 
#to change them. 



file = input('What is the text file you are trying to use?') #Results_A_9_1.txt is the one I used. 

with open(file) as f:
    first_line = f.readline()
split = first_line.split()
x_cols = split.index('X')
y_cols = split.index('Y')

results = np.loadtxt(file, usecols = [x_cols+1,y_cols+1],skiprows = 1)
Results = results.T
x = Results[0] - 295 #these numbers are optional and can be changed.  It is solely to centre the FIJI image around the centre of the AFM image. 
y = Results[1] - 296

#This code runs by taking a vector between 2 consecutive points.  So, when finding a line of
#collagen you want to analyze, it is best to split the collagen into segments of 2 points. 

#Each pair of points is unique.  This means that this code doesn't take point 1, and point 2 
#as a vector, then point 2 and point3 as another vector.  It takes point 1, and point 2 as one vector, then point 3
#and point 4 as another vector. 

def vectors(x_points,y_points,points):
    vec_mags = [] #Array to hold the magnitude of the vectors we are going to find
    dx = [] #change in x value between two consecutive points
    dy = [] #change in y value between two consecutive points
    x_base = [] #the base x values (first values) of the vectors to have somewhere to plot them
    y_base = [] #the base y values (first values) of the vectors to have somewhere to plot them
    angles = [] #array of angles for the vectors we are finding
    i = 1
    while i < len(points)+1 :
        #Runs through all the points in the array of points that is getting passed in to the function. \
        deltax = x_points[i]-x_points[i-1] #distance between two consecutive x-values.
        deltay = y_points[i]-y_points[i-1] #distance between two consecutive y-values
        
        x_base.append(x_points[i-1]) #x_points and y_points being appended here are the first of the two points that build the vectors
        y_base.append(y_points[i-1])
        
        angle = np.arctan([deltax, deltay]) #calculates theta of the vector
        angles.append(angle[1]) #np.arctan spits out 2 values and we are choosing the second value
        
        
        vec_mag = np.sqrt(deltax**2 + deltay**2) #calculates the magnitude of the vector.
        
        xnorm = deltax/vec_mag #dx that is normalized with the magnitude
        ynorm = deltay/vec_mag #dy that is normalized with the magnitude
        
        dx.append(xnorm)
        dy.append(ynorm)

        vec_mags.append(vec_mag)
        i = i + 2 #so that it uses two consecutive points and then skips two ahead to grab the next two points that make up the next vector. 
        
    dx = np.array(dx)[np.newaxis] #converts the list to an array
    dy = np.array(dy)[np.newaxis]
    vec_mags = np.array(vec_mags)
    
    angles = np.array(angles)
    angles = angles.reshape(int(len(points)/2))
    av_dir = np.mean(angles)#average direction of the vectors
    print('Average direction of vectors is: ' + str(av_dir) + ' rad')

    x_base = np.array(x_base)[np.newaxis]
    y_base = np.array(y_base)[np.newaxis]
    x_base = x_base.reshape(int(len(points)/2))
    y_base = y_base.reshape(int(len(points)/2))
    
    plt.subplot(1,2,1)
    plt.hist(angles, bins = 100)
    plt.title('Histogram of Angles from Vectors')

    
    plt.subplot(1,2,2)
    vecs = plt.quiver(x_base, y_base, dx, -dy, label = 'Vectors')
    a = np.vstack([x_base, y_base, dx, -dy]).T.sum(axis=1)
    sum_vecs = plt.quiver(a[0],a[1],a[2],a[3], [3,2,5], label = 'Sum of Vectors')
    plt.legend(handles = [vecs, sum_vecs], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Plotted Vectors')
    plt.gca().invert_yaxis()

vectors(x,y,results)



        
        

