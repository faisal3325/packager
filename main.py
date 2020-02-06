import os
import zipfile
import shutil

import conf as conf


def main(file_path):
    os.chdir(file_path)
    curr_dir = os.listdir()
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
            print(file)
            shutil.copyfile(file, f"{os.curdir}/{conf.layer_path}/{file}")
            print(f"{os.curdir}/{conf.layer_path}/{file}")
            # shutil.copy(file, f"{os.curdir}/{conf.layer_path}/{file}")

        zipf = zipfile.ZipFile('python.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('python/', zipf)
        zipf.close()

        os.chdir("..")


def filterFiles(file):
    if (file not in conf.files_to_ignore):
        return True
    else:
        return False


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


main("D:/Users/khanf/Documents/Repositories/aws_lambda")
