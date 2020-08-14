

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
        output_file = group + "-merged.mts"
        if os.path.exists(output_file):
            print("Skipping existing %s" % (output_file))
            continue
        cmd += "\" -c copy " + output_file
        print("Executing: %s" % (cmd))
        os.system(cmd)

        break

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

        break


groups = fetch_mts_groups(".")
merge_mts_groups(groups)
transcode_mts_groups(groups)

