#!/usr/bin/env  python3

#Libraries
import argparse
from argparse import RawTextHelpFormatter
import exifread
import hashlib
import os
import platform
import re
import shutil
import subprocess
import sys
import threading
import time
import toml


#Empty Variable Declarations
debug = 0       #debug 
input_path_size = 0 
input_hash_file = ""
input_path = ""
output_path = ""
checksum = ""
size = 0

#Static Variable Declarations
date = time.strftime('%Y-%m-%d_%T') #Date variable
path = os.getcwd()
start = time.time()

print ("Optichiver: Script for backing up to optical discs")

#Argument parsing
parser = argparse.ArgumentParser(description="Optichiver cli", formatter_class=RawTextHelpFormatter)

#input path(input)
parser.add_argument("--input",help="Input path",default="NONE",type=str)

#input-hash(input-hash)
parser.add_argument("--input-hash",help="Input hash file",default="NONE",type=str)

#recursion(recursive)
parser.add_argument("--recursive",help="Recursion enable",action="store_true")

#output path(output)
parser.add_argument("--output",help="Output path",default="NONE",type=str)

#size(size)
parser.add_argument("--size",
        help="Disc size:\n"
        "\tCD\t750MB\n"
        "\tDVD\t4.7GB\n"
        "\tDVD-DL\t9.4GB\n"
        "\tBL\t25GB\n"
        "\tBL-DL\t50GB\n"
        "\tBL-QL\t100GB\n"
        "\tCustom\t(int)B\n"
        ,default="DVD",type=str)

#checksum(checksum)
parser.add_argument("--checksum",
        help="Checksum algorithm:\n"
            "\tmd5\n"
            "\tsha1\n"
            "\tsha224\n"
            "\tsha256\n"
            "\tsha384\n"
            "\tsha512\n"
            ,default="hashlib.md5()",type=str)

#verify(verify)
parser.add_argument("--verify",help="Verify checksums on output",action="store_true")

#verbose(v)
parser.add_argument("-v","--verbose",help="Increase output verbosity",action="store_true")

args = parser.parse_args()

#args.input
if (args.input == "NONE"):
    print("\nERROR: input path was not configured")
    quit()
else:
    input_path = os.path(args.input)
    if not (os.path.exists(input_path)):
        print("\nERROR: input path is not valid")
        quit()

    if (debug == 1):
        print("debug> input path:",input_path)

if (args.input-hash == "NONE"):
    print("\nERROR: input hash file was not configured")
    quit()
else:
    input_hash_file = os.path(args.input-hash)
    if (debug == 1):
        print("debug> input hash file:",input_hash_file)

#args.recursive
if (args.input):
    recursive = args.recursive
    if(debug == 1):
        print("debug> recursion enabled: ",recursive)

#args.output
if (args.output == "NONE"):
    print("\nERROR: output path was not configured")
    quit()
else:
    output_path = os.path(args.input)
    if not (os.path.exists(output_path)):
        print("\nERROR: output path is not valid")
        quit()

    if (debug == 1):                               
        print("debug> input path:",input_path)     

#args.size
if (args.size == "DVD"):
    size = args.size
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "DVD-DL"):
    size = args.size
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "BL"):
    size = args.size
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "BL-DL"):
    size = args.size
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "BL-QL"):
    size = args.size
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "Custom"):
    size = args.size
    if(debug == 1):
        print("debug> disc size:",size)
else:
    print("\nERROR: input is not valid")
    quit()

#args.checksum
if(args.checksum == "md5"):
    checksum = hashlib.md5()
    if(debug == 1):
        print("debug> checksum:",checksum)
elif(args.checksum == "sha1"):
    checksum = hashlib.sha1()
    if(debug == 1):
        print("debug> checksum:",checksum)
elif(args.checksum == "sha224"):
    checksum = hashlib.sha224()
    if(debug == 1):
        print("debug> checksum:",checksum)
elif(args.checksum == "sha256"):
    checksum = hashlib.sha256()
    if(debug == 1):
        print("debug> checksum:",checksum)
elif(args.checksum == "sha384"):
    checksum = hashlib.sha384()
    if(debug == 1):
        print("debug> checksum:",checksum)
elif(args.checksum == "sha512"):
    checksum = hashlib.sha512()
    if(debug == 1):
        print("debug> checksum:",checksum)
else:
    print("\nERROR: checksum is not valid")
    quit()

#args.v
if (args.v):
    debug = 1
    print("debug> Output verbosity on")

def free_space_checker():
    global debug
    global input_path
    global output_path
    global input_path_size

    for path,dirs,files in os.walk(input_path):
        for f in files:
            fp = os.path.join(path,f)
            input_path_size += os.path.getsize(fp)
    print (input_path_size)
    output_free = int(os.statvfs(output_path)[1] * os.statvfs(output_path)[7])
    if(debug == 1):
        print ("input:  ",input_path,"used:", "\t",input_path_size, "\tBytes")
        print ("output: ",output_path,"free:","\t",output_free, "\tBytes")
    if(output_free < input_path_size):
        sys.exit("\nERROR: Insufficient Space")

def file_sorter_photos():
    global checksum
    global debug
    global input_path
    global output_path
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

            if (folder_size + image_size > size - 1E7):     #offset by -1E7(10MB)
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
            output_hash_file = os.path.join(output_folder,'hashes.toml')    #add variable for output hashes file
            with open(output_hash_file,'a') as hashes:
                hashes.write(toml.dumps({file: checksum.hexdigest()}))

#Checksum of input photos
def input_checksum_photos():
    global checksum
    global debug
    global input_hash_file
    global input_path

    if not os.path.exists(input_hash_file):
        print ("\nInput Checksum Thread:")
        for path,dirs,files in os.walk(input_path):
            for file in files:
                input_image = os.path.join(input_path,file)
                with open (input_image,'rb') as hash:
                    hash_data = hash.read()
                    checksum.update(hash_data)
                    with open(input_hash_file,'a') as hashes:
                        hashes.write(toml.dumps({file: checksum.hexdigest()}))
                    if (debug == 1):
                        print("Input Checksum Thread:","input checksum")
                        print("Input Checksum Thread:","input path:\t\t",input_image)
#                        print("----",file,"\t",":\t",checksum.hexdigest()[56:64],"----")       #remove

free_space_checker()
if __name__ == "__main__":
    input_checksum_thread = threading.Thread(target=input_checksum_photos, args=())
    input_checksum_thread.start()
file_sorter_photos()

#if(mode == "files"):
    
