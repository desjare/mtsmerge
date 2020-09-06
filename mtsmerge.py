#!/usr/bin/python3

import argparse
import os
import sys

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")

merge_suffix = "-merged"
output_ext = ".mp4"

def run_command(cmd):
	status = os.system(cmd)
	if(status != 0):
		print("Error: running command: %s" % (cmd, ))
		print("Error: return status: %d" % (status))
		print("Exiting...")
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

def build_input_args(groups):
	groups_args = {}
	for group, files in groups.items():
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

def merge_mts_groups(groups, output_dir):

	print("Merging mts")

	groups_input_args = build_input_args(groups)
	for group, files in groups.items():
		if len(files) < 2:
			print("Skipping: not enought files to merge %s" % ("".join(files)))
			continue

		cmd = "ffmpeg %s " % (groups_input_args[group])

		group_output = group
		if output_dir is not None:
			group_output = os.path.join(output_dir, os.path.basename(group))

		output_file = group_output + merge_suffix + ".mts"
		if os.path.exists(output_file):
			print("Warning: skipping existing %s" % (output_file))
			continue

		cmd += " -c copy \"%s\" " % (output_file)
		print("Running: %s" % (cmd))
		run_command(cmd)

def transcode_mts_groups(groups, output_dir, use_intermediate, encoder_args):

	print("Transcoding mts")

	# build concat command if we are not using intermediate file
	if use_intermediate is False:
		groups_input_args = build_input_args(groups)

	for group, files in groups.items():

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
			print("Warning: skipping existing %s" % (output_file))
			continue

		cmd = "ffmpeg %s %s \"%s\"" % (input_args, encoder_args, output_file)
		print("Running: %s" % (cmd))
		run_command(cmd)

parser = argparse.ArgumentParser(description="mtsmerge merge & transcode .mts, .mts1, .mts2, .mts3 file sequence into an mp4 or mkv")
parser.add_argument("--inputdir", type=str, default=".", dest="input_dir", help="directory where your media files are found")
parser.add_argument("--outputdir", type=str, default=None, dest="output_dir", help="directory where your media files are outputted")
parser.add_argument("--x265", default=False, action="store_true", help="transcode video in x265")
parser.add_argument("--opus", default=False, action="store_true", help="transcode audio in opus")
parser.add_argument("--useintermediate", default=False, action="store_true", dest="use_intermediate", help="use an intermediate mts file")
args = parser.parse_args()

encoder_args = ""

if args.x265 is True:
	encoder_args += ' -c:v libx265 -crf 28 ' 

if args.opus is True:
	encoder_args += ' -c:a libopus -b:a 256K -af "channelmap=channel_layout=5.1" '
	output_ext = ".mkv"

if args.output_dir is not None:
	os.makedirs(args.output_dir, exist_ok=True)

groups = fetch_mts_groups(args.input_dir)

if args.use_intermediate is True:
	merge_mts_groups(groups, args.output_dir)

transcode_mts_groups(groups, args.output_dir, args.use_intermediate, encoder_args)