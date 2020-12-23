#!/bin/python
import sys
import os
import uuid
from subprocess import DEVNULL, STDOUT, check_call
from datetime import datetime

worklog_dir = "/home/XXX/worklog/"
image_command = "deepin-screenshot -s " + worklog_dir
args = sys.argv[1:]

def make_new_project(project_name, log_dir):
    # Make new directory
    try:
        os.mkdir(log_dir + project_name)
    except:
        pass

def add_new_entry(path, info, image=None):
    # Open up log file
    out_file = open(path + "log.md", "a")

    now = datetime.now()
    
    # Write down time and info
    out_file.write("## Entry: " + now.strftime("%m/%d/%Y %-I:%M:%S") + "\n\n")
    out_file.write(info + "\n\n")

    # Put image if available
    if image != None:
        out_file.write("![](" + path + image + ")\n\n") 

    # Newline and close
    out_file.write("---\n\n")
    out_file.close()


def take_image(name, command, extension) -> str:
    # Make uuid for image name
    img_name = str(uuid.uuid1())

    # Put together command
    final_cmd = (command + name + "/" + img_name + extension).split(" ")

    # Call command
    check_call(final_cmd, stdout=DEVNULL, stderr=STDOUT)

    # Return image name
    return img_name + ".png"


# If new, run new project
if args[0] == "new":
    make_new_project(args[1], worklog_dir)

# If "with picture" run new entry with image
elif args[0] == "wp":
    img_name = take_image(args[1], image_command, ".png")
    add_new_entry(worklog_dir + args[1] + "/", args[2], img_name)

# If view, run view
elif args[0] == "view":
    command = ("markdown_previewer " + worklog_dir + args[1] + "/log.md").split(" ")
    check_call(command)

# Otherwhise just add entry
else:
    add_new_entry(worklog_dir + args[0] + "/", args[1])
