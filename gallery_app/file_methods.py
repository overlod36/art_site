import os
from pathlib import Path
import shutil
from io import BytesIO
from PIL import Image
from django.core.files import File

PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

PIC_SIZE_RESTR = 5242880

def create_folder(path):
    os.makedirs(path)

def get_student_pic_path(instance, filename):
    return os.path.join("%s" % 'student_galleries', instance.student_gallery.student.user.username, filename)

def remove_folder(path):
    if os.path.isdir(path): Path(os.path.join(path)).rmdir()

def image_compress(img):
    conv_image = Image.open(img)
    image_io = BytesIO()
    conv_image.save(image_io, 'JPEG', quality=100, subsampling=0)
    res = File(image_io, name=img.name)
    return res