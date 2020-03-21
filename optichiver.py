#!/usr/bin/env  python3

#import glob
import shutil
import subprocess
import sys
import os
import exifread
import multiprocessing as mp
debug = 0   #debug toggle

#Empty Variable Declarations
size = 0
input_path = "/home/user1/temp/input"   #remove 
output_path = "/mnt/nfs/servert1/temp/output" #remove 

dvd_size=               4.7   #GB   #input_size == 1
dvd_double_size=        9.4   #GB   #input_size == 2
bluray_size=            25.0  #GB   #input_size == 3
bluray_double_size=     50.0  #GB   #input_size == 4
bluray_quad_size=       100.0 #GB   #input_size == 5

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
         print ("Selected disk size was ",size,"GB")

def file_paths(input_path, output_path,debug):
    input_path_temp = input("\nInput path: ")
    if (len(input_path_temp) > 0): #and len(input_path_temp) < 4097):
        if (debug == 1):
            print ("input_path length is: ", len(input_path_temp))
        input_path = input_path_temp
    else:
        print ("Error input is incorrect")
        input_path_temp = input("\nInput path: ")

    output_path_temp = input("\nOutput path: ")
    if (len(output_path_temp) > 0 and output_path_temp != input_path_temp): #and len(output_path_temp) < 4097 ):
        if (debug == 1):
            print ("output_path length is: ", len(output_path_temp))
        output_path = output_path_temp
    else:
        print ("Error input is incorrect")
        output_path_temp = input("\nOutput path: ")

def free_space_checker(input_path,output_path,debug):
    input_size = 0
    output_size = 0
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    for path,dirs,files in os.walk(input_path):
        for f in files:
            fp = os.path.join(path,f)
            input_size += os.path.getsize(fp)
    for path,dirs,files in os.walk(output_path):
        for f in files:
            fp = os.path.join(path,f)
            output_size += os.path.getsize(fp)
    output_free = os.statvfs(output_path)[2]
    if(debug == 1):
        print ("input:  ",input_path,"used:", "\t",input_size, "\tBytes")
        print ("output: ",output_path,"free:","\t",output_free, "\tBytes")
    if(output_free > input_size):
        if (debug == 1):
            print ("free:   ", output_path + ": \t", output_size - input_size, "\tBytes")
    else:
        print("\nSpace needed: ", "\t\t\t\t",-1* (output_size - input_size), "\tBytes")
        sys.exit("\nERROR: Insufficient Space")

def file_sorter(input_path,output_path,debug,size):
    shutil.copytree(input_path,output_path,symlinks=False,ignore=None)
    if (debug == 1):
        print("\nFiles copied to output")
        subprocess.run("ls -la " + output_path, shell=True)
        print("\n")

def file_sorter_photos(input_path,output_path,debug,size):
    image_file_index = 1    #counts index of file within directory
    #implement multiprocess for folder index
    pool = mp.Pool(mp.cpu_count())
    for file in os.listdir(input_path)[index_min:index_max]
        if (debug == 1):
            print ("Input path:","\t",os.path.abspath(input_path))
        image_file_index +=1    #increments index of file by 1
        print ("File:","\t","\t",file)
        image_path = os.path.join(input_path,file)
        if (debug == 1):
            print ("File path:","\t",image_path)
            print ("File size:","\t",os.path.getsize(image_path),"Bytes")
        image_file = open(image_path,'rb')
        tags = exifread.process_file(image_file)
        image_date = tags.get('Image DateTime')
        image_date_year = str(image_date)[0:4]
        image_date_month = str(image_date)[5:7]
        image_date_day = str(image_date)[8:10]
        if (debug == 1):
            print ("File date:","\t",image_date)
            print ("File year:","\t",image_date_year)
            print ("File month:","\t",image_date_month)
            print ("File day:","\t",image_date_day)
            
        image_file_year = os.path.join(output_path,image_date_year) 
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
        if (debug == 1):
            print("\nOutput path:")
            for dir in os.walk(output_path):
                print (dir[0])

            print("\nOutput path variables:")
            print("image file year: ", image_file_year)
            print("image file month:", image_file_month)
            print("image file day:  ", image_file_day)

        shutil.copy(image_path,image_file_day,follow_symlinks=False)
        return 

def multiprocessing(input_path,output_path,debug):
    nproc = mp.cpu_count()
    pool = mp.Pool(nprocs)
    input_path_length = len([name for name in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, name))])
    print (input_path_length)
    files_per_thread = 0
    files_per_thread_offset = 0
    print (files_per_thread)
    print (files_per_thread_offset)
#    file_sorter_photos(input_path,output_path,debug,size)
#    n(nprocs) [0:n1] [n2:n3-1] [n3:n4-1]
#   [0 : task1(total/nproc)] [(total/nproc)+1: task2(total/nproc)]n
#    count = 1
    if (input_path_length % nproc == 0):
        files_per_thread = input_path_length / nproc
        for tasks in range (0,(nproc)):

    else:
        files_per_thread = input_path_length / (nproc - 1)
        files_per_thread_offset = input_path_length % (nproc - 1)
        for tasks in range (0,(nproc - 1)):


#def file_checksumming(image_file,debug,input_path,output_path)
#photos function #support for exif extraction
#photo album/folder function
#files function
#checksumming of folders
#checksumming of individual files
    

#size_input(size,debug)
#file_paths(input_path,output_path,debug)
#free_space_checker(input_path,output_path,debug)
#file_sorter_photos(input_path,output_path,debug,size)
#multiprocessing(input_path,output_path,debug)

