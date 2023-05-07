import os
from pathlib import Path
import shutil
from io import BytesIO
from PIL import Image
from django.core.files import File

PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

PIC_SIZE_RESTR = 5242880

def transliterate(string):
    char_dict = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', ',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}
    
    for key in char_dict:
        string = string.replace(key, char_dict[key])
    return string

def get_transliteration(title):
    return transliterate(title.lower())

def create_folder(path):
    os.makedirs(path)

def get_student_pic_path(instance, filename):
    return os.path.join("%s" % 'student_galleries', instance.student_gallery.student.user.username, filename)

def get_public_pic_path(instance, filename):
    return os.path.join("%s" % 'public_galleries', instance.public_gallery.code_name, filename)

def remove_folder(path):
    if os.path.isdir(path): Path(os.path.join(path)).rmdir()

def image_compress(img):
    conv_image = Image.open(img)
    image_io = BytesIO()
    conv_image.save(image_io, 'JPEG', quality=100, subsampling=0)
    res = File(image_io, name=img.name)
    return res