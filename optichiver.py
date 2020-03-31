#!/usr/bin/env  python3

import hashlib
import shutil
import subprocess
import sys
import os
import exifread
import threading
import toml
import re

debug = 0   #debug toggle

#Empty Variable Declarations
size = 0
input_size = 0
input_path = ""
output_path = ""

#Static Variable Declarations
checksum = hashlib.sha256()

dvd_size=               4.7E9   #B   #input_size == 1
dvd_double_size=        9.4E9   #B   #input_size == 2
bluray_size=            25E9    #B   #input_size == 3
bluray_double_size=     50E9    #B   #input_size == 4
bluray_quad_size=       100E9   #B   #input_size == 5

print ("Optichiver: Script for backing up to optical discs")

def size_input():
    global size
    global debug
    while True:
        try:    
            input_size = int(input("Select disk" + "\n1: DVD(4.7GB)" + "\n2: DVD Double Layer(9.4GB)" + "\n3: Bluray(25GB)" + "\n4: Bluray Double Layer(50GB)" + "\n5: Bluray Quad Layer(100GB)" + "\ninput: "))
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
         print ("Selected disk size was ",size,"B")

def file_paths():
    global input_path
    global output_path
    global debug
    input_path_temp = input("\nInput path: ")
    if (len(input_path_temp) > 0):
        if (debug == 1):
            print ("input_path length is: ", len(input_path_temp))
        input_path = input_path_temp
    else:
        print ("Error input is incorrect")
        input_path_temp = input("\nInput path: ")

    output_path_temp = input("\nOutput path: ")
    if (len(output_path_temp) > 0 and output_path_temp != input_path_temp): 
        if (debug == 1):
            print ("output_path length is: ", len(output_path_temp))
        output_path = output_path_temp
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
    else:
        print ("Error input is incorrect")
        output_path_temp = input("\nOutput path: ")

def free_space_checker():
    global input_path
    global output_path
    global debug
    global input_size
    for path,dirs,files in os.walk(input_path):
        for f in files:
            fp = os.path.join(path,f)
            input_size += os.path.getsize(fp)
    print (input_size)
    output_free = int(os.statvfs(output_path)[1] * os.statvfs(output_path)[7])
    if(debug == 1):
        print ("input:  ",input_path,"used:", "\t",input_size, "\tBytes")
        print ("output: ",output_path,"free:","\t",output_free, "\tBytes")
    if(output_free < input_size):
        sys.exit("\nERROR: Insufficient Space")

def file_sorter_photos():
    global input_path
    global output_path
    global debug
    global checksum
    global size
    folder_size = 0
    folder = 1
    for file in os.listdir(input_path):
        if (debug == 1):
            print ("Input path:","\t",os.path.abspath(input_path))
        print ("File:","\t","\t",file)
        image_path = os.path.join(input_path,file)
        if (debug == 1):
            print ("File path:","\t",image_path)
            print ("File size:","\t",os.path.getsize(image_path),"Bytes")
        #Exif Parser    
        with open(image_path,'rb') as image_file:
            tags = exifread.process_file(image_file,details=False)

            if (image_file == None):                        #Non Exif image parser format: yyyymmdd_hhmmss
                image_filename = re.findall(r'\d+',file)    #Regex digit string parser
                if (len(image_filename[0]) == 8):           #8 character check
                    image_date_year = image_filename[0][0:4]
                    image_date_month = image_filename[0][4:6]
                    image_date_day = image_filename[0][6:8]
            else:
                image_date = tags.get('Image DateTime')
                image_date_year = str(image_date)[0:4]
                image_date_month = str(image_date)[5:7]
                image_date_day = str(image_date)[8:10]

            if (debug == 1):
                print ("File date:","\t",image_date)
                print ("File year:","\t",image_date_year) 
                print ("File month:","\t",image_date_month)
                print ("File day:","\t",image_date_day)

            image_size = os.path.getsize(image_path)    #input image size

            if (folder_size + image_size > size - 1E7):
                folder += 1
                folder_name = "disk" + str(folder + 1)
                output_folder = os.path.join(output_path,folder_name)
                folder_size = 0

            folder_name = "disk" + str(folder)
            output_folder = os.path.join(output_path,folder_name)

            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)
            
            image_file_year = os.path.join(output_folder,image_date_year)         
            image_file_month = os.path.join(image_file_year,image_date_month)     
            image_file_day = os.path.join(image_file_month,image_date_day)        
                                                                             
            if not os.path.isdir(image_file_year):                               
                os.mkdir(image_file_year)                                        
            if not os.path.isdir(image_file_month):                              
                os.mkdir(image_file_month)                                       
            if not os.path.isdir(image_file_day):                                
                os.mkdir(image_file_day)
            
            if(debug == 1):                                                      
                print("\nOutput path variables:")                                
                print("image file year: ", image_file_year)                      
                print("image file month:", image_file_month)                     
                print("image file day:  ", image_file_day)
                
            shutil.copy(image_path,image_file_day,follow_symlinks=False)

            folder_size += image_size
            hash_data = image_file.read()
            checksum.update(hash_data)
            output_hash_file = os.path.join(output_folder,'hashes.toml')
            with open(output_hash_file,'a') as hashes:
                hashes.write(toml.dumps({file: checksum.hexdigest()}))

def input_checksum():
    global debug
    global input_path
    global checksum
    if not os.path.exists('hashes.toml'):
        print ("\nInput Checksum Thread:")
        for path,dirs,files in os.walk(input_path):
            for file in files:
                input_image = os.path.join(input_path,file)
                with open (input_image,'rb') as hash:
                    hash_data = hash.read()
                    checksum.update(hash_data)
                    with open('hashes.toml','a') as hashes:
                        hashes.write(toml.dumps({file: checksum.hexdigest()}))
                    if (debug == 1):
                        print("Input Checksum Thread:","input checksum")
                        print("Input Checksum Thread:","input path:\t\t",input_image)
                        print("----",file,"\t",":\t",checksum.hexdigest()[56:64],"----")

size_input()
file_paths()
free_space_checker()
if __name__ == "__main__":
    input_checksum_thread= threading.Thread(target=input_checksum, args=())
    input_checksum_thread.start()
file_sorter_photos() 
