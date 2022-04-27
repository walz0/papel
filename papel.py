"""
    papel - raw text document router
    :: walz 2020
"""
import sys
import os

# Output HTML document
output = ""
# List of paragraphs
paragraphs = []
# List of citations
citations = []
# Title page lines
title_lines = []
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
    
    # This should be loaded from a css file
    output += "<!DOCTYPE html><html>"
    output += "<style>"
    output += "body {font-size: %spx; " % (str(options['-s']))
    output += "text-indent: %spx; " % (str(options['-i']))
    output += "line-height: %s}" % (str(options['-h']))
    output += ".citation { padding-left: 36px; text-indent: -36px }"
    output += ".title-page { line-height: 1.5; text-align: center }"
    output += "</style>"
    output += "<body>"
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

def addTitlePage(raw, nl):
    global output
    global title_lines
    # Start of the title page
    t_index = 0
    for i in range(len(raw)):
        if raw[i] == "\\":
            if (i - 1) in nl: # If a return precedes
                raw = raw[:i] # Remove indicator in output
                t_index = i # Record start of title page
                raw = raw.strip()
                break
    # Clear newlines
    nl = [] 
    if t_index: # If title page exists
        # Previous line start index
        prev = 0 
        # Crop raw text to title page section
        raw = raw[:t_index]
        # Count new lines
        for i in range(len(raw)):
            if raw[i] == "\n":
                nl += [i] 

        # Add padding to top
        output += "<br>" * 6
        output += "<div class='title-page'>"
        for i in range(len(raw)):
            # If new line
            if i != 0:
                if i in nl and i+1 in nl: # If new line is consecutive
                    if len(title_lines) == 0:
                        # Center section
                        # Add title
                        output += "<p style='padding-left: 20px; text-align: center; text-indent: 0; font-weight: bold;'>{}</p><br>".format(raw[prev:i].strip())
                        title_lines += [raw[prev:i].strip()]
                        prev = i
                        continue
                    # Add new line
                    addTitlePageLine(raw[prev:i].strip())
                    prev = i
    output += "</div>"
    # Add padding to bottom
    output += "<br>" * 9

# Returns a list of indeces of the \n chars in the text
def getNewlines(text):
    # Output
    nl = []
    # Previous paragraph start index
    prev = 0
    # Calculate end index by distance from last newline 
    for i in range(len(text)):
        if text[i] == "\n":
            nl += [i]
    return nl

def addBody(raw, nl):
    t_index = 0 # Title page index
    for i in range(len(raw)):
        if raw[i] == "\\":
            if (i - 1) in nl:
                # Detected title page
                t_index = i+2
    #nl = []
    # Previous paragraph start index
    prev = t_index
    # Calculate end index by distance from last newline 
    for i in range(t_index, len(raw)):
        if raw[i] == "\n":
            #nl += [i]
            if i == len(raw) - 1:
                addParagraph(raw[prev:i].strip())
                break
            # If new line is consecutive
            if raw[i - 1] == "\n":
                # Add a new paragraph
                addParagraph(raw[prev:i].strip())
                prev = i
        # References reached
        if raw[i] == "/":
            if (i - 1) in nl:
                addParagraph(raw[prev:i].strip())
                break
        if i == len(raw) - 2:
            # Reached end of document
            addParagraph(raw[prev:i].strip())
            break

def addReferences(raw, nl):
    global output
    # Start of References
    r_index = 0 
    # References (Forward slash between two returns)
    for i in range(len(raw)):
        if raw[i] == "/":
            if (i - 1) in nl: # If a return precedes
                raw = raw[:i] + raw[i+1:] # Remove indicator in output
                r_index = i # Record start of References
                break
    # Clear newlines
    nl = [] 
    if r_index: # If References exists
        # Add References title
        output += "<p style='text-align: center; text-indent: 0; font-weight: bold; margin: 35px 0 -10px 0'>References</p>"  
        # Previous citation start index
        prev = 0 
        # Crop raw text to References section
        raw = raw[r_index:]
        # Count new lines
        for i in range(len(raw)):
            if raw[i] == "\n":
                nl += [i] 
        # Remove new line after indicator
        nl = nl[1:]
        
        for i in range(len(raw)):
            # If new line (citation)
            if i != 0:
                if i in nl and i+1 in nl: # If new line is consecutive
                    # Add new citation
                    addCitation(raw[prev:i])
                    prev = i

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

def addTitlePageLine(text):
    global output
    global title_lines
    output += "<p>{}</p>".format(text)
    title_lines += [text]

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
    nl = getNewlines(raw)
    # Process title page
    addTitlePage(raw, nl)
    if len(title_lines[0].split(" ")) > 12:
        print("Warning: APA recommends that your title be no more than 12 words in length")
    # Process body
    addBody(raw, nl)
    # Process references
    addReferences(raw, nl)
    # Output HTML file
    render()

    """
        -Footers
        -Page Numbers
        -Save as PDF (use selenium to automate chrome print to PDF with 1" margins)
        -Fix links in citations zooming out the page
    """
