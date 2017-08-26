import os
import sys
import argparse
import re
from PIL import Image
from PIL.exifTags import TAGS

imagesAllowed = (".jpg",".png",".gif",)
galleryDir = "gallery"
templateDir = "template"
thumbsDir = "_thumbs"
thumbsPath = os.path.join(galleryDir,thumbsDir)
thumbWidth = [200]
thumbRatio = [4, 3]
publicBase = ""
noScan = ()
sort = ""

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
                    imagesList[] = entry
                elif entry.is_dir() and entry.name != noScan:
                    dirs[] = directory.replace("{dirUri",\
                                               os.path.join(galleryBase,entry)\
                                               .replace("{dirName",entry)
                """generate(os.path.join(dirPath,entry),entry,fullAriane,privateBaseList)"""

    if type(imagesList) is list:
        imagesList.sort(reverse=True) if sort = "desc" else test.sort()

def get_content(path):
    with open(path, "r") as content_file:
        return content_file.read()

def get_template_path(file_name):
    return os.path.join(TEMPLATE_PATH,file_name)

def get_image_type(image):
    with Image.open(image) as im:
        return(im.format)

def get_exif(image):
    elements = {}
    with Image.open as im:
        exif = im.getexif()
        for tag, value in exif.items():
            decoded = TAGS.get(tag,tag)
            elements = value
        return elements

def create_thumb(image,path,name):
    x,_y = image.size
    if x > y:
        hx = x / 2
        hy1 = y / 2
        hy2 = (y / 1.2) / 2 """on réduit la hauteur de 20%"""
        box = (hx - hy2, hy1 - hy2, hx + hy2, hy1 + hy2)
    elif y > x:
        hy = y / 2
        hx1 = x / 2
        hx2 = (x / 1.2) / 2
        box = (hx1 - hx2, hy - hx2, hx1 + hx2, hy + hx2)
    else:
        h1 = x / 2
        h2 = (x / 1.2) / 2
        xy1 = h1 - h2
        xy2 = h1 + h2
        box = (h1, h1, h2, h2)
    image.crop(box)
    image.save(os.path.join(path,name)
