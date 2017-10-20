#!/usr/bin/python

from botocore.session import Session

import re
import os
import sys
import botocore
import argparse
import jinja2


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

session = Session()
allservices = session.get_available_services()

parser = argparse.ArgumentParser(description="Generate aws stackstorm actions")
parser.add_argument('-d', '--outputdir', default="actions", help="base output directory")
parser.add_argument('-s', '--service', default=None, help="service to generate actions for (eg s3)")
parser.add_argument('-v', '--version', required=True, help="pack version to generate")
args = parser.parse_args()

myservice = args.service
outputdir = args.outputdir
version = args.version
actionsdir = outputdir + "/actions"

# print "outputdir: %s" % outputdir
# print "myservice: %s" % myservice

try:
    os.stat(outputdir)
except:
    os.mkdir(outputdir)

try:
    os.stat(actionsdir)
except:
    os.mkdir(actionsdir)

templateLoader = jinja2.FileSystemLoader(searchpath="templates")
templateEnv = jinja2.Environment(loader=templateLoader)

if myservice is None:
    print "service not defined. please choose from the following:\n"
    print ', '.join(session.get_available_services())
    print
    sys.exit(1)
  
print "Creating pack for %s:" % myservice

try:
    mysrv = session.get_service_model(myservice)
except botocore.exceptions.UnknownServiceError as e:
    print "\n%s\n" % e
    sys.exit(1)

allvars = {}
allvars['pack'] = 'aws_' + myservice
allvars['service'] = myservice
allvars['pack_version'] = version

packyaml = outputdir + '/pack.yaml'
template = templateEnv.get_template('pack_template.yaml.jinja')

with open(packyaml, 'w') as y:
    outputText = template.render(allvars).encode('utf8')  # pylint: disable=no-member
    y.write(outputText)

for op in mysrv.operation_names:

    allvars['paramsreq'] = []
    allvars['params'] = []

    model = mysrv.operation_model(op)

    op = convert(op)

    print " " + op
    allvars['action'] = op
    allvars['name'] = op

    if model.input_shape is None:
        continue

    members = model.input_shape.members

    smodel = model.service_model

    # print smodel._shape_resolver

    smembers = model.input_shape._shape_model['members']
    for sname, sdata in smembers.items():
        tmp = {}
        stype = smodel._shape_resolver._shape_map[sdata['shape']]['type']
        # blob defined in boto as bytes or seekable file-like object - not supported here
        if stype == "blob":
            stype = "string"
        if stype == "double":
            stype = "number"
        if stype == "long":
            stype = "integer"
        if stype == "structure":
            stype = "object"
        if stype == "map":
            stype = "object"
        if stype == "list":
            stype = "array"
        if stype == "timestamp":
            stype = "string"
        if stype == "float":
            stype = "number"
        tmp['name'] = sname
        tmp['type'] = stype
        if 'documentation' in sdata:
            tmp['description'] = striphtml(sdata['documentation'].rstrip().replace('"', "'"))
            tmp['description'] = striphtml(tmp['description'].replace("\\", "\\\\"))
        else:
            tmp['description'] = ''

        if sname in model.input_shape.required_members:
            allvars['paramsreq'].append(tmp)
        else:
            allvars['params'].append(tmp)

    actionyaml = actionsdir + '/' + allvars['name'] + ".yaml"
    template = templateEnv.get_template('action_template.yaml.jinja')

    with open(actionyaml, 'w') as y:
        outputText = template.render(allvars).encode('utf8')  # pylint: disable=no-member
        y.write(outputText)
