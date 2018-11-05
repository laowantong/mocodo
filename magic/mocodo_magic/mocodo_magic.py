#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from __future__ import print_function
from IPython.core.display import HTML
from IPython.core.display import SVG
from IPython.core.display import display
from IPython.core.magic import (Magics, magics_class, line_cell_magic)
import warnings

import os.path
import argparse

from subprocess import Popen, PIPE
import os, codecs

def read_contents(filename, encoding="utf8"):
    with codecs.open(filename, encoding=encoding) as f:
        return f.read()

def write_contents(filename, contents, encoding="utf8"):
    with codecs.open(filename, encoding=encoding, mode="w") as f:
        f.write(contents)

@magics_class
class MocodoMagics(Magics):

    @line_cell_magic
    def mocodo(self, line, cell=""):
        """
        Mocodo IPython magic extension

        Magic methods:
            %mocodo [command line options]
            %%mocodo [command line options]
            < MCD ... >

        Usage:
            %load_ext mocodo_magic
        """
        
        def execute_command(options):
            global stdoutdata
            process = Popen(["mocodo"] + options, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdoutdata, stderrdata = process.communicate()
            try:
                stdoutdata = stdoutdata.strip().decode("utf8")
                stderrdata = stderrdata.strip().decode("utf8")
            except:
                pass
            status = process.wait()
            if status == 0 and not stderrdata:
                return True
            warnings.formatwarning = lambda x, *args, **kargs : str(x)
            warnings.warn(stderrdata)
        
        def display_diagrams():
            if os.path.isfile(output_name + ".svg") and os.path.getmtime(input_path) <= os.path.getmtime(output_name + ".svg"):
                if not notebook_options.no_mcd:
                    display(SVG(filename=output_name + ".svg"))
                if notebook_options.mld:
                    mld = read_contents(output_name + ".html")
                    display(HTML(mld))
                return True
        
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--no_mcd", action="store_true")
        parser.add_argument("--mld", action="store_true")
        parser.add_argument("--input")
        parser.add_argument("--output_dir")
        parser.add_argument("--image_format")
        (notebook_options, options) = parser.parse_known_args(line.split())
        
        try:
            os.makedirs("mocodo_notebook")
        except OSError:
            if not os.path.isdir("mocodo_notebook"):
                raise
        input_path = notebook_options.input
        if not input_path:
            input_path = "mocodo_notebook/sandbox.mcd"
            write_contents(input_path, cell)
        elif not os.path.isfile(input_path) and os.path.isfile(input_path + ".mcd"):
            input_path += ".mcd"
        
        output_dir = notebook_options.output_dir
        if not output_dir:
            output_dir = "mocodo_notebook"
        else:
            try:
                os.makedirs(output_dir)
            except OSError:
                if not os.path.isdir(output_dir):
                    raise
        output_name = os.path.join(output_dir, os.path.splitext(os.path.split(input_path)[1])[0])
        
        options.extend(["--input", input_path, "--output_dir", output_dir, "--image_format", "svg"]) # may override user's provided options
        try: # prevent explicit option --relations to override HTML generation
            options.insert(options.index("--relations") + 1, "html")
        except ValueError:
            pass
        
        if execute_command(options):
            if not display_diagrams():
                if "--print_params" in options:
                    form = '# You may edit and run the following lines\n'\
                           'import codecs, json\n'\
                           'params = u"""\n'\
                           '%s"""\n'\
                           'try:\n'\
                           '    json.loads(params)\n'\
                           'except:\n'\
                           '    raise RuntimeError("Invalid JSON. Find out why on http://jsonlint.com")\n'\
                           'with codecs.open("%s/params.json", "w", "utf8") as f:\n'\
                           '    f.write(params.strip())'
                    get_ipython().set_next_input(form % (stdoutdata, output_dir), replace = True)
                    return
                if "--help" in options:
                    print(stdoutdata)
                    return
                if "--replace" in options:
                    get_ipython().set_next_input("%%mocodo\n" + stdoutdata.rstrip(), replace = True)
                    return
                print("%%mocodo")
                print(stdoutdata.rstrip())
                if not notebook_options.no_mcd or notebook_options.mld:
                    parser.add_argument("--arrange", nargs="?")
                    parser.add_argument("--obfuscate", nargs="?")
                    parser.add_argument("--flip", nargs="?")
                    (_, options) = parser.parse_known_args(options)
                    write_contents(input_path, stdoutdata)
                    options.extend(["--input", input_path, "--output_dir", output_dir, "--image_format", "svg"])
                    if execute_command(options):
                        display_diagrams()

def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(MocodoMagics)
