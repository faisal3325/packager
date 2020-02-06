import os
import zipfile
import shutil
from distutils.dir_util import copy_tree

import conf as conf


def main(file_path):
    os.chdir(file_path)
    curr_dir = os.listdir()

    # prepare layers
    # hookUpLayers(curr_dir)

    # prepare functions
    hookUpFunctions(curr_dir)


def hookUpFunctions(curr_dir):
    print(curr_dir)
    if conf.scripts in curr_dir:
        os.chdir(conf.scripts)
        scripts_dirs = os.listdir()

    # print(scripts_dirs)

    for dir in scripts_dirs:
        if dir in conf.scripts_second_level:
            os.chdir(dir)
            content = filter(filterFiles, os.listdir())
            scripts_dirs.extend(
                list(map(lambda a: f"{dir}/{a}", list(content))))
            try:
                scripts_dirs.remove(dir)
            except Exception:
                pass
            os.chdir("..")

    print(scripts_dirs)

    for dir in scripts_dirs:
        os.chdir(dir)

        curr = dir.split('/')
        curr.reverse()
        curr = curr[0]

        if os.path.exists(f'{curr}.zip'):
            os.remove(f'{curr}.zip')

        if os.path.exists(f'{curr}'):
            shutil.rmtree(f'{curr}')

        content = list(filter(filterFiles, os.listdir()))

        # if not os.path.exists(curr):
        #     os.makedirs(curr)

        print('content', content)

        for file in content:
            if isdir(file):
                print(file)
                copy_tree(file, f"{os.curdir}/{dir}/{file}")
            else:
                print(file)
                shutil.copyfile(file, f"{os.curdir}/{dir}")

        print('done')

        zipf = zipfile.ZipFile(f'{curr}.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(f'{curr}/', zipf)
        zipf.close()

        os.rmdir(curr)

        os.chdir("..")

        if '/' in dir:
            os.chdir("..")


def hookUpLayers(curr_dir):
    print(curr_dir)
    if conf.modules in curr_dir:
        os.chdir(conf.modules)
        modules_dirs = os.listdir()

    for dir in modules_dirs:
        os.chdir(dir)
        content = filter(filterFiles, os.listdir())

        if not os.path.exists(conf.layer_path):
            os.makedirs(conf.layer_path)

        for file in list(content):
            if file == 'python':
                continue
            shutil.copyfile(file, f"{os.curdir}/{conf.layer_path}/{file}")

        zipf = zipfile.ZipFile('python.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('python/', zipf)
        zipf.close()

        os.chdir("..")


def filterFiles(file):
    if (file not in conf.files_to_ignore):
        return True
    else:
        return False


def isdir(source):
    try:
        os.chdir(source)
        os.chdir('..')
        return True
    except Exception:
        return False


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


main("D:/Users/khanf/Documents/Repositories/aws_lambda")
