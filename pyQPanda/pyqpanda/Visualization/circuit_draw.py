import pyqpanda.pyQPanda as pq
#import matplotlib.pyplot as plt
from .matplotlib_draw import *

def draw_circuit_pic(prog, pic_name, verbose=False):
    layer_info = pq.circuit_layer(prog)
    qcd = MatplotlibDrawer(qregs = layer_info[1], cregs = layer_info[2], ops = layer_info[0], scale=0.7)
    qcd.draw(pic_name, verbose)

def draw_qprog(prog, output=None, scale=0.7, filename=None, with_logo = False, line_length=100, NodeIter_first=None, \
    NodeIter_second=None, console_encode_type = 'utf8'):
    """Draw a quantum circuit to different formats (set by output parameter):

    **text**: ASCII art TextDrawing that can be printed in the console.

    **pic**: images with color rendered purely in Python.

    **latex**: latex source code of circuit

    Args:
        prog : the quantum circuit to draw
        scale (float): scale of image to draw (shrink if < 1). Only used by the ``pic`` outputs.
        filename (str): file path to save image to
        NodeIter_first: circuit printing start position.
        NodeIter_second: circuit printing end position.
        console_encode_type(str): Target console encoding type. 
            Mismatching of encoding types may result in character confusion, 'utf8' and 'gbk' are supported.
            Only used by the ``pic`` outputs.
        line_length (int): Sets the length of the lines generated by `text` output type.

    Returns: no return

    """
    default_output = 'text'
    if output is None:
        output = default_output

    text_pic = 'null'
    if output == 'pic':
        if filename is None:
            filename = 'QCircuit_pic.jpg'
        draw_circuit_pic(prog, filename)
    elif output == 'text':
        if filename is None:
            filename = ''
        if NodeIter_first is None and  NodeIter_second is None:
            text_pic = pq.draw_qprog_text(prog, line_length, filename)
        elif NodeIter_first is None:
            text_pic = pq.draw_qprog_text(prog, line_length, filename, prog.begin(), NodeIter_second)
        elif NodeIter_second is None:
            text_pic = pq.draw_qprog_text(prog, line_length, filename, NodeIter_first, prog.end())
        
        if console_encode_type == 'gbk':
            text_pic = pq.fit_to_gbk(text_pic)
        
        #print(text_pic)
    elif output == 'latex':
        if filename is None:
            filename = 'QCircuit_latex.tex'
        if NodeIter_first is None and  NodeIter_second is None:
            text_pic = pq.draw_qprog_latex(prog, line_length, filename, with_logo)
        elif NodeIter_first is None:
            text_pic = pq.draw_qprog_latex(prog, line_length, filename, with_logo, prog.begin(), NodeIter_second)
        elif NodeIter_second is None:
            text_pic = pq.draw_qprog_latex(prog, line_length, filename, with_logo, NodeIter_first, prog.end())
        
    return text_pic