"""

    papel - raw text document router

    Written by Aidan Walz 2020

"""
import sys
import os

# Output HTML document
output = ""

# Total number of paragraphs
paragraphs = []

def init():
    global output
    # DEFAULTS

    options = {
        '-s' : 17, # font-size
        '-i' : 50, # text-indent 
        '-h' : 2   # line-height 
    }
    if len(sys.argv) > 1:
        for o in options:
            if o in sys.argv:
                options[o] = select_args(o)

    output += "<!DOCTYPE html><html><style>body {font-size: " + str(options['-s'])
    output += "px; text-indent: " + str(options['-i']) 
    output += "px; line-height: " + str(options['-h']) + "}</style><body>"
    pass

def select_args(option):
    """

        ARGUMENTS:
            -s :: font-size
            -i :: text-indent 
            -h :: line-height 

    """
     # Screen args for selected option
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == option: # If option selected 
            if i != len(sys.argv) - 1: # If not at the end of args
                try:
                    # If size arg is an integer
                    if int(sys.argv[i + 1]):
                        return int(sys.argv[i + 1])
                except:
                    print("ERROR: Argument not valid, please use the syntax \"{} [integer]\"".format(option))


def addParagraph(text):
    global output
    global paragraphs
    paragraphs += [text]
    output += "<p>{}</p>".format(text)


def render():
    global output
    # Write end of document
    output += "</body></html>"
    # Create new output file if one does not exist
    f = open("output.html", "w")
    # Overwrite existing output file data
    f.write(output)
    # Close file
    f.close()


if __name__ == "__main__":
    # Load raw text 
    raw = ""
    with open("raw.txt", "r") as paper:
        raw = paper.read(); 

    # Initialize HTML document
    init()

    # New line character queue
    nl = []
    # Previous paragraph start index
    prev = 0
    # Calculate end index by distance from last newline 
    for i in range(len(raw)):
        if raw[i] == "\n":
            nl += [i]
            if i == len(raw) - 1:
                addParagraph(raw[prev:i])
                break
        # If new line is consecutive
        if len(nl) > 1:
            if nl[len(nl) - 2] == i - 1:
                # Add a new paragraph
                addParagraph(raw[prev:i])
                # nl = []
                prev = i
        if i == len(raw) - 2:
            # Reached end of document
            addParagraph(raw[prev:i])
            break
    render()
