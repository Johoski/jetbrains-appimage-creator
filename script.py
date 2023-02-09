import os
import shutil
import platform
import json
import tarfile
import requests
from PIL import Image
# for now only works with ideaIU-2022.3.2

# common variables
dependencies = 'dependencies'
temp = 'temp'
icon_size = 256
arch = 'ARCH=x86_64'
appimagetool = 'dependencies/appimagetool-x86_64.AppImage'
URL_appimagetool = "https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage"
# read IntelliJ Idea Ultimate variables from conf.json
with open(os.path.join(dependencies, 'conf.json')) as f:
    conf = json.load(f)
    ideaIU_conf = conf['ideaIU-2022_3_2']
    source_tar_file = ideaIU_conf['tar']
    AppDir_folder = ideaIU_conf['AppDir']
    usr_folder = ideaIU_conf['usr']
    bin_folder = ideaIU_conf['bin']
    source_folder = ideaIU_conf['source']
    source_icon = ideaIU_conf['source_icon']
    icon = ideaIU_conf['icon']
    dep_AppRun = ideaIU_conf['dep_AppRun']
    dep_desktop = ideaIU_conf['dep_desktop']
    AppRun = ideaIU_conf['AppRun']
    desktop = ideaIU_conf['desktop']

# checks if needed stuff is there
def check():
    if platform.system() == "Windows":
        print("OS:                  FAILED (This script is made for Linux only)")
        exit()
    elif platform.system() == "Linux" or platform.system() == "Linux2":
        print("OS:                  OK")
    isdependencies = os.path.isdir(dependencies)
    if isdependencies:
        print("Dependencies:        OK")
    else:
        print("Dependencies:        FAILED (Redownload the dependencies folder)")
        exit()
    isAppImagetool = os.path.isdir(appimagetool)
    if isAppImagetool:
        print("AppImage Tool:       OK")
    else:
        print("AppImage Tool:       FAILED (Starting download)")
        response = requests.get(URL_appimagetool)
        open(appimagetool, "wb").write(response.content)
        print("AppImage Tool:       FAILED (Download finished)")
        isAppImagetool = os.path.isdir(appimagetool)
        if isAppImagetool:
            print("AppImage Tool:       OK (Download succesful)")
        else:
            print("AppImage Tool:       FAILED (Download failed, download the file manually)")
            exit()


def extract():
    file = tarfile.open(source_tar_file)
    file.extractall(temp)
    file.close

# creates AppDir
def createAppDir():
    istemp = os.path.isdir(temp)
    if istemp:
        shutil.rmtree(temp)
        os.mkdir(temp)
    else:
        os.mkdir(temp)
    os.mkdir(AppDir_folder)
    os.mkdir(usr_folder)

# copies the folder to the appimage one
def copy_to_AppDir():
    shutil.copytree(source_folder, bin_folder)


def set_icon():
    with open(source_icon, 'r+b') as f:
        with Image.open(f) as image:
            image = Image.open(source_icon)
            new_image = image.resize((icon_size, icon_size))
            new_image.save(icon)


def copy_dependencies():
    os.system("cp " + dep_AppRun + " " + AppRun)
    os.system("cp " + dep_desktop + " " + desktop)

def createAppImage():
    os.system("sudo " + arch + " " + appimagetool + " " + AppDir_ideaIU)

check()
extract()
createAppDir()
copy_to_AppDir()
set_icon()
copy_dependencies()
createAppImage()
