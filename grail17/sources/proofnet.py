#!/usr/bin/env python

# LIRa refers to:
# http://www.phil.uu.nl/~moortgat/lmnlp/2012/Docs/contributionLIRA.pdf
# Proofs nets and the categorial flow of information
# Michael Moortgat and Richard Moot

import re

import os, sys
import platform
import argparse
import textwrap
  
 
vertices = 0
  

class ProofStructure:

    def __init__(self, formula, vertex):
        self.formula = formula
        self.main = vertex
        self.tensors = []
        
    def print_self(self):
        for t in self.tensors:
            if t.is_cotensor():
                print "Cotensor: {0}".format(t)
                print t.arrow
            else:
                print "Tensor: {0}".format(t)
            print "Hypotheses:"
            for hv in t.get_hypotheses():
                print hv
                print "h:{0},c:{1}\n".format(hv.hypothesis,hv.conclusion)
            print "Conclusions:"
            for cv in t.get_conclusions():
                print cv
                print "h:{0},c:{1}\n".format(cv.hypothesis,cv.conclusion)
        
    def add_tensor(self, tensor):
        #self.tensors[:0] = [tensor]
        self.tensors.append(tensor)
        tensor.alpha = 't' + chr(len(self.tensors) + 96)
                
    def toTeX(self):
        # Erase file
        f = open('formula.tex', 'w')
        f.close()
        
        # Write to formula.tex
        # Header
        f = open('formula.tex', 'a')
        f.write('\documentclass[class=minimal,border=0pt]{standalone}\n\n')
        f.write('\usepackage{tikz-qtree}\n')
        f.write('\usepackage{stmaryrd}\n\n')
        f.write('\\begin{document}\n\n')
        
        # Tikzpicture
        f.write('\\begin{tikzpicture}[scale=.8,')
        f.write('cotensor/.style={minimum size=2pt,fill,draw,circle},\n')
        f.write('tensor/.style={minimum size=2pt,fill=none,draw,circle},')
        f.write('sibling distance=1.5cm,level distance=1cm,auto]\n\n')

        x = 2
        y = 1
        
        if not self.tensors:
            f.write(self.main.toTeX(x, y, self.main))
        
        for t in self.tensors:
            
            f.write('{0} at ({1},{2}) {{}};\n'.format(t.toTeX(),x,y))
            f.write(t.hypotheses_to_TeX(x, y))
            f.write(t.conclusions_to_TeX(x, y))
            if t.is_cotensor():
                f.write("\draw[->] ({0}) -- ({1});\n".format(t.alpha,t.arrow))
            y += 3
                
        f.write('\n\end{tikzpicture}\n\n')
        
        # End of document
        f.write('\end{document}')
        f.close()

        
# This returns True if the formula contains no connectives.   
def simple_formula(formula):
    connectives = re.compile(r"(\*|\\|/|\(\*\)|\(/\)|\(\\\))")
    search = connectives.search(formula)
    return search is None        
   
   
# Flip the hypothesis boolean     
def flip_hypo(hypothesis):
    return (hypothesis + 1) % 2
        

def operators_to_TeX(string):
    string = string.replace("\\", "\\backslash ")
    string = string.replace("(*)", "\oplus ")
    string = string.replace("*", "\otimes ")
    string = string.replace("(/)", "\oslash ")
    string = string.replace("(\\backslash )", "\obslash ")
    return string
        
        
def type(connective, hypo):
    types = {
        # LIRa figure 3
        # (con,hypo):(premise#,geometry)
        # geometry: (f)ormula,(l)eft,(r)ight,(<)arrow to previous
       
        # Fusion connectives - hypothesis
        ("/",1):(2,"frl"),
        ("*",1):(1,"f<lr"),
        ("\\",1):(2,"lfr"),
        # Fusion connectives - conclusion
        ("/",0):(1,"lf<r"),
        ("*",0):(2,"lrf"),
        ("\\",0):(1,"rlf<"),
        # Fission connectives - hypothesis
        ("(/)",1):(2,"f<rl"),
        ("(*)",1):(1,"flr"),
        ("(\\)",1):(2,"lf<r"),
        # Fission connectives - conclusion
        ("(/)",0):(1,"lfr"),
        ("(*)",0):(2,"lrf<"),
        ("(\\)",0):(1,"rlf")        
    }
    return types[(connective, hypo)]    

    
class Vertex:

    def __init__(self, formula=None, hypo=None):
        global vertices
        self.set_hypothesis(None)
        self.set_conclusion(None)
        self.alpha = chr(vertices + 97)
        vertices += 1
        if formula is not None:
            self.main = formula
            self.link(formula, hypo)
            
    def set_hypothesis(self, hypo):
        self.hypothesis = hypo
        
    def set_conclusion(self, con):
        self.conclusion = con
        
    def toTeX(self, x, y, tensor):  
        label = operators_to_TeX(self.main)
        line = "\draw ({0}) -- ({1});\n".format(tensor.alpha,self.alpha)
        return "\\node ({0}) at ({1},{2}) {{${3}$}};\n".format(self.alpha, 
                x, y, label) + line
        
    # LIRa example 2    
    def type(self):
        if isinstance(self.hypothesis, Tensor):
            if isinstance(self.conclusion, Tensor):
                return 'internal'
            else:
                return 'conclusion'
        elif isinstance(self.conclusion, Tensor):
            return 'hypothesis'
        else:
            return 'both'
            
    def link(self, label, hypo):
        if hypo:
            self.set_hypothesis(label)
        else:
            self.set_conclusion(label)
            
    # This is the source of the recursion        
    def unfold(self, formula, hypo, structure):
        regexp = re.compile(
        r"""(\(.+\)|[\w']+)                     #left formula
            (\*|\\|/|\(\*\)|\(/\)|\(\\\))       #main connective
            (\(.+\)|[\w']+)$                    #right formula
        """, re.X)
        search = regexp.match(formula)
        (left, connective, right) = search.groups()
        (h, geometry) = type(connective,hypo)
        if h == 1:
            structure.add_tensor(OnePremise(left, right, 
                                    geometry, self, structure))
        else:
            structure.add_tensor(TwoPremise(left, right, 
                                    geometry, self, structure))

              
class Tensor:

    def __init__(self):
        print "error"
        
    def toTeX(self):
        co = ''
        if self.is_cotensor():
            co = 'co'
        return '\\node [{0}tensor] ({1})'.format(co,self.alpha)
        
    def parse_geometry(self, geometry, vertex):
        index = geometry.find("<")
        if index > -1:
            self.arrow = vertex.alpha
        geometry = geometry.replace("<", "")
        return geometry
        
    def get_lookup(self, left, right, vertex):
        lookup = {
            'f':(Tensor.link,vertex),
            'l':(Tensor.eval_formula,left),
            'r':(Tensor.eval_formula,right)
        }
        return lookup
        
    def set_structure(self, struc):
        self.structure = struc
        
    def is_cotensor(self):
        return hasattr(self, 'arrow')
        
    def link(self, vertex, hypo):
        flipped_hypo = flip_hypo(hypo)
        vertex.link(self, flipped_hypo)
        return vertex
        
    def eval_formula(self, part, hypo):
        if simple_formula(part):
            return self.link(Vertex(part, hypo), hypo)
        else:
            vertex = Vertex()
            vertex.main = "."  
            self.link(vertex, hypo)
            part = part[1:-1]
            flipped_hypo = flip_hypo(hypo)
            vertex.unfold(part, flipped_hypo, self.structure)
            return vertex
            
  
class OnePremise(Tensor):

    def __init__(self, left, right, geometry, vertex, struc):
        self.index = Tensor.set_structure(self, struc)
        geometry = Tensor.parse_geometry(self, geometry, vertex)
        lookup = Tensor.get_lookup(self, left, right, vertex)
        (function,arg) = lookup[geometry[0]]
        self.top = function(self, arg, 1)
        (function,arg) = lookup[geometry[1]]
        self.bottomLeft = function(self, arg, 0)
        (function,arg) = lookup[geometry[2]]
        self.bottomRight = function(self, arg, 0)
        
    def get_hypotheses(self):
        return [self.top]
        
    def get_conclusions(self):
        return [self.bottomLeft, self.bottomRight]
        
    def num_hyp(self):
        return 1
    
    def num_con(self):
        return 2
        
    def hypotheses_to_TeX(self, x, y):
        return self.top.toTeX(x, y + 1, self)
        
    def conclusions_to_TeX(self, x, y):
        s1 = self.bottomLeft.toTeX(x - 1, y - 1, self)
        s2 = self.bottomRight.toTeX(x + 1, y - 1, self)
        return s1 + s2
    
    
class TwoPremise(Tensor):

    def __init__(self, left, right, geometry, vertex, struc):
        self.index = Tensor.set_structure(self, struc)
        geometry = Tensor.parse_geometry(self, geometry, vertex)
        lookup = Tensor.get_lookup(self, left, right, vertex)
        (function,arg) = lookup[geometry[0]]
        self.topLeft = function(self, arg, 1)
        (function,arg) = lookup[geometry[1]]
        self.topRight = function(self, arg, 1)
        (function,arg) = lookup[geometry[2]]
        self.bottom = function(self, arg, 0)
        
    def get_hypotheses(self):
        return [self.topLeft, self.topRight]
        
    def get_conclusions(self):
        return [self.bottom]
      
    def num_hyp(self):
        return 2
    
    def num_con(self):
        return 1
        
    def hypotheses_to_TeX(self, x, y):
        s1 = self.topLeft.toTeX(x - 1, y + 1, self)
        s2 = self.topRight.toTeX(x + 1, y + 1, self)
        return s1 + s2
    
    def conclusions_to_TeX(self, x, y):
        return self.bottom.toTeX(x, y - 1, self)
  
  
# By default the formula appears in hypothesis position.  
def unfold_formula(formula, hypothesis=1):
    vertex = Vertex(formula, hypothesis)
    structure = ProofStructure(formula, vertex)
    if not simple_formula(formula):
        vertex.unfold(formula, hypothesis, structure)     # Recursively unfold
    return structure

def main():
    p = argparse.ArgumentParser(  
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent('''\
    Lexical unfolding of proof structures for LG
    Formula language:
            A,B ::= p |             atoms (use alphanum)
            A*B | B\A | A/B |       product
            A(*)B | A(/)B | A(\)B   coproduct'''),
                                usage = 'proofnet.py [options] formula')
    p.add_argument('formula', metavar='F', type=str, nargs='+',
                   help='a formula in LG to unfold')
    p.add_argument('--tex', '-t', action = 'store_true', 
                help = 'print result to LaTeX')
    p.add_argument('--conclusion', '-c', action = 'store_true',
                help = 'conclusion unfolding instead of hypothesis unfolding')
    arguments = p.parse_args()
    if len(arguments.formula) != 1:
        p.print_help()
        sys.exit()
    formula = arguments.formula[0]
    hypothesis = not arguments.conclusion
    structure = unfold_formula(formula,hypothesis)
    structure.print_self()  # for debugging
    if arguments.tex:
        structure.toTeX()
        os.system('pdflatex formula.tex')
        if platform.system() == 'Windows':
            os.system('start formula.pdf')
        elif platform.system() == 'Linux':
            os.system('pdfopen --file formula.pdf')
        # Mac OS X ?
         
if __name__ == '__main__':
    main()     
  