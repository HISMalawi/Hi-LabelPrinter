# Introduction
This scripts helps to detect zpl files inside the downloads folder 
and pushes them to a label printer.

The system detects files with extension `.raw.z64.zpl` created by a
browser app that generates zpl commands.

# Requirements
1. Ubuntu
2. python 3 or greater

# Installation steps
1. Install virtual env folder inside the directory like `python -m venv myenv`
2. Activate virtual env like `source myenv/bin/activate`
3. Install dependancies using `pip3 install -r requirements.txt`


# Running the app
1. Run `python3 zpl_tracker.py` using the terminal

# TODOs:
1. Compile this into executionable file that can be easily installed
2. Change this into a background service that can run on computer startup
3. Add printer name configuration instead of depending on default printer provided by Os
4. Windows support