import os
import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS

images_allowed = (".jpg",".jpeg",".png",".gif",)
gallery_dir = "gallery"
template_dir = "template"
thumbs_dir = "_thumbs"
thumbs_path = os.path.join(gallery_dir,thumbs_dir)
thumbs_width = (200, 200)
public_base = ""
no_scan = ("_template")
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

GALLERY_PATH = args.dir if args.dir else os.path.join(SCRIPT_PATH,gallery_dir)
PUBLIC_BASE = args.base.rstrip(os.path.sep) if args.base else public_base
GALLERY_DIR = os.path.basename(PUBLIC_BASE) if PUBLIC_BASE else gallery_dir
TEMPLATE_PATH = os.path.join(GALLERY_PATH,template_dir)\
    if os.path.isdir(os.path.join(GALLERY_PATH,template_dir)) else template_dir
SUB_DIRS = GALLERY_PATH.split(GALLERY_DIR)[1].split(os.path.sep)
SUB_DIRS.insert(0,GALLERY_DIR)
SUB_DIRS = list(filter(None,SUB_DIRS))

def generate(dir_path="",current_dir="",ariane="",private_base_list="",dirs=""):

    """Set content of html templates in respective vars"""
    page = get_content(get_template_path("index.html"))\
            if os.path.exists(get_template_path("index.html")) else ""
    image_tag = get_content(get_template_path("imagetag.html"))\
            if os.path.exists(get_template_path("imagetag.html")) else ""
    directory = get_content(get_template_path("directory.html"))\
            if os.path.exists(get_template_path("directory.html")) else ""
    ariane_tag = get_content(get_template_path("ariane.html"))\
            if os.path.exists(get_template_path("ariane.html")) else ""
    exif_tag = get_content(get_template_path("exif.html"))\
            if os.path.exists(get_template_path("exif.html")) else ""

    dir_path = os.path.normpath(dir_path) if dir_path else GALLERY_PATH
    dir_path = dir_path.rstrip(os.path.sep)
    current_dir = os.path.basename(dir_path)
    dirs = []
    if len(SUB_DIRS) > 1:
        ariane = []
        nb_back = len(SUB_DIRS) - 1
        for element in SUB_DIRS:
            ariane.append(ariane_tag.replace("{dirName}",element)\
                                   .replace("{url}","../" * nb_back))
            nb_back -= 1
        dirs.append(directory.replace("{dirUri}","../")\
                          .replace("{dirName}",".."))
    else:
        ariane = [ariane_tag.replace("{dirName}",GALLERY_DIR)\
                            .replace("{url}","")]

    if os.path.isdir(dir_path):
        thumbs_path = os.path.join(dir_path,thumbs_dir)

        if not os.path.isdir(thumbs_path):
            os.mkdir(thumbs_path)

        images_list = []

        with os.scandir(dir_path) as current:
            for entry in current:
                if entry.name.endswith(images_allowed):
                    images_list.append(entry.name)
                elif entry.is_dir()\
                        and entry.name != no_scan\
                        and entry.name != thumbs_dir:
                    dirs.append(\
                          directory.replace("{dirUri}",\
                                        os.path.join(entry.name))\
                                   .replace("{dirName}",entry.name))

    if type(images_list) is list:
        image_tags = []
        images_list.sort(reverse=True) if sort == "desc" else images_list.sort()
        for image in images_list:
            with Image.open(os.path.join(dir_path,image)) as i:
                if i.format == "JPEG":
                    exif_datas = exif_tag
                    elements = {}
                    if hasattr(i,"_getexif"):
                        exif = i._getexif()
                        for tag, value in exif.items():
                            decoded = TAGS.get(tag,tag)
                            if type(value) is str:
                                exif_datas = exif_datas.replace(\
                                            "{" + decoded + "}",value)
                        exif_string = exif_datas
                else:
                    exif_string = ""
                image_attr = {"base_name": image,\
                             "name": os.path.splitext(image),\
                             "path": dir_path}
                image_comment = ""
                if not os.path.isfile(os.path.join(dir_path,thumbs_dir,image))\
                   or args.regenerate:
                    create_thumb(i,image_attr)
                image_tags.append(image_tag\
                            .replace("{thumbUri}",\
                                os.path.join(thumbs_dir, image))\
                            .replace("{thumbsWidth}",str(thumbs_width[0]))\
                            .replace("{thumbHeight}",str(thumbs_width[1]))\
                            .replace("{imageUri}",image)\
                            .replace("{imageWidth}",str(i.size[0]))\
                            .replace("{height}",str(i.size[1]))\
                            .replace("{imageComment}",image_comment)\
                            .replace("{imageExif}",exif_string))

        comment = get_content(get_template_path("comment.html"))\
            if os.path.exists(get_template_path("comment.html")) else ""
        images = "\n".join(image_tags) if type(image_tags) is list else ""
        sub_dirs = "\n".join(dirs) if type(dirs) is list else ""
        page = page.replace("{galleryPath}",PUBLIC_BASE)\
                   .replace("{images}",images)\
                   .replace("{subDirs}",sub_dirs)\
                   .replace("{ariane}", "".join(ariane))\
                   .replace("{currentDir}",current_dir)\
                   .replace("{comment}",comment)

        with open(os.path.join(dir_path,"index.html"),"w") as file:
            file.write(page)
            file.close

def get_content(path):
    """Return content of wanted file"""
    with open(path, "r") as content_file:
        return content_file.read()

def get_template_path(file_name):
    """Concat template path and file"""
    return os.path.join(TEMPLATE_PATH,file_name)

def create_thumb(image,attr):
    """Create square thumbs from the middle of picture"""
    x,y = image.size
    if x > y:
        hx = x / 2
        hy1 = y / 2
        hy2 = (y / 1.2) / 2
        """on réduit la hauteur de 20%"""
        box = (hx - hy2, hy1 - hy2, hx + hy2, hy1 + hy2)
        thumb = image.crop(box)
    elif y > x:
        hy = y / 2
        hx1 = x / 2
        hx2 = (x / 1.2) / 2
        box = (hx1 - hx2, hy - hx2, hx1 + hx2, hy + hx2)
        thumb = image.crop(box)
    else:
        thumb = image
    thumb.thumbnail(thumbs_width)
    thumbUri = os.path.join(attr["path"],thumbs_dir,attr["base_name"])
    thumb.save(thumbUri,image.format)

generate()
