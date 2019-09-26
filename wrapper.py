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
        input("Press enter to relaunch the script, CTRL-C to exit")
        print("Reloading Program...")
        importlib.reload(FileManager)
        importlib.reload(LexicalSimplifier)
        importlib.reload(StopwordRemover)
        importlib.reload(POSTagger)
        importlib.reload(SyntacticSimplifier)
        importlib.reload(simplifier)