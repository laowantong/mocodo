from IPython.core.display import HTML
from IPython.core.display import SVG
from IPython.core.display import display
from IPython.core.magic import (Magics, magics_class, line_cell_magic)
from IPython.utils.warn import error

import os.path
import argparse

from subprocess import Popen, PIPE
import os, codecs

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
            %load_ext mocodo
        """
        
        def execute_command(options):
            global stdoutdata
            process = Popen(["mocodo"] + options, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdoutdata, stderrdata = process.communicate()
            status = process.wait()
            if status == 0 and stderrdata == "":
                return True
            error(stderrdata.strip())
        
        def display_diagrams():
            if os.path.isfile(output_name + ".svg") and os.path.getmtime(input_path) <= os.path.getmtime(output_name + ".svg"):
                if not notebook_options.no_mcd:
                    display(SVG(filename=output_name + ".svg"))
                if notebook_options.mld:
                    mld = codecs.open(output_name + ".html", "r", 'utf8').read()
                    display(HTML(mld))
                return True
        
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--no_mcd", action="store_true")
        parser.add_argument("--mld", action="store_true")
        parser.add_argument("--input")
        parser.add_argument("--output_dir")
        parser.add_argument("--image_format")
        (notebook_options, options) = parser.parse_known_args(line.split())
        
        input_path = notebook_options.input
        if not input_path:
            input_path = "mocodo_notebook/sandbox.mcd"
            codecs.open(input_path, "w", "utf8").write(cell)
        elif not os.path.isfile(input_path) and os.path.isfile(input_path + ".mcd"):
            input_path += ".mcd"
        
        output_dir = notebook_options.output_dir
        if not output_dir:
            output_dir = "mocodo_notebook"
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
                    print '# You may edit and run the following lines in a new cell\n\nimport codecs\nparams = u"""\n%s"""\ncodecs.open("%s/params.json", "w", "utf8").write(params.strip())' % (stdoutdata, output_dir)
                elif "--help" in options:
                    print stdoutdata
                else:
                    print "%%mocodo"
                    print stdoutdata
                    if not notebook_options.no_mcd or notebook_options.mld:
                        parser.add_argument("--arrange", nargs="?")
                        parser.add_argument("--obfuscate", nargs="?")
                        parser.add_argument("--flip", nargs="?")
                        (_, options) = parser.parse_known_args(options)
                        codecs.open(input_path, "w", "utf8").write(stdoutdata.decode("utf8"))
                        options.extend(["--input", input_path, "--output_dir", output_dir, "--image_format", "svg"])
                        if execute_command(options):
                            display_diagrams()

def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(MocodoMagics)

