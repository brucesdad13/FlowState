import bge
from scripts.gameUtils import utils
logic = bge.logic
logic.utils = utils()

logic.loadGlobalDict()

logic.globalDict['sceneHistory'] = []
logic.utils.setDefaultState()
logic.saveGlobalDict()
logic.utils.setMode(logic.utils.MODE_MENU)