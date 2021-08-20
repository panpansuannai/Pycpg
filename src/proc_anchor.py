from proc_struct import *
import graphviz

class Position(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property 
    def x(self):
        return self._x
    @property 
    def y(self):
        return self._y
    def copy(self):
        return Position(self.x, self.y)

    @classmethod
    def test(cls):
        pos = Position(10, 1)
        assert pos.x == 10 and pos.y == 1
        pos = Position(-1, 0)
        assert pos.x == -1 and pos.y == 0


class OneLink(object):
    def __init__(self):
        self._next = None

    @property
    def next(self):
        return self._next

    def link_to(self, other):
        self._next = other

    @classmethod
    def test(cls):
        link = OneLink()
        link.link_to(None)
        assert link.next is None
        link.link_to(10)
        assert link.next == 10

class MultiLink(object):
    def __init__(self):
        self._next = []

    @property
    def nexts(self):
        return self._next

    def link_to(self, other):
        self._next.append(other)
    @classmethod
    def test(cls):
        link = MultiLink()
        link.link_to(None)
        assert len(link.nexts) == 1
        link.link_to(10)
        assert len(link.nexts) == 2
        assert link.nexts[0] is None
        assert link.nexts[1] == 10

class AnchorGraph(object):
    def __init__(self, rows, colum, anchor_in: Position, anchor_out: Position):
        if anchor_in.x != anchor_out.x:
            ''' Todo: more link method '''
            raise ValueError("AnchorGraph's in and out anchor must with the same x")
        self._rows = rows
        self._colum = colum
        self._anchors = [[None for i in range(colum)] for j in range(rows)]
        self._in = anchor_in.copy()
        self._out = anchor_out.copy()

    @property
    def rows(self):
        return self._rows
    @property
    def colum(self):
        return self._colum

    def anchor_in(self):
        ''' Return the input anchor of a AnchorGraph '''
        return self.positional_get(self._in).anchor_in()

    def anchor_out(self):
        ''' Return the output anchor of a AnchorGraph '''
        return self.positional_get(self._out).anchor_out()
    
    def overall_link(self, next):
        if not isinstance(next, AnchorGraph):
            raise ValueError("AnchorGraph only supported to link AnchorGraph")
        self.anchor_out().overall_link(next.anchor_in())

    def positional_link(self, from_pos: Position, to_pos: Position):
        if (self.positional_get(from_pos) is None 
            or self.positional_get(to_pos) is None):
            raise ValueError("Can not link None anchor")
        self.positional_get(from_pos).overall_link(self.positional_get(to_pos))

    def serial_link(self, lst: list):
        last_pos = None
        for i in lst:
            if last_pos is not None:
                self.positional_link(last_pos, i)
            last_pos = i

    def positional_set(self, position, anchor):
        self._anchors[position.y][position.x] = anchor

    def positional_get(self, position):
        return self._anchors[position.y][position.x]

    def serial_set(self, lst: list):
        for i, anchor in enumerate(lst):
            self.positional_set(Position(i % self.colum, i // self.colum),
                                anchor)
    @classmethod
    def test(cls):
        graph = AnchorGraph(3, 3, Position(0, 0), Position(0, 2))
        assert graph.colum == 3
        assert graph.rows == 3
        graph.serial_set([Anchor("({}, {})".format(j, i)) for i in range(3) for j in range(3)])
        assert graph.anchor_in() == graph.positional_get(Position(0, 0))
        assert graph.anchor_out() == graph.positional_get(Position(0, 2))
        assert graph.positional_get(Position(0, 0)).body == "(0, 0)"
        assert graph.positional_get(Position(2, 2)).body == "(2, 2)"
        graph.positional_link(Position(0, 0),Position(0, 1))
        assert graph.positional_get(Position(0, 0)).next() == graph.positional_get(Position(0, 1))

class Anchor(AnchorGraph):
    def __init__(self, body, link=OneLink()):
        AnchorGraph.__init__(self, 1,1,Position(0,0), Position(0,0))
        self._link = link
        self._body = body

    @property
    def body(self):
        return self._body

    def overall_link(self, other):
        if not isinstance(other, Anchor) and not isinstance(other, AnchorGraph):
            raise ValueError("Anchor only supported to link to Anchor or AnchorGraph")
        self._link.link_to(other.anchor_in)

    def anchor_in(self):
        ''' Return the input anchor of an Anchor,
            that is itself '''
        return self

    def anchor_out(self):
        ''' Return the output anchor of an Anchor,
            that is itself '''
        return self
    def next(self):
        if not isinstance(self._link, OneLink):
            raise ValueError("next can only be called while self._link is OneLink")
        return self._link.next()
    def nexts(self):
        if not isinstance(self._link, MultiLink):
            raise ValueError("nexts can only be called while self._link is MultiLink")
        return self._link.nexts()

    @classmethod
    def test(cls):
        anchor = Anchor("body")
        assert anchor.body == "body"
        assert anchor.anchor_in() is anchor
        assert anchor.anchor_out() is anchor
        other = Anchor("other")
        anchor.overall_link(other)
        assert anchor.next() == other

class GenAnchorGraph(object):
    @classmethod
    def generate(cls, struct):
        if isinstance(struct, WhileStruct):
            return cls.generate_while_anchors(struct)
        elif isinstance(struct, IfStruct):
            return cls.generate_if_anchors(struct)
        elif isinstance(struct, BodyStruct):
            return cls.generate_body_anchors(struct)
        elif isinstance(struct, StructsBlock):
            return cls.genrate_block_anchors(struct)
        else:
            raise ValueError("Unsupport struct")

    @classmethod
    def genrate_block_anchors(cls, block: StructsBlock) -> AnchorGraph:
        rows, colum = (block.size(), 1)
        anchors = AnchorGraph(rows, colum, Position(0, 0), Position(0, colum - 1))
        anchors.serial_set([GenAnchorGraph.generate(struct) for struct in block])
        anchors.serial_link([Position(0, i) for i in range(colum)])
        return anchors

    @classmethod
    def generate_while_anchors(cls, wstruct: WhileStruct) -> AnchorGraph:
        ''' TODO: Support break statement '''
        '''
        While Statement:
            ^ : condition anchor
            ⌂ : loop body item
            O : end anchor

        ◎   >  ^   >  ◎
               |
        |      ⌂      
               |      | 
        ◎   <  ◎      

               O   <  ◎
        '''
        rows, colum = (4, 3)
        anchors = AnchorGraph(rows, colum, Position(1, 0), Position(1, 3))
        lst = [Anchor(None), Anchor(wstruct.condition.body, MultiLink()), Anchor(None),
               None, GenAnchorGraph.generate(wstruct.loop_block), None,
               Anchor(None), Anchor(None), None,
               None, Anchor(None), Anchor(None)]
        anchors.serial_set(lst)
        anchors.serial_link([Position(1, 0), Position(1, 1),Position(1, 2),Position(0, 2),
                             Position(0, 0), Position(1, 0),Position(2, 0), Position(2, 3),
                             Position(1, 3)])
        return anchors
    @classmethod
    def generate_if_anchors(cls, ifstruct: IfStruct) -> AnchorGraph:
        '''
        If Statement:
            ^ : condition
            ⌂ : body
            O : end anchor

        ^      ◎   |    ^   >  ◎
                   |           | 
        ⌂          |    |      ⌂       
                   |           | 
        O      ◎   |    O   <  ◎
        '''
        rows, colum = (3, 2)
        anchors = AnchorGraph(rows, colum, Position(0, 0), Position(0, 2))
        lst = [Anchor(ifstruct.condition.body, MultiLink()), Anchor(None),
               None, GenAnchorGraph.generate(ifstruct.yes_block),
               Anchor(None), Anchor(None)]
        anchors.serial_set(lst)
        anchors.serial_link([Position(0, 0), Position(1, 0), Position(1, 1),
                             Position(1, 2), Position(0, 2)])
        anchors.positional_link(Position(0, 0), Position(0, 2))
        return anchors

    @classmethod
    def generate_body_anchors(cls, bodystruct: BodyStruct):
        anchor = Anchor(bodystruct.body)
        return anchor
    @classmethod
    def test(cls):
        cls.test_body()
        cls.test_if()
        cls.test_while()
        cls.test_block()

    @classmethod
    def test_body(cls):
        struct = BodyStruct("Hello")
        anchor = cls.generate(struct)
        assert isinstance(anchor, Anchor)
        assert anchor.body == "Hello"

    @classmethod
    def test_if(cls):
        block = StructsBlock()
        block.add_struct(BodyStruct("first"))
        block.add_struct(BodyStruct("second"))
        block.add_struct(BodyStruct("third"))
        block.add_struct(BodyStruct("fourth"))
        block.add_struct(BodyStruct("fifth"))
        block.add_struct(BodyStruct("sixth"))
        block = IfStructBody(block)
        cond = BodyStruct("Condition")
        struct = IfStruct(cond, block)
        graph = cls.generate(struct)
        assert isinstance(graph, AnchorGraph)
        assert graph.positional_get(Position(0, 0)).body == "Condition"
        assert graph.anchor_in().body == "Condition"
        assert graph.anchor_out() is graph.positional_get(Position(0, 2))

    @classmethod
    def test_while(cls):
        block = StructsBlock()
        block.add_struct(BodyStruct("first"))
        block.add_struct(BodyStruct("second"))
        block.add_struct(BodyStruct("third"))
        block.add_struct(BodyStruct("fourth"))
        block.add_struct(BodyStruct("fifth"))
        block.add_struct(BodyStruct("sixth"))
        block = WhileStructBody(block)
        cond = BodyStruct("Condition")
        struct = WhileStruct(cond, block)
        graph = cls.generate(struct)
        assert isinstance(graph, AnchorGraph)
        assert graph.positional_get(Position(1, 0)).body == cond.body
        assert graph.anchor_in().body == cond.body
        assert graph.anchor_out().body == graph.positional_get(Position(1, 3)).body

    @classmethod
    def test_block(cls):
        block = StructsBlock()
        block.add_struct(BodyStruct("first"))
        block.add_struct(BodyStruct("second"))
        block.add_struct(BodyStruct("third"))
        block.add_struct(BodyStruct("fourth"))
        block.add_struct(BodyStruct("fifth"))
        block.add_struct(BodyStruct("sixth"))
        graph = cls.generate(block)
        assert isinstance(graph, AnchorGraph)
        assert graph.positional_get(Position(0, 0)) is graph.anchor_in()


def test_mode():
    return __name__ == '__main__'

def test_main():
    green = "\033[32m"
    normal = "\033[0m"
    Position.test()
    OneLink.test()
    MultiLink.test()
    Anchor.test()
    AnchorGraph.test()
    GenAnchorGraph.test()
    print(green + "Pass all test cases" + normal)

if test_mode():
    test_main()

