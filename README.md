# mtsmerge

mtsmerge.py utility script

This script is used to convert MTS files that are outputted from my pvr to mp4. mts stands for MPEG Transport Stream. An MTS file is a video saved in the Advanced Video Coding High Definition (AVCHD) format. 

PVR sometimes uses older filesystem that supports only 4GB files and can split you media into several files. This is not very practical to watch a movie so I wrote this script.

The script simply merge file sequences (mts, mts1, mts2, mts3) of files having the same file name. Then, it convert it to mp4. It does it all using [ffmpeg](https://ffmpeg.org/). 

For example, if you have a folder with:

* CIVM-HD-08122020-0900PM.mts   
* CIVM-HD-08122020-0900PM.mts2
* CIVM-HD-08122020-0900PM.mts1 
* CIVM-HD-08122020-0900PM.mts3

it will convert it to:
* CIVM-HD-08122020-0900PM-merged.mp4

The script won't delete or cleanup your files.

**Usage:**

python3 mtsmerge.py from your mts directory

* python3 mtsmerge.py --help for options
* python3 mtsmerge.py --sourcedir <media folder> 

You can use --x265 for encoding video in HEVC/H.2265 but you will need a chromecast ultra is you plan to use a chromecast with your video.

You can use --opus for encoding audio in opus. The file will be saved as an .mkv extension since .mp4 does not support opus. Opus is supported by chromecast 3rd generation.

**Requirements**
* [python3](https://www.python.org/) (tested with python 3.6.9)
* [ffmpeg](https://ffmpeg.org/) in your path

**Tested**
* Tested with [Mediasonic ATSC Digital Converter Box with Recording/Media Player/TV Tuner Function (HW130STB)](https://www.amazon.ca/-/fr/gp/product/B01EW098XS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) MTS output.

**Bugs & Notes**

The current implementation transcode the AVCHD to h264 and does an audio passthrough by default. It merge the files to a single mts file before transcoding. This should not be necessary. It is also fairly simple to modify it and add parameters to use other codec configurations like HEVC, opus, etc. I welcome any contribution. 


