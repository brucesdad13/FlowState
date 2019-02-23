import bge
import time
logic = bge.logic
owner = logic.getCurrentController().owner

for child in owner.children:
    if 'Text' in child:
        if 'metadata' in owner:
            if "checkpoint order" in owner['metadata']:
                child['Text'] = str(owner['metadata']["checkpoint order"])