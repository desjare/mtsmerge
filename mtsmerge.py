#!/usr/bin/python3

import argparse
import os
import sys

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

merge_suffix = "-merged"

def run_command(cmd):
    status = os.system(cmd)
    if(status != 0):
        print("Command %s return status %d" % (cmd, status))
        sys.exit(1)

def fetch_mts_groups(path):
    groups = {}
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            fullpath = os.path.join(root,name)
            filename, ext = os.path.splitext(fullpath)
            if not "mts" in ext.lower():
                continue
            if merge_suffix in filename:
                continue

            if not filename in groups:
                groups[filename] = []
            # remove ./ from path since ffmpeg does not like them
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
        output_file = group + merge_suffix + ".mts"
        if os.path.exists(output_file):
            print("Skipping existing %s" % (output_file))
            continue
        cmd += "\" -c copy " + output_file
        print("Executing: %s" % (cmd))
        run_command(cmd)

def transcode_mts_groups(groups, encoder_args):
    for group, files in groups.items():
        input_file = group + merge_suffix + ".mts"
        output_file = group + merge_suffix + ".mp4"

        if os.path.exists(output_file):
            print("Skipping existing %s" % (output_file))
            continue

        cmd = "ffmpeg -i %s %s %s" % (input_file, encoder_args, output_file)
        print("Executing: %s" % (cmd))
        run_command(cmd)

parser = argparse.ArgumentParser(description="mtsmerge merge & transcode .mts, .mts1, .mts2, .mts3 file sequence into an mp4")
parser.add_argument("--sourcedir", type=str, default=".", help="directory where your media files are found")
parser.add_argument("--x265", default=False, action="store_true", help="transcode video in x265")
parser.add_argument("--opus", default=False, action="store_true", help="transcode audio in opus")
args = parser.parse_args()

encoder_args = ""

if args.x265 is True:
    encoder_args += " -c:v libx265 -crf 28 "

if args.opus is True:
    encoder_args += " -c:a libopus -b:a 128K "

groups = fetch_mts_groups(args.sourcedir)
merge_mts_groups(groups)
transcode_mts_groups(groups, encoder_args)