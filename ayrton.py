#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# NOTE: try to keep this module as bare as possible
# no useless imports, no prints, definetely no logging...
# any new line makes it more difficult to debug with python's state machine

import os
import sys
import sh
import importlib
import builtins

class Runner (object):
    # this class changes the behaviour of sh.Command
    # so is more shell scripting freindly
    def __init__ (self, exe):
        self.exe= exe

    def __call__ (self, args):
        os.system ("%s %s" % (self.exe, args))

def polute (d):
    # these functions will be loaded from each module and put in the globals
    builtins= dict (
        os= [ 'chdir', 'getcwd', 'uname', 'chmod', 'chown', 'link', 'listdir', 'mkdir', 'remove' ],
        time= [ 'sleep', ],

        file_test= [ '_a', '_b', '_c', '_d', '_e', '_f', '_g', '_h', '_k', '_p',
                     '_r', '_s', '_u', '_w', '_x', '_L', '_N', '_S', '_nt', '_ot' ],
        )

    for module, functions in builtins.items ():
        m= importlib.import_module (module)
        for function in functions:
            d[function]= getattr (m, function)

class Namespace (dict):
    def __init__ (self):
        super ().__init__ ()
        polute (self)

    def __getitem__ (self, k):
        try:
            ans= getattr (builtins, k)
        except AttributeError:
            try:
                ans= super ().__getitem__ (k)
            except KeyError:
                ans= Runner (k)

        return ans

if __name__=='__main__':
    script= compile (file (sys.argv[1]).read (), sys.argv[1], 'exec')
    n= Namespace ()
    # we have to toy with the argv
    n['sys']= sys
    sys.argv.pop (0)

    # fire!
    exec (s, n)
