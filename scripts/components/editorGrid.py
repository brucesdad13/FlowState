import bge
from collections import OrderedDict

if not hasattr(bge, "__component__"):
    # Put shared definitions here executed only in game engine.
    # e.g:
    # scene = bge.logic.getCurrentScene()
    logic = bge.logic

class visibility(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
        ("Unit", {"meters", "feet"}),
    ])

    def start(self, args):
        self.visible = False
        self.units = args['Unit']

    def update(self):
        if(self.units == "meters"):
            if(logic.utils.getMapEditor().unitsMetric):
                self.object.visible = True
            else:
                self.object.visible = False
        else:
            if(not logic.utils.getMapEditor().unitsMetric):
                self.object.visible = True
            else:
                self.object.visible = False
