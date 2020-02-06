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
    prepareFunctions(files)


def prepareLayers(files):
    # check if module present
    if conf.module not in files:
        return

    # change to module dir
    os.chdir(conf.module)

    # get all modules
    modules = list(
        filter(lambda file: file.startswith('ER_'), os.listdir()))

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
        _target = target
        if target is None:
            _target = file
        # move to file
        os.chdir(file)

        recursivelyGetFiles(file, _target)

        targetFolder = _target.split('/')[0]
        zip(targetFolder)

        if os.path.exists(f'{targetFolder}'):
            shutil.rmtree(f'{targetFolder}')

        os.chdir("..")


def recursivelyGetFiles(path, target, recur=0):
    # get files in path
    files = list(filter(lambda file: filterFiles(file), os.listdir()))
    # loop through all and check wether file is dir
    for file in files:
        if isDir(file):
            os.chdir(file)
            recursivelyGetFiles(file, f"{target}/{file}", recur + 1)
            os.chdir("..")
        else:
            copyFile(file, path, target, recur)


def copyFile(file, path, target, recur):
    # create target path
    backtrack = ''
    if recur > 0:
        for i in range(0, recur):
            backtrack = f"{backtrack}../"

    if not os.path.exists(f"{backtrack}{target}"):
        os.makedirs(f"{backtrack}{target}")
    shutil.copyfile(file, f"{backtrack}{target}/{file}")


def isDir(source):
    try:
        os.chdir(source)
        os.chdir('..')
        return True
    except Exception:
        return False


def zip(target):
    zipf = zipfile.ZipFile(f'{target}.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(f'{target}/', zipf)
    zipf.close()


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


main("D:/Users/khanf/Documents/Repositories/aws_lambda")
