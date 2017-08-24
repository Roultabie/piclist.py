import os
import sys
import argparse
import re

imagePattern = "/([^.]+)\.(jpg|png|gif)/Ui"
galleryDir = "gallery"
templateDir = "template"
thumbsDir = "_thumbs"
thumbsPath = os.path.join(galleryDir,thumbsDir)
thumbWidth = [200]
thumbRatio = [4, 3]
publicBase = ""

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str, help="spécifie le répertoire à traiter")
parser.add_argument("--base", type=str, help="spécifie la raçine publique de la galerie")
parser.add_argument("-r", "--regenerate", help="force la génération complète du répertoire", action="store_true")
args = parser.parse_args()

SCRIPT_PATH = os.path.abspath(__file__)

if os.path.exists(os.path.join(SCRIPT_PATH,"/config.cfg")):
    import configparser
    config = ConfigParser.ConfigParser
    config.read(os.path.join(SCRIPT_PATH,"/config.cfg"))

GALLERY_PATH = args.dir if args.dir else os.path.join(SCRIPT_PATH,galleryDir)
PUBLIC_BASE = args.base.rstrip("/") if args.base else publicBase.rstrip("/")
GALLERY_DIR = os.path.basename(PUBLIC_BASE) if PUBLIC_BASE else galleryDir
TEMPLATE_PATH = os.path.join(GALLERY_PATH,templateDir) if os.path.isdir(os.path.join(GALLERY_PATH,templateDir)) else templateDir

print(os.path.join(GALLERY_PATH,templateDir))

def get_content(path):
    with open(path, "r") as content_file:
        content = content_file.read()

