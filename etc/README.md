# Men&Mice Action Generator

Men&Mice uses a SOAP API which details all operations and data types available.
In order to save lots of manual labor we've created a script to parse the 
SOAP WSDL file and generate StackStorm actions from it.

# Typical Workflow

``` shell
# fetch the latest WSDL from the Men&Mice server
./action_generate.py fetch-wsdl -H menandmice.domain.tld

# gerenate actions from the latest WSDL (outpuit to ../actions)
./action_generate.py generate
  
# see more examples
./action_generate.py examples
```

# How it works

1. Fetch the SOAP WSDL from the Men&Mice server
2. Parse the SOAP WSDL file
3. Iterate over all of the `operations` aka commands.
4. For each `operation` gather all input arguments
5. Populate a `dict` with all of the information about the operation
   and its input arguments
6. Render an action YAML for this opeartion using from the `etc/action_template.yaml.j2` 
   Jinja2 template. The context for the render is the `dict` created above.
