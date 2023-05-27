import os
import hashlib
import sys


def get_data(project, manifest):
    """
    obtain WSIs
    :param project: sub-project abb
    :param manifest: nanifest file
    :return: None
    """
    cmd = "gdc-client download -m " + manifest + " -d ../Data/" + project
    os.system(cmd)


def check_md5(file):
    """
    check md5
    :param file: check file
    :return: hash
    """
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def check(MANIFEST_NAME, BASE_DATA_DIR):
    """
    check each WSIs
    :param MANIFEST_NAME: manifest
    :param BASE_DATA_DIR: dirs
    :return: None
    """
    with open(MANIFEST_NAME) as f:
        next(f)
        for each in f:
            # print(each)
            tem = each.strip().split("\t")
            file = os.path.join(BASE_DATA_DIR, tem[0], tem[1])
            if not os.path.isfile(file):
                print(f"exist error: {file}")
            if tem[2] != check_md5(file):
                print("MD5 does not match manifest")
            else:
                print("MD5 matching")


def run(manifest_dir):
    """
    obtain WSIs
    :param manifest_dir: abs path of manifest
    :return: None
    """
    # manifest_dir = "/home/bio1/workdata/Benchmark_WSI/Benchmark/manifest"
    os.chdir(manifest_dir)
    BASE_DIR = os.path.abspath(os.path.join(manifest_dir, ".."))

    for line in os.listdir(manifest_dir):
        project = line.strip().split('_')[2].replace(".txt", "")
        print(f"Start download WSI of {project} sub-project")
        # mkdir for each project
        save_dir = os.path.join(BASE_DIR, "Data", project)
        os.makedirs(save_dir, exist_ok=True)
        manifest = os.path.join(line)
        # retrieve WSIs by gdc
        get_data(project, manifest)
        print("Download completed")
        # check md5
        check(line, save_dir)
        print("Check complected")
    print("Retrieve WSIs finished")


if __name__ == '__main__':
    # run("/home/bio1/workdata/Benchmark_WSI/Benchmark/manifest")
    manifest = sys.argv[1]
    run(manifest)
