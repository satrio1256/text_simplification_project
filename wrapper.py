import sys
import simplifier
import FileManager
import LexicalSimplifier
import StopwordRemover
import SyntacticSimplifier
import POSTagger
import importlib

import traceback
import logging

sv = None
wv = None
if __name__ == "__main__":
    while True:
        if not sv:
            sv = simplifier.loadSense()
            wv = simplifier.loadWord2Vec()
        try:
            simplifier.calculate(sv, wv)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logging.error(traceback.format_exc())
        print("Press enter to relaunch the script, CTRL-C to exit")
        sys.stdin.readline()
        print("Loading FileManager")
        importlib.reload(FileManager)
        print("Loading LexicalSimplifier")
        importlib.reload(LexicalSimplifier)
        print("Loading StopwordRemover")
        importlib.reload(StopwordRemover)
        print("Loading POSTagger")
        importlib.reload(POSTagger)
        print("Loading Syntactic Simplifier")
        importlib.reload(SyntacticSimplifier)
        print("Loading Simplifier")
        importlib.reload(simplifier)