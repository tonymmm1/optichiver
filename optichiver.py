#!/usr/bin/env  python3

import hashlib
import shutil
import subprocess
import sys
import os
import exifread
import threading
import toml

debug = 0   #debug toggle

#Empty Variable Declarations
size = 0
input_size = 0

input_path = "/home/user1/temp/input"   #remove 
output_path = "/home/user1/temp/output" #remove 

#Static Variable Declarations
checksum = hashlib.sha256()

dvd_size=               4.7E9   #B   #input_size == 1
dvd_double_size=        9.4E9   #B   #input_size == 2
bluray_size=            25.0E9  #B   #input_size == 3
bluray_double_size=     50.0E9  #B   #input_size == 4
bluray_quad_size=       100.0E9 #B   #input_size == 5

#uncomment
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
         print ("Selected disk size was ",size,"B")

def file_paths(input_path, output_path,debug):
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
    else:
        print ("Error input is incorrect")
        output_path_temp = input("\nOutput path: ")

def free_space_checker(input_path,output_path,debug,input_size):
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
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

#sorts files in single level directory ex: /images*.jpg
def file_sorter_photos(input_path,output_path,debug,checksum,size):
    size = 1E9
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
            if (folder_size + image_size > size - 1E6):
                folder += 1
                folder_name = "disk" + str(folder + 1)
                output_folder = os.path.join(output_path,folder_name)
                folder_size = 0
            folder_name = "disk" + str(folder)
            output_folder = os.path.join(output_path,folder_name)
            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)
            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)                   
            image_file_year = os.path.join(output_folder,image_date_year)         
            image_file_month = os.path.join(image_file_year,image_date_month)     
            image_file_day = os.path.join(image_file_month,image_date_day)        
                                                                             
            if not os.path.isdir(output_path):  #remove                           
                os.mkdir(output_path)           #remove                           
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

#    print("image size sum:\t",image_size_sum,"Bytes") #remove or debug
    
def input_checksum(debug,input_path,checksum):
    print ("\nInput Checksum Thread:")
    for file in os.listdir(input_path):
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

#photos function #support for exif extraction
#photo album/folder function
#files function

#if __name__ == "__main__":
#    input_checksum_thread= threading.Thread(target=input_checksum, args=(debug,input_path,hashlib.sha256()))
#    input_checksum_thread.start()

free_space_checker(input_path,output_path,debug,input_size)
file_sorter_photos(input_path,output_path,debug,checksum,size) #remove


#size_input(size,debug)
#file_paths(input_path,output_path,debug)
#free_space_checker(input_path,output_path,debug)
#if (nproc > 1):
#    multiprocessing(input_path,output_path,debug,nproc)

