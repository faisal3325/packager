import os
import zipfile
import shutil

import conf as conf


def main(file_path):
    # move to file_path
    os.chdir(file_path)
    files = os.listdir()

    # prepare layers
    prepareLayers(files)

    # prepare functions
    # prepareFunctions(files)


def prepareLayers(files):
    # check if module present
    if conf.module not in files:
        return

    # change to module dir
    os.chdir(conf.module)

    # get all modules
    modules = list(
        filter(lambda file: file.startswith('ER_'), os.listdir()))
    print(modules)

    # process modules
    processFile(modules, target=conf.layer_path)

    os.chdir("..")


def prepareFunctions(files):
    # check if script present
    if conf.script not in files:
        return

    # change to script dir
    os.chdir(conf.script)

    # get all scripts
    scripts = os.listdir()
    print(scripts)

    # process scripts
    processFile(scripts)

    os.chdir("..")


def filterFiles(file):
    if (file not in conf.files_to_ignore):
        return True
    else:
        return False


def processFile(files, target=None):
    # loop through each file to process
    for file in files:
        if target is None:
            target = file
        # move to file
        os.chdir(file)

        recursivelyGetFiles(file, target)

        zip(target)

        toDelete = target.split('/')[0]
        if os.path.exists(f'{toDelete}'):
            shutil.rmtree(f'{toDelete}')

        os.chdir("..")


def recursivelyGetFiles(path, target):
    # get files in path
    print(path, target)
    print(os.listdir())
    files = list(filter(lambda file: filterFiles(file), os.listdir()))
    print(files)
    # loop through all and check wether file is dir
    for file in files:
        if isDir(file):
            os.chdir(file)
            recursivelyGetFiles(file, f"{target}/{file}")
            os.chdir("..")
        else:
            copyFile(file, path, target)


def copyFile(file, path, target):
    # create target path
    if not os.path.exists(target):
        os.makedirs(target)
    shutil.copyfile(file, f"{target}/{file}")


def isDir(source):
    try:
        os.chdir(source)
        os.chdir('..')
        return True
    except Exception:
        return False


def zip(target):
    zipf = zipfile.ZipFile('python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('python/', zipf)
    zipf.close()


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


main("D:/Users/khanf/Documents/Repositories/aws_lambda")
