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
checksum = ""
debug = 0           #debug 
input_path_size = 0 
input_hash_file = ""
input_path = ""
label = ""
output_path = ""
size = 0

#Static Variable Declarations
date = time.strftime('%Y-%m-%d_%T') #Date variable
path = os.getcwd()
start = time.time()

print ("Optichiver: Script for backing up to optical discs")

#Argument parsing
parser = argparse.ArgumentParser(description="Optichiver cli", formatter_class=RawTextHelpFormatter)

#input path(input)
parser.add_argument("--input",help="Input path",default=None)

#hashfile(hashfile)
parser.add_argument("--hashfile",help="Input hash file",default=None)

#label(label)
parser.add_argument("--label",help="Set disc label prefix",default="disc")

#output path(output)
parser.add_argument("--output",help="Output path",default=None)

#size(size)
parser.add_argument("--size",
        help="Disc size:\n"
        "\tDVD\t4.7GB\n"
        "\tDVD-DL\t9.4GB\n"
        "\tBL\t25GB\n"
        "\tBL-DL\t50GB\n"
        "\tBL-QL\t100GB\n"
        ,default="DVD",type=str)

#custom(custom)
parser.add_argument("--custom",help="Custom disc size (int)B")

#checksum(checksum)
parser.add_argument("--checksum",
        help="Checksum algorithm:\n"
            "\tmd5\n"
            "\tsha1\n"
            "\tsha224\n"
            "\tsha256\n"
            "\tsha384\n"
            "\tsha512\n"
            ,default="md5",type=str)

#verify(verify)
parser.add_argument("--verify",help="Verify checksums on output",action="store_true")

#verbose(v)
parser.add_argument("--verbose",help="Increase output verbosity",action="store_true")

args = parser.parse_args()

#input
if (args.input == None):
    print("\nERROR: input path was not configured")
    quit()
else:
    input_path = args.input
    print(input_path)
    if not (os.path.isdir(input_path)):
        print("\nERROR: input path is not valid")
        quit()
    if (debug == 1):
        print("debug> input path:",input_path)

#input hashfile
if (args.hashfile == None):
    print("\nERROR: input hash file was not configured")
    quit()
else:
    input_hash_file = args.hashfile
    if (debug == 1):
        print("debug> input hash file:",input_hash_file)

#label
if(args.label):
    label = args.label
    if(debug == 1):
        print("debug> disc label:",label)

#output
if (args.output == None):
    print("\nERROR: output path was not configured")
    quit()
else:
    output_path = args.output
    if not (os.path.isdir(output_path)):
        print("\nERROR: output path is not valid")
        quit()
    if (debug == 1):                               
        print("debug> output path:",output_path)     

#size
if (args.size == "DVD"):
    size = 4.7E9
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "DVD-DL"):
    size = 9.4E9
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "BL"):
    size = 25E9
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "BL-DL"):
    size = 5E10
    if(debug == 1):
        print("debug> disc size:",size)
elif (args.size == "BL-QL"):
    size = 1E11
    if(debug == 1):
        print("debug> disc size:",size)
else:
    print("\nERROR: disc size is not valid")
    quit()

#custom
if (args.custom):
    size = int(args.custom)
    if(debug == 1):
        print("debug> disc size:",size)
else:
    print("\nERROR: custom size is not valid")
    quit()

#checksum
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

#verbose
if (args.verbose):
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
    global label
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

            if (folder_size + image_size > size):     
                folder += 1
                folder_name = label + "_" + str(folder + 1).zfill(3)
                output_folder = os.path.join(output_path,folder_name)
                folder_size = 0

            folder_name = label + "_" + str(folder).zfill(3)
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

#verifies input_hash_file with specified path(created iso/udf file and or burnt disc)
def verify_output(verify_path):
    global checksum
    global debug
    global input_hash_file
    global output_path
    
    verify_path = output_path   #default value is output_path
    verify_hash_file = os.path.join(verify_path,"verify_hash_file.toml")
    
    if os.path.exists(input_hash_file) and os.path.exists(output_path):
        if not os.path.exists(verify_path):
            os.mkdir(verify_path)
            if(debug == 1):
                print("debug> os.mkdir(verify_path)")
        if (debug == 1):
            print("debug> os.listdir(verify_path)")
        if not os.path.exists(input_hash_file):
            for path,dirs,files in os.walk(verify_path):
                for file in files:
                    verify_image = os.path.join(verify_path,file)
                    with open (verify_image,'rb') as hash:
                        hash_data = hash.read()
                        checksum.update(hash_data)
                        with open(verify_hash_file,'a') as hashes:
                            hashes.write(toml.dumps({file: checksum.hexdigest()}))
                        if (debug == 1):
                            print("debug> file hash",file,":",checksum.hexdigest())
        else:
            print("\nERROR: verification hash file exists")
            quit()
    else:
        print("\nERROR: output path or input hash file do not exist")
        quit()

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

free_space_checker()
if __name__ == "__main__":
    input_checksum_thread = threading.Thread(target=input_checksum_photos, args=())
    input_checksum_thread.start()
file_sorter_photos()
verify_output(output_path)
