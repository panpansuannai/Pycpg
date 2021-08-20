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

    @property
    def body(self):
        return self._body

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

    def size(self):
        return len(self._structs)

    def __iter__(self):
        return self._structs.__iter__()

class IfStructBody(object):
    def __init__(self, block: StructsBlock):
        self._block = block
    @property
    def block(self):
        return self._block

class IfStruct(LinkedStruct):
    def __init__(self, condition: LinkedStruct, yes_block: IfStructBody):
        self._condition = condition
        self._yes_block = yes_block
    @property
    def condition(self):
        return self._condition
    @property
    def yes_block(self):
        return self._yes_block.block

class WhileStructBody(object):
    def __init__(self, block: StructsBlock):
        self._block = block
    @property
    def block(self):
        return self._block

class WhileStruct(LinkedStruct):
    def __init__(self, condition: LinkedStruct, loop_block: WhileStructBody):
        super().__init__()
        self._condition = condition
        self._loop_body = loop_block

    @property
    def condition(self):
        return self._condition
    @property
    def loop_block(self):
        return self._loop_body.block

@singleton
class START(LinkedStruct, BodyStruct):
    def __init__(self):
        BodyStruct.__init__(self, 'Start')
        LinkedStruct.__init__(self)
    
@singleton
class END(BodyStruct):
    def __init__(self):
        BodyStruct.__init__(self, 'End')