import os
import shutil
import platform
import json
from PIL import Image
# for now only works with ideaIU-2022.3.2

# common variables
dependencies = 'dependencies'
temp = 'temp'
icon_size = 256
arch = 'ARCH=x86_64'
appimagetool = 'dependencies/appimagetool-x86_64.AppImage'
# read IntelliJ Idea Ultimate variables from conf.json
with open(os.path.join(dependencies, 'conf.json')) as f:
    conf = json.load(f)
    ideaIU_conf = conf['ideaIU-2022_3_2']
    AppDir_ideaIU = ideaIU_conf['AppDir']
    usr_ideaIU = ideaIU_conf['usr']
    bin_ideaIU = ideaIU_conf['bin']
    source = ideaIU_conf['source']
    icon_ideaIU = ideaIU_conf['icon']
    dep_ideaIU_AppRun = ideaIU_conf['dep_AppRun']
    dep_ideaIU_desktop = ideaIU_conf['dep_desktop']
    ideaIU_AppRun = ideaIU_conf['AppRun']
    ideaIU_desktop = ideaIU_conf['desktop']

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


# creates AppDir
def createAppDir():
    istemp = os.path.isdir(temp)
    if istemp:
        shutil.rmtree(temp)
        os.mkdir(temp)
    else:
        os.mkdir(temp)
    os.mkdir(AppDir_ideaIU)
    os.mkdir(usr_ideaIU)

# copies the folder to the appimage one
def copy_to_AppDir():
    shutil.copytree(source, bin_ideaIU)


def set_icon():
    icon = "temp/ideaIU-2022.3.2.AppDir/idea.png"
    with open(icon_ideaIU, 'r+b') as f:
        with Image.open(f) as image:
            image = Image.open(icon_ideaIU)
            new_image = image.resize((icon_size, icon_size))
            new_image.save(icon)


def copy_dependencies():
    os.system("cp " + dep_ideaIU_AppRun + " " + ideaIU_AppRun)
    os.system("cp " + dep_ideaIU_desktop + " " + ideaIU_desktop)

def createAppImage():
    os.system("sudo " + arch + " " + appimagetool + " " + AppDir_ideaIU)

check()
createAppDir()
copy_to_AppDir()
set_icon()
copy_dependencies()
createAppImage()
