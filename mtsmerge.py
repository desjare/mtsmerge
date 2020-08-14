#!/usr/bin/python3

import os
import sys

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

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
            groups[filename] += [fullpath.replace("./","")]

    sortedgroups = {}
    for group, files in groups.items():
        sortedgroups[group] = sorted(files)

    return sortedgroups

def merge_mts_groups(groups):
    for group, files in groups.items():
        cmd = "ffmpeg -i \"concat:"
        is_first = True
        for path in files:
            if is_first is True:
                cmd += path
                is_first = False
            else:
                cmd += "|" + path
        output_file = group + "-merged.mts"
        if os.path.exists(output_file):
            print("Skipping existing %s" % (output_file))
            continue
        cmd += "\" -c copy " + output_file
        print("Executing: %s" % (cmd))
        os.system(cmd)

def transcode_mts_groups(groups):
    for group, files in groups.items():
        input_file = group + "-merged.mts"
        output_file = group + "-merged.mp4"

        if os.path.exists(output_file):
            print("Skipping existing %s" % (output_file))
            continue

        cmd = "ffmpeg -i %s %s" % (input_file, output_file)
        print("Executing: %s" % (cmd))
        os.system(cmd)

groups = fetch_mts_groups(".")
merge_mts_groups(groups)
transcode_mts_groups(groups)

