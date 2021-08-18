from decorator import singleton

class GraphAttrs(object):
    def __init__(self):
        self._attrs = {}

    def add_attr(self, name: str, value: str):
        self._attrs[name] = value

class Arc(GraphAttrs):
    def __init__(self):
        super().__init__()

class DiArc(Arc):
    def __init__(self):
        super().__init__()
        
class HasBody(object):
    def __init__(self, body: str):
        self._body = body

    def merge_body(self, other):
        self._body = self._body + ' ' + other._body

''' Struct with a anchor point can link to other struct,
    for example:
        ◎------>
        ^
        ```anchor```
    
      -------
     |  xxx  |--------◎  <---- ```anchor```
      -------         |
      -------         |
     |  xxx  |<-------◎  <---- ```anchor```
      ------- 
         ^
         |___________ ```HasBody and has anchor```
'''
class LinkedStruct(GraphAttrs):
    def __init__(self):
        super().__init__()

    def link_to(self, next, arc: Arc = None):
        self._next = next
        self._next_arc = arc

''' Struct owned body that can be drawed in graphviz ,
    for example: 
         ----------
        |  a > 10  |
         ----------
'''
class BodyStruct(HasBody):
    def __init__(self, body):
        HasBody.__init__(self, body)

''' A structure container that hold many structures '''
class StructsBlock(object):
    def __init__(self):
        self._structs = []

    def add_struct(self, struct):
        self._structs.append(struct)

class IfStructBody(object):
    def __init__(self, block: StructsBlock):
        self._block = block

class IfStruct(LinkedStruct):
    def __init__(self, condition: LinkedStruct, yes_block: IfStructBody):
        self._condition = condition
        self._yes_block = yes_block

class WhileStructBody(object):
    def __init__(self, block: StructsBlock):
        self._block = block

class WhileStruct(LinkedStruct):
    def __init__(self, condition: LinkedStruct, loop_block: WhileStructBody):
        super().__init__()
        self._condition = condition

@singleton
class START(LinkedStruct, BodyStruct):
    def __init__(self):
        BodyStruct.__init__(self, 'Start')
        LinkedStruct.__init__(self)
    
@singleton
class END(BodyStruct):
    def __init__(self):
        BodyStruct.__init__(self, 'End')