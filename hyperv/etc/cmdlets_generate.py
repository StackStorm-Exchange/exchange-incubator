#!/usr/bin/env python
#
# Description:
#  This script generates all of our actions for Hyper-V cmdlets from etc/cmdlets.txt
#  placing all of the actions into actions/*.yaml. Each action is generated
#  from the Jinja template etc/action_template.yaml.
#
#  This also generates an etc/action_table.md file that contains the table of
#  actions seen in the README.md (manually copied in). Each line in the file
#  is generated from a Jinja template etc/action_table_template.txt
#
# Usage:
#  ./cmdlets_generate.py
#
# Files generated
#  actions/*.yaml (one for each action in etc/cmdlets.txt)
#  etc/action_table.md
#
import re
import os
import jinja2

CMDLETS_FILE = "./cmdlets.txt"

ACTION_TEMPLATE_PATH = "./action_template.yaml"
ACTION_DIRECTORY = "../actions"

TABLE_TEMPLATE_PATH = "./action_table_template.txt"
TABLE_FILE_PATH = "./action_table.md"
# POWERSHELL_LINK_URL_BASE = "https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration"  # noqa
POWERSHELL_LINK_URL_BASE = "https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps" # noqa


def convert_camel_case_to_snake_case(name):
    s0 = name.replace('-', '')
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s0)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def jinja_render(filename, context):
    path, filename = os.path.split(filename)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


def render_action(context):
    return jinja_render(ACTION_TEMPLATE_PATH, context)


def render_table(context):
    return jinja_render(TABLE_TEMPLATE_PATH, context)


def read_file_lines(filename):
    with open(CMDLETS_FILE) as f:
        content = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
    return content


def main():
    cmdlet_lines = read_file_lines(CMDLETS_FILE)
    context = {}
    context['cmdlet_camel_case'] = None
    context['cmdlet_snake_case'] = None
    context['description'] = None
    context['powershell_url'] = None

    try:
        os.remove(TABLE_FILE_PATH)
    except OSError:
        pass

    with open(TABLE_FILE_PATH, "a+") as f:
        f.write(("| Action | PowerShell Cmdlet | Description |\n"
                 "|--------|-------------------|-------------|\n"))

    # File format
    #  Cmdlet-CamelCase
    #  Cmdlet description string
    #  Cmdlet2-CamelCase
    #  Cmdlet2 description string
    #  ...
    for idx, line in enumerate(cmdlet_lines):
        if (idx % 2 == 0):  # is even
            context['cmdlet_camel_case'] = line
            context['cmdlet_snake_case'] = convert_camel_case_to_snake_case(line)
        else:  # is even
            # Generate the action/cmdlet.yaml for this cmdlet
            context['description'] = line
            action_data = render_action(context)
            action_filename = "{}/{}.yaml".format(ACTION_DIRECTORY,
                                                  context['cmdlet_snake_case'])
            with open(action_filename, "w") as f:
                f.write(action_data)

            # Generate a line for this cmdlet in etc/action_table.md
            context['powershell_url'] = "{}/{}".format(POWERSHELL_LINK_URL_BASE,
                                                       context['cmdlet_camel_case'].lower())
            action_table = render_table(context)
            with open(TABLE_FILE_PATH, "a+") as f:
                f.write(action_table + "\n")


if __name__ == "__main__":
    main()
