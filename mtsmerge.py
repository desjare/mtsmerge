

#ffmpeg -i "concat:00000.MTS|00001.MTS|00002.MTS" -c copy output.mts

import os

def fetch_mts_groups(path):
    groups = {}
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            fullpath = os.path.join(root,name)
            filename, ext = os.path.splitext(fullpath)
            if not "mts" in ext.lower():
                continue

            if not filename in groups:
                groups[filename] = []
            groups[filename] += [fullpath]

    sortedgroups = {}
    for group, files in groups.items():
        sortedgroups[group] = sorted(files)

    return sortedgroups

def merge_mts_groups(groups):
    for group, files in groups.items():
        cmd = "ffmpeg -i \"concat:"
        for path in files:
            cmd += "|" + path
        cmd += "\" -c copy " + group + ".mts"

        print(cmd)


groups = fetch_mts_groups(".")
merge_mts_groups(groups)

