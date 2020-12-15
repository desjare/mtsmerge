#!/usr/bin/python3
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
"""
mtsmerge utility script to convert MTS files that are outputted from my PVR
to mp4 or mkv.
"""
import argparse
import os
import sys
import logging

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

DEFAULT_MERGE_SUFFIX = "-merged"
DEFAULT_OUTPUT_EXT = ".mp4"

infos = []
errors = []
warnings = []

def handle_info(info):
    """
    log and keep track of info log messages
    """
    infos.append(info)
    logging.info(info)

def handle_warning(warning):
    """
    log and keep track of info warning messages
    """
    warnings.append(warning)
    logging.warning(warning)

def handle_error(error):
    """
    log and keep track of info warning messages
    """
    errors.append(error)
    logging.error(error)

def print_summary():
    """
    print a summary of work that has been done
    """
    print("Summary: ")

    print("\n".join(infos))
    print("")

    print("Warnings:")
    print("\n".join(warnings))
    print("")

    print("Errors:")
    print("\n".join(errors))
    print("")

def run_command(cmd:str) -> bool:
    """
    run a command using os.system on the shell
    """
    handle_info("Running: %s" % (cmd))
    status = os.system(cmd)
    if status != 0:
        handle_error("Error: running command: %s" % (cmd, ))
        handle_error("Error: return status: %d" % (status))
        return False
    return True

def fetch_mts_groups(path:str, merge_suffix:str) -> dict:
    """
    walk a path a return a directory with grouped mts files by name
    """
    mts_groups = {}
    for root, _, files in os.walk(path, topdown=False):
        for name in files:
            fullpath = os.path.join(root,name)
            filename, ext = os.path.splitext(fullpath)
            if not "mts" in ext.lower():
                continue
            if merge_suffix in filename:
                continue

            if not filename in mts_groups:
                mts_groups[filename] = []
            # remove ./ from path since ffmpeg does not like them
            mts_groups[filename] += [fullpath.replace("./","")]

    sortedgroups = {}
    for group, files in mts_groups.items():
        sortedgroups[group] = sorted(files)

    return sortedgroups

def build_input_args(mts_groups:dict) -> dict:
    """
    build ffmpeg input arguments based on mts_groups directory
    """
    groups_args = {}
    for group, files in mts_groups.items():
        if len(files) > 1:
            cmd = " -i \"concat:"
        else:
            cmd = " -i \""

        is_first = True
        for path in files:
            if is_first is True:
                cmd += path
                is_first = False
            else:
                cmd += "|" + path
        cmd += "\" "
        groups_args[group] = cmd

    return groups_args

def merge_mts_groups(mts_groups:dict, output_dir:str, merge_suffix:str):
    """
    merge mts files together into merged mts
    """
    handle_info("Merging mts")

    groups_input_args = build_input_args(mts_groups)
    for group, files in mts_groups.items():
        if len(files) < 2:
            handle_warning("Skipping: not enought files to merge %s" % ("".join(files)))
            continue

        cmd = "ffmpeg %s " % (groups_input_args[group])

        group_output = group
        if output_dir is not None:
            group_output = os.path.join(output_dir, os.path.basename(group))

        output_file = group_output + merge_suffix + ".mts"
        if os.path.exists(output_file):
            handle_warning("Warning: skipping existing %s" % (output_file))
            continue

        cmd += " -c copy \"%s\" " % (output_file)

        run_command(cmd)

def transcode_mts_groups(mts_groups:dict, output_dir:str, output_ext:str, use_intermediate:dict, merge_suffix:str, encoder_args:str):
    """
    transcode mts files into the output directory
    """
    handle_info("Transcoding mts")

    # build concat command if we are not using intermediate file
    if use_intermediate is False:
        groups_input_args = build_input_args(mts_groups)

    for group, files in mts_groups.items():

        group_merge_suffix = merge_suffix
        if len(files) < 2:
            group_merge_suffix = ""

        if use_intermediate is True:
            group_input = group
            input_args = " -i \"%s\"" % (group_input + group_merge_suffix + ".mts")
        else:
            input_args = groups_input_args[group]

        group_output = group
        if output_dir is not None:
            group_output = os.path.join(output_dir, os.path.basename(group))

        output_file = group_output + group_merge_suffix + output_ext

        if os.path.exists(output_file):
            handle_warning("Warning: skipping existing %s" % (output_file))
            continue

        cmd = "ffmpeg %s %s \"%s\"" % (input_args, encoder_args, output_file)
        run_command(cmd)

def main():
    """
    script entry point
    """
    parser = argparse.ArgumentParser(description="mtsmerge merge & transcode .mts, .mts1, .mts2, .mts3 file sequence into an mp4 or mkv")
    parser.add_argument("--inputdir", type=str, default=".", dest="input_dir", help="directory where your media files are found")
    parser.add_argument("--outputdir", type=str, default=None, dest="output_dir", required=True, help="directory where your media files are outputted")
    parser.add_argument("--default-map", default=True, dest="default_map", action="store_false", help="map all streams by default")
    parser.add_argument("--audio-track", type=int, default=None, dest="audio_track", help="which audio track to transcode (1 or 2 or 3, etc.)")
    parser.add_argument("--x265", default=False, action="store_true", help="transcode video in x265 in a mkv container")
    parser.add_argument("--opus", default=False, action="store_true", help="transcode audio in opus in a mkv container")
    parser.add_argument("--useintermediate", default=False, action="store_true", dest="use_intermediate", help="use an intermediate mts file")
    args = parser.parse_args()

    # setup logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # set formatter
    console_handler.setFormatter(formatter)

    # add console handler
    logger.addHandler(console_handler)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    encoder_args = ""

    output_ext = DEFAULT_OUTPUT_EXT
    merge_suffix = DEFAULT_MERGE_SUFFIX

    if args.audio_track is not None:
        encoder_args += " -map 0:0 -map 0:%d " % (args.audio_track)
    elif args.default_map is True:
        encoder_args += " -map 0 "

    if args.x265 is True:
        encoder_args += ' -c:v libx265 -crf 24 '
        output_ext = ".mkv"

    if args.opus is True:
        encoder_args += ' -c:a libopus -b:a 256K -af "channelmap=channel_layout=5.1" '
        output_ext = ".mkv"

    if args.output_dir is not None:
        os.makedirs(args.output_dir, exist_ok=True)

    groups = fetch_mts_groups(path=args.input_dir, merge_suffix=merge_suffix)

    if args.use_intermediate is True:
        merge_mts_groups(mts_groups=groups, output_dir=args.output_dir, merge_suffix=merge_suffix)

    transcode_mts_groups(mts_groups=groups,
        output_dir=args.output_dir,
        output_ext=output_ext,
        use_intermediate=args.use_intermediate,
        merge_suffix=merge_suffix,
        encoder_args=encoder_args)

main()
