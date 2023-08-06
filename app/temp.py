# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import gzip
import shutil
import json

if os.getcwd().split("/")[-1] == "app":
    os.chdir("..")
    print("Changed working directory to root")
    print("Current working directory: ", os.getcwd())

# %%
def unzip_gz(input_file, output_file, tmp_dir):
    output_file = os.path.join(tmp_dir, output_file)
    with gzip.open(input_file, 'rb') as gz_file:
        with open(output_file, 'wb') as output:
            output.write(gz_file.read())

def unzip_all_gz_files(data_dir, tmp_dir):
    if tmp_dir not in os.listdir():
        os.mkdir(tmp_dir)
    for f in os.listdir(data_dir):
        if f.endswith('.gz'):
            unzip_gz(os.path.join(data_dir, f), f[:-3], tmp_dir)

def merge_jsonsdata(data_dir,tmp_dir, output_file):
    unzip_all_gz_files(data_dir, tmp_dir)
    data = []
    for f in os.listdir(tmp_dir):
        if f.endswith('.json'):
            with open(os.path.join(tmp_dir, f), 'r') as json_file:
                data.append(json_file.read())
    with open(os.path.join(data_dir, output_file), 'w') as output:
        json.dump(data, output, indent=4)
        
    remove_directory(tmp_dir)

def remove_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its contents have been removed successfully.")
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
    except PermissionError:
        print(f"Permission denied to remove directory '{directory_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def zip(file_path, location, root):
    file_path = os.path.join(root, file_path)
    location = os.path.join(root, location)
    with open(file_path, 'rb') as src, gzip.open(location, 'wb') as dst:
        dst.writelines(src)
    
data_dir = 'data'
data_fname = 'data.json'
data_gzip_fname = 'data.json.gz'
data_path = os.path.join(data_dir, data_fname)
tmp_dir = 'tmp'

if data_gzip_fname not in os.listdir(data_dir):
    merge_jsonsdata(data_dir,tmp_dir, data_fname)
    zip(data_fname, data_gzip_fname, data_dir)
else:
    print(f"File '{data_path}' already exists.")

# %%



