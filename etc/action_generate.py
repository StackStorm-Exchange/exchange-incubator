#!/usr/bin/env python
#
# Description:
#
# Usage:
#
# Files generated
#  actions/*.yaml (one for each operation in etc/menandmice_wsdl.xml)
#
import re
import jinja2

import zeep
import operator # todo remove this
import datetime
import os
import requests
import sys
import argparse
import glob
import json
import pprint
from xml.dom import minidom


WSDL_FILE = "./cmdlets.txt"
ACTION_TEMPLATE_PATH = "./action_template.yaml.j2"
ACTION_DIRECTORY = "../actions"
WSDL_URL = "http://{0}/_mmwebext/mmwebext.dll?wsdl?server=localhost"

DEFAULT_ACTION_PARAMS = ['operation',
                         'connection',
                         'server',
                         'username',
                         'password',
                         'port',
                         'transport']

class Cli:
    def parse(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        # Subparsers
        subparsers = parser.add_subparsers(dest="command")

        ## commands
        fetch_parser = subparsers.add_parser('fetch-wsdl',
                                             help="Deploy packs to a host")
        # connection args
        fetch_parser.add_argument('-H', '--hostname',
                                  help='Hostname/IP of Men&Mice Server',
                                  required=True)
        fetch_parser.add_argument('-w', '--wsdl-path',
                                  help="WSDL file to write to")

        generate_parser = subparsers.add_parser('generate',
                                                help="Generate actions from the the WSDL")
        action_dir = os.path.join(os.path.dirname(__file__), '..', 'actions')
        generate_parser.add_argument('-d', '--directory', default=action_dir,
                                     help="Directory where actions should be written to")
        generate_parser.add_argument('-w', '--wsdl-path',
                                     help="WSDL file to use")

        examples_parser = subparsers.add_parser('examples',
                                                help="Prints examples of how to use this script to stdout"
        )

        args = parser.parse_args()
        if args.command == "examples":
            self.examples()
            exit(0)
        return args

    def examples(self):
        print "examples:\n"\
            "  # fetch the latest WSDL from the Men&Mice server/\n"\
            "  ./action_generate.py fetch-wsdl -H host.domain.tld\n"\
            "\n"\
            "  # fetch the latest WSDL from the Men&Mice server to a specific name/\n"\
            "  ./action_generate.py fetch-wsdl -H host.domain.tld -w menandmice_wsdl_new.xml\n"\
            "\n"\
            "  # gerenate actions from the latest WSDL/\n"\
            "  ./action_generate.py generate\n"\
            "\n"\
            "  # gerenate actions into an alternate directory from a specific WSDL/\n"\
            "  ./action_generate.py generate -d ../actions_new -w menandmice_wsdl_new.xml\n"\


class ActionGenerator(object):

    def __init__(self, cli_args, **kwargs):
        self.cli_args = cli_args

    def run(self):
        if self.cli_args.command == "fetch-wsdl":
            self.fetch_wsdl()
        elif self.cli_args.command == "generate":
            self.generate()
        else:
            raise RuntimeError("Unknown command {}".format(self.cli_args.command))

    def fetch_wsdl(self):
        wsdl_url = WSDL_URL.format(self.cli_args.hostname)
        response = requests.get(wsdl_url)
        xml = minidom.parseString(response.text)
        xml_str = xml.toprettyxml(indent="   ")

        t = datetime.datetime.now()
        date_str = t.strftime('%Y_%m_%d')

        with open("menandmice_wsdl_{}.xml".format(date_str), "w") as f:
            f.write(xml_str)

    def camel_case_to_snake_case(self, name):
        s0 = name.replace('-', '')
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s0)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def jinja_render_file(self, filename, context):
        path, filename = os.path.split(filename)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(context)


    def jinja_render_str(self, jinja_template_str, context):
        return jinja2.Environment().from_string(jinja_template_str).render(context)

    def render_action(self, context):
        action_data = self.jinja_render_file(ACTION_TEMPLATE_PATH, context)
        action_filename = "{}/{}.yaml".format(ACTION_DIRECTORY,
                                              context['operation_snake_case'])
        with open(action_filename, "w") as f:
            f.write(action_data)

    def build_type_dict(self, type_elem):
        elem_type = type_elem.type
        if not elem_type.name:
            return None

        if isinstance(elem_type, zeep.xsd.types.builtins.BuiltinType):
            if type_elem.accepts_multiple:
                return [ elem_type._default_qname.localname ]
            else:
                return elem_type._default_qname.localname
        else:
            type_dict = {}
            for attribute_name, attribute_elem in elem_type.elements:
                attribute_obj = self.build_type_dict(attribute_elem)
                type_dict[attribute_name] = attribute_obj

            if type_elem.accepts_multiple:
                type_dict = [type_dict]
        return type_dict

    def get_type_description(self, type_elem):
        type_dict = self.build_type_dict(type_elem)
        #type_desc = pprint.pformat(type_dict)
        type_desc = json.dumps(type_dict, indent=2)
        type_desc = type_desc.replace('\n', '\n       ')
        return ">\n      '" + type_desc + "'"

    def generate(self):
        wsdl_path = None
        if self.cli_args.wsdl_path:
            wsdl_path = self.cli_args.wsdl_path
        else:
            wsdl_files = glob.glob("./menandmice_wsdl_*.xml")
            # find newest wsdl (by name)
            wsdl_path = max(wsdl_files)

        client = zeep.Client(wsdl=wsdl_path)

        operations_context = []

        # Parse Operations from the WSDL file
        for service in client.wsdl.services.values():
            if service.name != "Service":
                continue

            for port in service.ports.values():
                if port.name != "ServiceSoap12":
                    continue

                operations = sorted(port.binding._operations.values(),
                                    key=operator.attrgetter('name'))

                for operation in operations:
                    name = operation.name
                    op_inputs = []

                    for input_name, input_elem in operation.input.body.type.elements:
                        type_obj = input_elem.type
                        input_type = type_obj.name
                        param_required = 'true' if input_elem.min_occurs > 0 else 'false'
                        parameter_name = self.camel_case_to_snake_case(input_name)

                        if name == 'GetHistory' and parameter_name == 'username':
                            parameter_name = 'user_name'
                        elif name == 'Login' and parameter_name == 'server':
                            continue
                        elif name == 'Login' and parameter_name == 'password':
                            continue
                        elif name == 'Login' and parameter_name == 'login_name':
                            continue

                        if parameter_name in DEFAULT_ACTION_PARAMS:
                            print ("ERROR: Param conflicts with default: {}.{}"
                                   .format(name, parameter_name))

                        if isinstance(type_obj, zeep.xsd.types.builtins.BuiltinType):
                            description = None
                            if input_name == "session":
                                param_required = False
                                description = '"Login session cookie. If empty then username/password will be used to login prior to running this operation"'

                            type_name = type_obj._default_qname.localname
                            parameter_type = type_name
                            if type_name == "unsignedInt":
                                parameter_type = "integer"
                            op_inputs.append({'name': input_name,
                                              'data_type': type_obj._default_qname.localname,
                                              'type_name': input_type,
                                              'type_elem': input_elem,
                                              'builtin': True,
                                              'parameter_name': parameter_name,
                                              'parameter_type': parameter_type,
                                              'parameter_description': description,
                                              'parameter_required': param_required})
                        else:
                            op_inputs.append({'name': input_name,
                                              'data_type': 'object',
                                              'type_name': input_type,
                                              'type_elem': input_elem,
                                              'builtin': False,
                                              'parameter_name': parameter_name,
                                              'parameter_type': 'object',
                                              'parameter_description': self.get_type_description(input_elem),
                                              'parameter_required': param_required})

                    # Debug
                    # op_inputs_str = [input['type_name'] + "(" + input['data_type'] + ") " + input['name'] for input in op_inputs]
                    # print "{}({})".format(name, ', '.join(op_inputs_str))

                    op_context = {'name': name,
                                  'inputs': op_inputs,
                                  'operation_camel_case': name,
                                  'operation_snake_case': self.camel_case_to_snake_case(name),
                                  'operation_description': 'None (yet)',
                                  'operation_parameters': op_inputs}
                    self.render_action(op_context)


if __name__ == "__main__":
    cli = Cli()
    args = cli.parse()
    generator = ActionGenerator(args)
    generator.run()
