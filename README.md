# mtsmerge.py: PVR output MTS merge and transcode utility script

## Intended audience 
This script is meant to be used by people with little prior knowledge of media files, transcoding, etc. It is meant to be simple to use but requires the use of the command line.

## Description
This script is used to convert MTS files that are outputted from my PVR to mp4. MTS stands for MPEG Transport Stream. An MTS file is a video saved in the Advanced Video Coding High Definition [AVCHD](https://en.wikipedia.org/wiki/AVCHD) format. 

PVR sometimes uses an older filesystem that supports only 4GB files and can split your media into several files. This is not very practical to watch a movie so I wrote this script. Storing media in [AVCHD](https://en.wikipedia.org/wiki/AVCHD) is also taking a lot of disk space. Converting them to another format for storage is useful.

The script simply merge file sequences (.mts, .mts1, .mts2, .mts3) of files having the same file name. Then, it converts it to mp4. It does it all using [ffmpeg](https://ffmpeg.org/). 

For example, if you have a folder with:

* CIVM-HD-08122020-0900PM.mts   
* CIVM-HD-08122020-0900PM.mts2
* CIVM-HD-08122020-0900PM.mts1 
* CIVM-HD-08122020-0900PM.mts3

it will convert it to:
* CIVM-HD-08122020-0900PM-merged.mp4

The script won't delete or clean up your files.

## Usage

For help:
python3 mtsmerge.py -h

Exxamples:
* python3 mtsmerge.py (from your current mts directory)
* python3 mtsmerge.py --sourcedir <media folder> 
* python3 mtsmerge.py --x265 (encoding with newer codec [HEVC/H.265](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding) video )
* python3 mtsmerge.py --x265 --opus (encoding with newer codec [HEVC/H.265](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding) & [opus](https://opus-codec.org/) audio)

You can use --x265 for encoding video in HEVC/H.265 but you will need a **chromecast ultra** is you plan to use a chromecast with your video.

You can use --opus for encoding audio in [opus](https://opus-codec.org/). The file will be saved as an .mkv extension since .mp4 does not support opus. Opus is supported by chromecast 3rd generation.

**Encoding examples**

1h57:00 1920x1080 HD movie MTS from my PVR with 5.1 ac3 384 kb/s audio

| Codec | File Size | mtsmerge.py Options | Encoding Speed |
--- | --- | --- | --- |
| [AVCHD](https://en.wikipedia.org/wiki/AVCHD) (original file) | 16.7GB | N/A | N/A
| [h264](https://en.wikipedia.org/wiki/Advanced_Video_Coding) (default) | 4.26GB | default | Fast |
| [h265](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding)  | 1.4GB | --x265 | Slow |
| [h265](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding) & [opus](https://opus-codec.org/)  | 1.4GB | --x265 --opus | Slower |

## Requirements
* [python3](https://www.python.org/) (tested with python 3.6.9)
* [ffmpeg](https://ffmpeg.org/) in your path

I prepared a tutorial video to learn how to do that on windowws 10:

https://youtu.be/G-Qb_BKxm0g

## Tested
* Tested with [Mediasonic ATSC Digital Converter Box with Recording/Media Player/TV Tuner Function (HW130STB)](https://www.amazon.ca/-/fr/gp/product/B01EW098XS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) MTS output.

## Bugs & Notes

The current implementation transcode the AVCHD to h264 and does an audio passthrough by default. It merge the files to a single mts file before transcoding. This should not be necessary. It is also fairly simple to modify it and add parameters to use other codec configurations like HEVC, opus, etc. I welcome any contribution. 


