import os
from pathlib import Path
import shutil

PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

def create_folder(path):
    os.makedirs(path)

def get_student_pic_path(instance, filename):
    return os.path.join("%s" % 'student_galleries', instance.student_gallery.student.user.username, filename)
