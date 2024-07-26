import os
import zipfile
import shutil
from git import Repo

def init():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

def extract_zip(zip_path):

    clear_uploads_dir()
    path = 'uploads/' + zip_path.split('/')[-1].split('.')[0]
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if not os.path.exists(path):
            os.makedirs(path)
        zip_ref.extractall(path)
    
    contents = os.listdir(path)
    return contents

def clear_uploads_dir():
    for file in os.listdir('uploads'):
        file_path = os.path.join('uploads', file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def clone_repo(url):
    clear_uploads_dir()
    path = 'uploads/' + url.split('/')[-1].split('.')[0]
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        Repo.clone_from(url, path)
        return path
    except Exception as e:
        print(e)
        return
    

def count_line_number(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return len(lines)

def count_words(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()
        return len(words)