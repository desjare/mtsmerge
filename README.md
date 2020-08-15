# mtsmerge

mtsmerge.py utility script

This script is used to convert Mediasonic HW130STB mts files to mp4. It requires ffmpeg. It simply merge file sequences (mts, mts1, mts2, mts3) of files having the same file name. Then, it convert it to mp4.

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

** Requirements **
* python3 (tested with python 3.6.9)
* ffpmeg in your path



