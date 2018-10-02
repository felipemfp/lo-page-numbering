#!/usr/bin/env python3

import os
import zipfile
import argparse

def zipall(ob, path, rel=""):
    basename = os.path.basename(path)
    if os.path.isdir(path):
        if rel == "":
            rel = basename
        ob.write(path, os.path.join(rel))
        for root, dirs, files in os.walk(path):
            for d in dirs:
                zipall(ob, os.path.join(root, d), os.path.join(rel, d))
            for f in files:
                ob.write(os.path.join(root, f), os.path.join(rel, f))
            break
    elif os.path.isfile(path):
        ob.write(path, os.path.join(rel, basename))
    else:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Release a new version')
    parser.add_argument('version', type=str, help='version (e.g., 0.1.0)')
    
    args = parser.parse_args()

    release = args.version.replace('.', '_')
    release_dir = 'LibreOffice/versions/{}'.format(release)

    os.makedirs(release_dir, exist_ok=True)

    files_dir = 'OpenOffice/python/oxt_metadata'
    oxt_file = '{}/PageNumberingAddon.oxt'.format(release_dir)

    with zipfile.ZipFile(oxt_file, "w") as oxt:
        for f in os.listdir(files_dir):
            zipall(oxt, os.path.join(files_dir, f))
    
    print('Release file available in {}'.format(oxt_file))