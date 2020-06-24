#!/usr/bin/env  python3

#Libraries
import argparse
from argparse import RawTextHelpFormatter
import exifread
import os
import platform
import re
import shutil
import subprocess
import threading
import time
import toml


#Empty Variable Declarations
checksum = ""
checksum_command = ""
debug = 0        
format_method = ""
hash_mode = 0
input_path_size = 0 
input_hash_file = ""
input_path = ""
label = ""
output_path = ""
size = 0
skipcheck = 0

#Static Variable Declarations
date = time.strftime('%Y-%m-%d_%T') #Date variable
path = os.getcwd()
start = time.time()

print ("Optichiver: Script for backing up to optical discs\n")

#Argument parsing
parser = argparse.ArgumentParser(description="Optichiver cli", formatter_class=RawTextHelpFormatter)

#input path(input)
parser.add_argument("--input",help="Input path",default=None)

#output path(output)
parser.add_argument("--output",help="Output path",default=None)

#skip file check
parser.add_argument("--skipcheck",help="Skip system file check",action="store_true")

#size(size)
parser.add_argument("--size",
        help="Disc size:\n"
        "\tDVD\t4.7GB(default)\n"
        "\tDVD-DL\t9.4GB\n"
        "\tBD\t25GB\n"
        "\tBD-DL\t50GB\n"
        "\tBD-QL\t100GB\n"
        ,default="DVD",type=str)

#custom(custom)
parser.add_argument("--custom",
        help="Custom size:\n" 
        "\t(int)B\n",default=None)

#label(label)
parser.add_argument("--label",help="Set disc label prefix",default="disc")

#format
parser.add_argument("--format",
        help="Output file format\n"
        "\tYMD\t\t/label/year/month/dir/image.jpg\n"
        "\tYM\t\t/label/year/month/image.jpg\n"
        "\tY\t\t/label/year/image.jpg\n"
        "\tNONE(default)\t/label/image.jpg\n"
        ,default="NONE")
#hash
parser.add_argument("--hash",help="Enable hashing",action="store_true")

#checksum(checksum)
parser.add_argument("--checksum",
        help="Checksum algorithm:\n"
            "\tblake2\n"
            "\tmd5\n"
            "\tsha1\n"
            "\tsha224\n"
            "\tsha256(default)\n"
            "\tsha384\n"
            "\tsha512\n"
            ,default="sha256")

#hashfile(hashfile)
parser.add_argument("--hashfile",help="Input hash file",default=None)

#verbose(v)
parser.add_argument("--verbose",help="Increase output verbosity",action="store_true")

args = parser.parse_args()

#verbose
if (args.verbose):
    debug = 1
    print("debug> Output verbosity on")

#input
if (args.input == None):
    print("\nERROR: input path was not configured")
    quit()
else:
    input_path = args.input
    if not (os.path.isdir(input_path)):
        print("\nERROR: input path is not valid")
        quit()
    if (debug == 1):
        print("debug> input path:",input_path)

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

#skipcheck
if (args.skipcheck):
    skipcheck = 1
    if(debug == 1):
        print("debug> skipcheck:",skipcheck)

#size
if not (args.custom):
    if (args.size == "DVD"):
        size = 4.7E9
        if(debug == 1):
            print("debug> disc size:",size)
    elif (args.size == "DVD-DL"):
        size = 9.4E9
        if(debug == 1):
            print("debug> disc size:",size)
    elif (args.size == "BD"):
        size = 25E9
        if(debug == 1):
            print("debug> disc size:",size)
    elif (args.size == "BD-DL"):
        size = 5E10
        if(debug == 1):
            print("debug> disc size:",size)
    elif (args.size == "BD-QL"):
        size = 1E11
        if(debug == 1):
            print("debug> disc size:",size)
    else:
        print("\nERROR: disc size is not valid")
        quit()

#custom
elif (args.custom):
    size = int(args.custom)
    if(debug == 1):
        print("debug> disc size:",size)
else:
    print("\nERROR: custom size is not valid")
    quit()

#format
if(args.format == "YMD"):
    format_method = "YMD"
    if(debug == 1):
        print("debug> format:",format_method)
elif(args.format == "YM"):
    format_method = "YM"
    if(debug == 1):
        print("debug> format:",format_method)
elif(args.format == "Y"):
    format_method = "Y"
    if(debug == 1):
        print("debug> format:",format_method)
elif(args.format == "NONE"):
    format_method = "NONE"
    if(debug == 1):
        print("debug> format:",format_method)
else:
    print("\nERROR: format invalid")
    quit()

#checksum
if(args.hash):
    hash_mode = 1 
    if(args.checksum == "blake2"):
        checksum = "blake2"
        checksum_command = "b2sum"
        if(debug == 1):
            print("debug> checksum:",checksum)
    elif(args.checksum == "md5"):
        checksum = "md5"
        checksum_command = "md5sum"
        if(debug == 1):
            print("debug> checksum:",checksum)
    elif(args.checksum == "sha1"):
        checksum = "sha1"
        checksum_command = "sha1sum"
        if(debug == 1):
            print("debug> checksum:",checksum)
    elif(args.checksum == "sha224"):
        checksum = "sha224"
        checksum_command = "sha224sum"
        if(debug == 1):
            print("debug> checksum:",checksum)
    elif(args.checksum == "sha256"):
        checksum = "sha256"
        checksum_command = "sha256sum"
        if(debug == 1):
            print("debug> checksum:",checksum)
    elif(args.checksum == "sha384"):
        checksum = "sha384"
        checksum_command = "sha384sum"
        if(debug == 1):
            print("debug> checksum:",checksum)
    elif(args.checksum == "sha512"):
        checksum = "sha512"
        checksum_command = "sha512sum"
        if(debug == 1):
            print("debug> checksum:",checksum)
    else:
        print("\nERROR: checksum is not valid")
        quit()

#input hashfile
if (args.hashfile == None):
    print("\nERROR: input hash file was not configured")
    quit()
else:
    input_hash_file = args.hashfile
    if (debug == 1):
        print("debug> input hash file:",input_hash_file)

def free_space_checker():
    global debug
    global input_path
    global output_path
    global input_path_size

    for path,dirs,files in os.walk(input_path):
        for f in files:
            fp = os.path.join(path,f)
            input_path_size += os.path.getsize(fp)
    output_free = int(os.statvfs(output_path)[1] * os.statvfs(output_path)[7])
    if(debug == 1):
        print ("debug> input:  ",input_path,"used:", "\t",input_path_size, "\tBytes")
        print ("debug> output: ",output_path,"free:","\t",output_free, "\tBytes")
    if(output_free < input_path_size):
        print("\nERROR: Insufficient Space")
        quit()

def file_sorter_photos():
    global checksum_command
    global debug
    global input_path
    global hash_mode
    global label
    global output_path
    global path
    global size

    folder_size = 0
    folder = 1
    os.chdir(output_path)
    for file in os.listdir(input_path):
        if (debug == 1):
            print ("Input path:","\t",os.path.abspath(input_path))
        print ("File:","\t\t",file)
        image_path = os.path.join(input_path,file)
        if (debug == 1):
            print ("File path:","\t",image_path)
            print ("File size:","\t",os.path.getsize(image_path),"Bytes")
        
        #format YMD
        if(format_method == "YMD"):
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
                    output_folder = os.path.relpath(folder_name)
                    folder_size = 0

                folder_name = label + "_" + str(folder).zfill(3)
                output_folder = os.path.relpath(folder_name)

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
                    
                shutil.copy2(image_path,image_file_day)

                folder_size += image_size
                if (hash_mode == 1): 
                    output_image_path = os.path.join(image_file_day,file)
                    output_command = subprocess.run([checksum_command,output_image_path],check=True,capture_output=True,encoding='utf8')

                    output_hash_file = os.path.join(output_folder,'hashes.toml')
                    with open(output_hash_file,'a') as output_hashes:
                        output_hashes.write(toml.dumps({file: output_command.stdout.strip()}))

        #format YM
        elif(format_method == "YM"):
            #Exif Parser
            with open(image_path,'rb') as image_file:
                tags = exifread.process_file(image_file,details=False)

                if (image_file == None):                        #Non Exif image parser format: yyyymmdd_hhmmss
                    image_filename = re.findall(r'\d+',file)    #Regex digit string parser
                    if (len(image_filename[0]) == 8):           #8 character check
                        image_date_year = image_filename[0][0:4]
                        image_date_month = image_filename[0][4:6]
                else:
                    image_date = tags.get('Image DateTime')
                    image_date_year = str(image_date)[0:4]
                    image_date_month = str(image_date)[5:7]

                if (debug == 1):
                    print ("File date:","\t",image_date)
                    print ("File year:","\t",image_date_year) 
                    print ("File month:","\t",image_date_month)

                image_size = os.path.getsize(image_path)    #input image size

                if (folder_size + image_size > size):     
                    folder += 1
                    folder_name = label + "_" + str(folder + 1).zfill(3)
                    output_folder = os.path.relpath(folder_name)
                    folder_size = 0

                folder_name = label + "_" + str(folder).zfill(3)
                output_folder = os.path.relpath(folder_name)

                if not os.path.isdir(output_folder):
                    os.mkdir(output_folder)
                
                image_file_year = os.path.join(output_folder,image_date_year)         
                image_file_month = os.path.join(image_file_year,image_date_month)     
                                                                                 
                if not os.path.isdir(image_file_year):                               
                    os.mkdir(image_file_year)                                        
                if not os.path.isdir(image_file_month):                              
                    os.mkdir(image_file_month)                                       
                
                if(debug == 1):                                                      
                    print("\nOutput path variables:")                                
                    print("image file year: ", image_file_year)                      
                    print("image file month:", image_file_month)                     
                    
                shutil.copy2(image_path,image_file_month)

                folder_size += image_size
                
                if (hash_mode == 1):
                    output_image_path = os.path.join(image_file_month,file)
                    output_command = subprocess.run([checksum_command,output_image_path],check=True,capture_output=True,encoding='utf8')

                    output_hash_file = os.path.join(output_folder,'hashes.toml')
                    with open(output_hash_file,'a') as output_hashes:
                        output_hashes.write(toml.dumps({file: output_command.stdout.strip()}))

        #format Y
        elif(format_method == "Y"):
            #Exif Parser
            with open(image_path,'rb') as image_file:
                tags = exifread.process_file(image_file,details=False)

                if (image_file == None):                        #Non Exif image parser format: yyyymmdd_hhmmss
                    image_filename = re.findall(r'\d+',file)    #Regex digit string parser
                    if (len(image_filename[0]) == 8):           #8 character check
                        image_date_year = image_filename[0][0:4]
                else:
                    image_date = tags.get('Image DateTime')
                    image_date_year = str(image_date)[0:4]

                if (debug == 1):
                    print ("File date:","\t",image_date)
                    print ("File year:","\t",image_date_year) 
                
                image_size = os.path.getsize(image_path)    #input image size

                if (folder_size + image_size > size):     
                    folder += 1
                    folder_name = label + "_" + str(folder + 1).zfill(3)
                    output_folder = os.path.relpath(folder_name)
                    folder_size = 0

                folder_name = label + "_" + str(folder).zfill(3)
                output_folder = os.path.relpath(folder_name)

                if not os.path.isdir(output_folder):
                    os.mkdir(output_folder)
                
                image_file_year = os.path.join(output_folder,image_date_year)         
                                                                                 
                if not os.path.isdir(image_file_year):                               
                    os.mkdir(image_file_year)                                        
                
                if(debug == 1):                                                      
                    print("\nOutput path variables:")                                
                    print("image file year: ", image_file_year)                      
                    
                shutil.copy2(image_path,image_file_year)

                folder_size += image_size

                if (hash_mode == 1):
                    output_image_path = os.path.join(image_file_year,file)
                    output_command = subprocess.run([checksum_command,output_image_path],check=True,capture_output=True,encoding='utf8')

                    output_hash_file = os.path.join(output_folder,'hashes.toml')
                    with open(output_hash_file,'a') as output_hashes:
                        output_hashes.write(toml.dumps({file: output_command.stdout.strip()}))

        #format NONE
        elif(format_method == "NONE"):
            image_size = os.path.getsize(image_path)    #input image size

            if (folder_size + image_size > size):     
                folder += 1
                folder_name = label + "_" + str(folder + 1).zfill(3)
                output_folder = os.path.relpath(folder_name)
                folder_size = 0

            folder_name = label + "_" + str(folder).zfill(3)
            output_folder = os.path.relpath(folder_name)                

            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)

            shutil.copy2(image_path,output_folder)
            
            folder_size += image_size

            if (hash_mode == 1):
                output_image_path = os.path.join(output_folder,file) 
                output_command = subprocess.run([checksum_command,output_image_path],capture_output=True,encoding='utf8')
                
                output_hash_file = os.path.join(output_folder,'hashes.toml')
                with open(output_hash_file,'a') as output_hashes:
                    output_hashes.write(toml.dumps({file: output_command.stdout.strip()}))
    os.chdir(path)

#Checksum of input photos
def input_checksum_photos():
    global checksum_command
    global debug
    global input_hash_file
    global input_path
    
    if not os.path.exists(input_hash_file):
        print ("\nInput Checksum Thread:")
        for file in os.listdir(input_path):
            image_path = os.path.join(input_path,file)
            input_command = subprocess.run([checksum_command,image_path],capture_output=True,encoding='utf8')
            with open(input_hash_file,'a') as hashes:
                hashes.write(toml.dumps({file: input_command.stdout.strip()}))

if not (skipcheck == 1):
    free_space_checker()
if (hash_mode == 1):
    if __name__ == "__main__":
            input_checksum_thread= threading.Thread(target=input_checksum_photos, args=())
            input_checksum_thread.start()
file_sorter_photos()

print("\nScript complete in",round(time.time()-start,3),'seconds')
