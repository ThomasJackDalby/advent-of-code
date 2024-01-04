import xml.etree.ElementTree as ET

svg = ET.Element("svg",
    xmlns="http://www.w3.org/2000/svg",
    viewBox = "0 0 1000 1000"
)

current_style = { 
    "stroke" : "black",
    "fill-opacity" : "0",
}

# style
def stroke(r, g, b):
    current_style["stroke"] = f"rgb({r},{g},{b})"

def stroke_weight(value):
    current_style["stroke-width"] = str(value)

def format_style(style):
    return ";".join((f"{key}:{value}" for key, value in style.items()))

def rect(x, y, w, h):
    element = ET.SubElement(svg, "rect")
    element.set("x", str(x))
    element.set("y", str(y))
    element.set("width", str(w))
    element.set("height", str(h))
    element.set("style", format_style(current_style))

def line(x1, y1, x2, y2):
    element = ET.SubElement(svg, "line")
    element.set("x1", str(x1))
    element.set("y1", str(y1))
    element.set("x2", str(x2))
    element.set("y2", str(y2))
    element.set("style", format_style(current_style))

def ellipse(x, y, r1, r2=None):
    if r2 is None: 
        element = ET.SubElement(svg, "circle")
        element.set("r", str(r1))        
    else: 
        element = ET.SubElement(svg, "ellipse")
        element.set("rx", str(r1))
        element.set("ry", str(r2))
    element.set("cx", str(x))
    element.set("cy", str(y))
    element.set("style", format_style(current_style))


def background(r, g, b):    
    svg.set("style", f"background-color:rgb({r},{g},{b})")

def save(file_path):
    tree = ET.ElementTree(svg)
    ET.indent(tree, space="\t", level=0)
    tree.write(file_path)