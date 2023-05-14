import os
from pathlib import Path
import shutil

PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

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

def get_lecture_file_path(instance, filename):
    return os.path.join("%s" % 'educational_tapes', instance.course.code_name, 'lectures', filename)

def get_task_file_path(instance, filename):
    return os.path.join("%s" % 'educational_tapes', instance.task_attempt.task.course.code_name, 'tasks', instance.task_attempt.task.code_name, instance.task_attempt.student.user.username, filename)

def get_test_file_path(instance, filename):
    filename = f'{get_transliteration(instance.name)}.json'
    return os.path.join("%s" % 'educational_tapes', instance.course.code_name, 'tests', get_transliteration(instance.name), filename)

def get_test_attempt_file_path(instance, filename):
    filename = f'{instance.test.name}.json'
    return os.path.join("%s" % 'educational_tapes', instance.test.course.code_name, 'tests', get_transliteration(instance.test.name), instance.student.user.username, get_transliteration(filename))

def remove_folder(path):
    if os.path.isdir(path): Path(os.path.join(path)).rmdir()

def remove_tree(path):
    if os.path.isdir(path): shutil.rmtree(path)

def create_folder(path):
    os.makedirs(path)