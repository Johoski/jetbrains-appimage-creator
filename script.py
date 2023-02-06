import os
import shutil
import platform
from subprocess import call
from PIL import Image
# for now only works with ideaIU-2022.3.2

# common variables
dependencies = 'dependencies'
temp = 'temp'
icon_width = 256
icon_height = 256
arch = 'ARCH=x86_64'
appimagetool = 'dependencies/appimagetool-x86_64.AppImage'
# IntelliJ Idea Ultimate variables
AppDir_ideaIU = "temp/ideaIU-2022.3.2.AppDir"
usr_ideaIU = "temp/ideaIU-2022.3.2.AppDir/usr"
bin_ideaIU = "temp/ideaIU-2022.3.2.AppDir/usr/bin"
ideaIU = "ideaIU-2022.3.2/idea-IU-223.8617.56/"
icon_ideaIU = "ideaIU-2022.3.2/idea-IU-223.8617.56/bin/idea.png"
dep_ideaIU_AppRun = "dependencies/ideaIU/AppRun"
dep_ideaIU_desktop = "dependencies/ideaIU/ideaIU.desktop"
ideaIU_AppRun = "temp/ideaIU-2022.3.2.AppDir/AppRun"
ideaIU_desktop = "temp/ideaIU-2022.3.2.AppDir/ideaIU.desktop"

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
    shutil.copytree(ideaIU, bin_ideaIU)


def set_icon():
    icon = "temp/ideaIU-2022.3.2.AppDir/idea.png"
    with open(icon_ideaIU, 'r+b') as f:
        with Image.open(f) as image:
            image = Image.open(icon_ideaIU)
            new_image = image.resize((icon_width, icon_height))
            new_image.save(icon)


def copy_dependencies():
    call(["cp", dep_ideaIU_AppRun, ideaIU_AppRun])
    call(["cp", dep_ideaIU_desktop, ideaIU_desktop])

def createAppImage():
    os.system("sudo " + arch + " " + appimagetool + " " + AppDir_ideaIU)

check()
createAppDir()
copy_to_AppDir()
set_icon()
copy_dependencies()
createAppImage()