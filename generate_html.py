import sys
import os
import jinja2
from datetime import datetime
from process_trace import process_trace
import regiontree

def gen(tracename, tracedir):

    # temporarily get debug output to put into the HTML
    timing_trees = process_trace(tracedir)

    jenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = jenv.get_template("index.html.jinja")
    out = template.render(tracename=tracename, now=datetime.now(), timing_trees=timing_trees)
    
    #print("Output:\n\n{}\n\n".format(out))

    outdir = "out/{}".format(tracename)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    with open("{}/{}".format(outdir, "index.html"), "w") as fh:
        fh.write(out)
    
    print("Generated file: {}/index.html".format(outdir))

        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-html.py <tracename> <tracedir>\n")
    else:
        gen(sys.argv[1], sys.argv[2])
