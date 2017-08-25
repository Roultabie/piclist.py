import os
import sys
import argparse
import re

imagesAllowed = (".jpg",".png",".gif",)
galleryDir = "gallery"
templateDir = "template"
thumbsDir = "_thumbs"
thumbsPath = os.path.join(galleryDir,thumbsDir)
thumbWidth = [200]
thumbRatio = [4, 3]
publicBase = ""
noScan = ()

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str,\
                    help="spécifie le répertoire à traiter")
parser.add_argument("--base", type=str,\
                    help="spécifie la raçine publique de la galerie")
parser.add_argument("-r", "--regenerate",\
                    help="force la génération complète du répertoire",\
                    action="store_true")
args = parser.parse_args()

SCRIPT_PATH = os.path.abspath(__file__)

if os.path.exists(os.path.join(SCRIPT_PATH,"config.cfg")):
    import configparser
    config = ConfigParser.ConfigParser
    config.read(os.path.join(SCRIPT_PATH,"config.cfg"))

GALLERY_PATH = args.dir if args.dir else os.path.join(SCRIPT_PATH,galleryDir)
PUBLIC_BASE = args.base.rstrip("/") if args.base else publicBase.rstrip("/")
GALLERY_DIR = os.path.basename(PUBLIC_BASE) if PUBLIC_BASE else galleryDir
TEMPLATE_PATH = os.path.join(GALLERY_PATH,templateDir)\
    if os.path.isdir(os.path.join(GALLERY_PATH,templateDir)) else templateDir

def generate(dirPath="",currentDir="",ariane="",privateBaseList="",dirs=""):
    """Set content of html templates in respective vars"""
    page = get_content(get_template_path("index.html"))\
            if os.path.exists(get_template_path("index.html")) else ""
    imageTag = get_content(get_template_path("imagetag.html"))\
            if os.path.exists(get_template_path("imagetag.html")) else ""
    directory = get_content(get_template_path("directory.html"))\
            if os.path.exists(get_template_path("directory.html")) else ""
    arianeTag = get_content(get_template_path("ariane.html"))\
            if os.path.exists(get_template_path("ariane.html")) else ""
    exifTag = get_content(get_template_path("exif.html"))\
            if os.path.exists(get_template_path("exif.html")) else ""

    dirPath = os.path.normpath(dirPath) if dirPath else GALLERY_PATH
    currentDir = currentDir if currentDir else GALLERY_DIR

    if dirPath not GALLERY_PATH:
        parentDir = directory.replace("{dirUri}","../").replace("{dirName}","..")
        after = os.path.basename(dirPath)

    """galleryBase = PUBLIC_BASE + after"""
    galleryBase = os.path.normpath(PUBLIC_BASE,after)
    fullAriane = ariane + arianeTag.replace("{dirName","{url}")\
                                   .replace(currentDir,galleryBase)

    if os.path.isdir(dirPath):
        thumbsPath = os.path.join(dirPath,thumbsDir)

        if not os.path.isdir(thumbsPath):
            os.mkdir(thumbsPath)

        with os.scandir(dirPath) as current:
            for entry in current:
                if entry.name.endswith(imagesAllowed):
                    imageList[] = entry
                elif entry.is_dir() and entry.name != noScan:
                    dirs[] = directory.replace("{dirUri",\
                                               os.path.join(galleryBase,entry)\
                                               .replace("{dirName",entry)
                """generate(os.path.join(dirPath,entry),entry,fullAriane,privateBaseList)"""

def get_content(path):
    with open(path, "r") as content_file:
        return content_file.read()

def get_template_path(file_name):
    return os.path.join(TEMPLATE_PATH,file_name)
