# mtsmerge

mtsmerge.py utility script

This script is used to convert MTS files that are outputted from my pvr to mp4. mts stands for MPEG Transport Stream. An MTS file is a video saved in the Advanced Video Coding High Definition (AVCHD) format.

The script simply merge file sequences (mts, mts1, mts2, mts3) of files having the same file name. Then, it convert it to mp4. It does it all using [ffmpeg](https://ffmpeg.org/) 

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

or

python3 mtsmerge.py --sourcedir <media folder> 

**Requirements**
* [python3](https://www.python.org/) (tested with python 3.6.9)
* [ffmpeg](https://ffmpeg.org/) in your path

**Tested**
* Tested with [Mediasonic ATSC Digital Converter Box with Recording/Media Player/TV Tuner Function (HW130STB)](https://www.amazon.ca/-/fr/gp/product/B01EW098XS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) MTS output.



