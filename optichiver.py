#!/usr/bin/env  python3

import glob
import shutil
import subprocess
import sys
import os
import PIL.Image

debug = 1   #debug toggle

#Empty Variable Declarations
size = 0
input_path = "/home/user1"
output_path = "/tmp/optichiver"

dvd_size=               4.7   #GB   #1
dvd_double_size=        9.4   #GB   #2
bluray_size=            25.0  #GB   #3
bluray_double_size=     50.0  #GB   #4
bluray_quad_size=       100.0 #GB   #5

#print ("Optichiver: Script for backing up to optical discs" + "\nEnsure there is enough disk space as this program will create file duplicates")

def size_input(size):
    while True:
        try:    
            input_size = int(input("Select disk" + "\n1: DVD(4.7 GB)" + "\n2: DVD Double Layer(9.4 GB)" + "\n3: Bluray(25GB)" + "\n4: Bluray Double Layer(50GB)" + "\n5: Bluray Quad Layer(100 GB)" + "\ninput: "))
        except ValueError:
            print ("\nInput was not valid")
            continue
        if (input_size == 1):
            size=   dvd_size
            break
        elif (input_size == 2):
            size=   dvd_double_size
            break
        elif (input_size == 3):
            size=   bluray_size
            break
        elif (input_size == 4): 
            size=   bluray_double_size
            break
        elif (input_size == 5):
            size=   bluray_quad_size
            break
        else:
            continue
    if (debug == 1):
         print ("Selected disk size was ",size,"GB")

def file_paths(input_path, output_path,debug):
    input_path_temp = input("\nInput path: ")
    if (len(input_path_temp) > 0 and len(input_path_temp) < 4097):
        if (debug == 1):
            print ("input_path length is: ", len(input_path_temp))
        input_path = input_path_temp
    else:
        print ("Error input is incorrect")
        input_path_temp = input("\nInput path: ")

    output_path_temp = input("\nOutput path: ")
    if (len(output_path_temp) > 0 and len(output_path_temp) < 4097 and output_path_temp != input_path_temp):
        if (debug == 1):
            print ("output_path length is: ", len(output_path_temp))
        output_path = output_path_temp
    else:
        print ("Error input is incorrect")
        output_path_temp = input("\nOutput path: ")

def free_space_checker(input_path,output_path,debug):
    if (debug == 1):
        print ("\n")
        subprocess.run("! " + output_path, shell=True)
        print("\n")
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    input = int(subprocess.check_output("df -B1 --output=used " + input_path + "| grep -x -E '[[:digit:]]+'", shell=True,universal_newlines=True))
    output = int(subprocess.check_output("df -B1 --output=avail " + output_path + "| grep -x -E '[[:digit:]]+'", shell=True,universal_newlines=True))

    if(debug == 1):
        print (input_path, "used:", int(input), "Bytes")
        print (output_path,"free:", int(output), "Bytes")
    if(output > input):
        print ("Free space remaining on", output_path + ": ", output - input, " Bytes")
    else:
        if (debug == 1):
            print("Space needed: ", -1* (output - input), " Bytes")
        sys.exit("ERROR: Insufficient Space")

def file_sorter(input_path,output_path,debug,size):
    shutil.copytree(input_path,output_path,symlinks=False,ignore=None)
    if (debug == 1):
        print("\nFiles copied to output")
        subprocess.run("ls -la " + output_path, shell=True)
        print("\n")


#def file_sorter_photos(input_path,output_path,debug,size):
#    extensions = ["jpg","png","bmp","jpeg","tif","tiff","nef"] #add more extensions as needed and or compile a larger list of image formats raw/compressed
#    for extension in extensions:
#        photos= glob.glob(output_path + '/**/*.' + extension, recursive=True)
#   Image.open(path)._getexit()[36867]
    

#photos function #support for exif extraction
#photo album/folder function
#files function

    

#size_input(size,debug)
#file_paths(input_path,output_path,debug)
#free_space_checker(input_path,output_path,debug)
