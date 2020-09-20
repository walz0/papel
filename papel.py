"""

    papel - raw text document router

    Written by Aidan Walz 2020

"""
import sys
import os
# Output HTML document
output = ""

# List of paragraphs
paragraphs = []

# List of citations
citations = []

# Number of spaces per tab
tab_stop = 4


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
    output += "px; line-height: " + str(options['-h']) + "}"
    output += ".citation { padding-left: 36px; text-indent: -36px }</style><body>"
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


def addCitation(text):
    global output
    global citations
    output += "<p class='citation'>{}</p>".format(text)
    citations += [text]
    

def spacesToTabs(text):
    global tab_stop
    tab = tab_stop * ' '
    count = 0 # Current space count
    for i in range(len(text)):
        if i + (tab_stop - 1) < len(text) - 1:
            if text[i:i+tab_stop] == tab: 
                # Replace spaces with tab
                text = text[:i] + '\t' + text[i + (tab_stop):]
    return text
                
                
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
                prev = i
        # Works Cited reached
        if raw[i] == "/":
            if (i - 1) in nl:
                addParagraph(raw[prev:i])
                break
        if i == len(raw) - 2:
            # Reached end of document
            addParagraph(raw[prev:i])
            break
 
    # Start of Works Cited 
    wc_index = 0 
    # Works Cited (Forward slash between two returns)
    for i in range(len(raw)):
        if raw[i] == "/":
            if (i - 1) in nl: # If a return precedes
                raw = raw[:i] + raw[i+1:] # Remove indicator in output
                wc_index = i # Record start of Works Cited
                for _ in nl:
                    if _ == wc_index - 1:
                        nl = nl[_:] # Crop nl to start from Works Cited
                break
    
    if wc_index > 0: # If Works Cited exists
        # Add Works Cited title
        output += "<p style='text-align: center; text-indent: 0; font-weight: bold; margin: 35px 0 -10px 0'>References</p>"  
        # Previous citation start index
        prev = 0 
        # Crop raw text to works cited section
        raw = raw[wc_index:]
        # Count new lines
        for i in range(len(raw)):
            if raw[i] == "\n":
                nl += [i] 
        # Remove new line after indicator
        nl = nl[1:]
        
        for i in range(len(raw)):
            # If new line (citation)
            if i != 0:
                if i in nl and i+1 in nl: # If new line consecutive
                    # Add new citation
                    addCitation(raw[prev:i])
                    prev = i 
    render()

    """
        Fix links in citations zooming out the page
    """
