import bge
from scripts.gameUtils import utils
logic = bge.logic
try:
    logic.utils
except:
    print("WARNING GAME STATE WAS INVALID!")
    logic.utils = utils()
    logic.loadGlobalDict()
    logic.globalDict['sceneHistory'] = []
    logic.utils.setDefaultState()
    logic.saveGlobalDict()
    logic.utils.log("Utils created")
