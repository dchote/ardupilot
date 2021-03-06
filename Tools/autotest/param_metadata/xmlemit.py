#!/usr/bin/env python

from xml.sax.saxutils import escape, quoteattr

from param import *
from emit import Emit

# Emit APM documentation in an machine readable XML format
class XmlEmit(Emit):
    
    def __init__(self):
        wiki_fname = 'apm.pdef.xml'
        self.f = open(wiki_fname, mode='w')
        preamble = '''<?xml version="1.0" encoding="utf-8"?>
        <!-- Dynamically generated list of documented parameters (generated by param_parse.py) -->    
        <paramfile>
        <vehicles>
        '''
        self.f.write(preamble)
    
    def close(self): 
        self.f.write('</libraries>')
        self.f.write('''</paramfile>\n''')
        self.f.close
        
    def emit_comment(self, s):
        self.f.write("<!-- " + s + " -->")

    def start_libraries(self):
        self.f.write('</vehicles>')
        self.f.write('<libraries>')
    
    def emit(self, g, f):
        t = '''<parameters name=%s>\n'''  % quoteattr(g.name) # i.e. ArduPlane
        
        for param in g.params:
            # Begin our parameter node
            if hasattr(param, 'DisplayName'):   
                t += '<param humanName=%s name=%s ' % (quoteattr(param.DisplayName),quoteattr(param.name)) # i.e. ArduPlane (ArduPlane:FOOPARM)
            else:
                t += '<param name=%s ' % quoteattr(param.name)
                    
            if hasattr(param, 'Description'):   
                t += 'documentation=%s' % quoteattr(param.Description) # i.w. parameter docs
            
            t += ">\n"
            
            # Add values as chidren of this node
            for field in param.__dict__.keys():
                if field not in ['name', 'DisplayName', 'Description', 'User'] and field in known_param_fields:
                    if field == 'Values' and Emit.prog_values_field.match(param.__dict__[field]):
                        t+= "<values>\n"
                        
                        values = (param.__dict__[field]).split(',')
                        for value in values:
                            v = value.split(':')
                            t+='''<value code=%s>%s</value>\n''' % (quoteattr(v[0]), escape(v[1])) # i.e. numeric value, string label
                            
                        t += "</values>\n"
                    else:
                        t += '''<field name=%s>%s</field>\n''' % (quoteattr(field), escape(param.__dict__[field])) # i.e. Range: 0 10
            
            t += '''</param>\n'''
        t += '''</parameters>\n'''
                        
        #print t
        self.f.write(t)
    


