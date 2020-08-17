# mtsmerge

mtsmerge.py: PVR output MTS merge and transcode utility script

This script is meant to be use by people with little prior knowledge of media files, transcoding, etc. It is meant to be simple to use but requires use of command line.

This script is used to convert MTS files that are outputted from my PVR to mp4. MTS stands for MPEG Transport Stream. An MTS file is a video saved in the Advanced Video Coding High Definition [AVCHD](https://en.wikipedia.org/wiki/AVCHD) format. 

PVR sometimes uses older filesystem that supports only 4GB files and can split you media into several files. This is not very practical to watch a movie so I wrote this script. Storing media in [AVCHD](https://en.wikipedia.org/wiki/AVCHD) is also taking a lot of disk space. Converting them to another format for storage is useful.

The script simply merge file sequences (.mts, .mts1, .mts2, .mts3) of files having the same file name. Then, it convert it to mp4. It does it all using [ffmpeg](https://ffmpeg.org/). 

For example, if you have a folder with:

* CIVM-HD-08122020-0900PM.mts   
* CIVM-HD-08122020-0900PM.mts2
* CIVM-HD-08122020-0900PM.mts1 
* CIVM-HD-08122020-0900PM.mts3

it will convert it to:
* CIVM-HD-08122020-0900PM-merged.mp4

The script won't delete or cleanup your files.

**Usage:**

For help:
python3 mtsmerge.py -h

Exxamples:
* python3 mtsmerge.py (from your current mts directory)
* python3 mtsmerge.py --sourcedir <media folder> 
* python3 mtsmerge.py --x265 (encoding with newer codec)

**Encoding examples**

1h57:00 1920x1080 HD movie MTS from my PVR with 5.1 ac3 384 kb/s audio

| Codec | File Size | mtsmerge.py Options | Encoding Speed |
--- | --- | --- | --- |
| [AVCHD](https://en.wikipedia.org/wiki/AVCHD) (original file) | 16.7GB | N/A | N/A
| [h264](https://en.wikipedia.org/wiki/Advanced_Video_Coding) (default) | 4.26GB | default | Fast |
| [h265](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding)  | 1.4GB | --x265 | Slow |


**Requirements**
* [python3](https://www.python.org/) (tested with python 3.6.9)
* [ffmpeg](https://ffmpeg.org/) in your path

**Tested**
* Tested with [Mediasonic ATSC Digital Converter Box with Recording/Media Player/TV Tuner Function (HW130STB)](https://www.amazon.ca/-/fr/gp/product/B01EW098XS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) MTS output.

**Bugs & Notes**

The current implementation transcodes the AVCHD to h264 and does an audio passthrough. You can use h225 using --x265. The script merges the files to a single mts file before transcoding. This should not be necessary. It is also fairly simple to modify it and add parameters to use other codecs like HEVC, opus, etc. I welcome any contribution. 


