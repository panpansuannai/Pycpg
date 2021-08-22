import graphviz
from proc_anchor import Anchor, AnchorGraph, Position, GenAnchorGraph
from args_parser import Config
from proc_struct import *

class GenDotName(object):
    prefix = 'anchor'
    counter = 0
    def __init__(self):
        raise ValueError("GenDotName can't be instantiated")

    @classmethod
    def new_name(cls, prefix=None) -> str:
        cls.counter = cls.counter + 1
        if prefix is None:
            return cls.prefix + str(cls.counter)
        else:
            return prefix + str(cls.counter)

class DotNodeAttrs(object):
    default = {'shape': 'box'}
    def __init__(self, **kwargs):
        self._attrs = self.default.copy()
        if kwargs is not None:
            self._attrs.update(kwargs)

    def get_attrs(self):
        return self._attrs
    
    @property
    def attrs(self):
        return self._attrs

class GenProceduralGraph(object):
    dot = graphviz.Digraph()
    anchor_names = {}
    graph_attrs = {'splines':'ortho'}
    def __inif__(self):
        raise ValueError("GenProceduralGraph can't be instantiated")
    
    @classmethod
    def generate(cls, anchors):
        if isinstance(anchors, Anchor):
            return cls.generate_anchor(anchors)
        elif isinstance(anchors, AnchorGraph):
            return cls.generate_anchor_graph(anchors)
        return None
    
    @classmethod
    def generate_anchor(cls, anchor: Anchor):
        if anchor not in cls.anchor_names.keys():
            name = GenDotName.new_name(anchor.body)
            if anchor.body is None:
                attrs = DotNodeAttrs(shape='point')
                print(attrs.attrs)
                cls.dot.node(name, '', attrs.attrs)
            else:
                attrs = DotNodeAttrs()
                print(attrs.attrs)
                cls.dot.node(name, anchor.body, attrs.attrs)
            cls.anchor_names[anchor] = (name, name)
        return anchor

    @classmethod
    def get_anchor_graph_in_out_name(cls, anchors: AnchorGraph) -> tuple[str, str]:
        in_name, _ = cls.anchor_names[anchors.anchor_in()]
        _, out_name = cls.anchor_names[anchors.anchor_out()]
        return (in_name, out_name)

    @classmethod
    def generate_anchor_graph(cls, anchors: AnchorGraph):
        anchors_list = [[cls.generate(anchors.positional_get(Position(i, j))) for i in range(anchors.colum)]
                for j in range(anchors.rows)]
        for i in anchors_list:
            for anchor in i:
                if anchor is not None:
                    _, anc_out = cls.anchor_names[anchor]
                    for anc in anchor.nexts:
                        other_in, _ = cls.anchor_names[anc]
                        cls.dot.edge(anc_out, other_in)
        cls.anchor_names[anchors] = cls.get_anchor_graph_in_out_name(anchors)
        return anchors

    @classmethod
    def render(cls, config: Config):
        cls.dot.attr('graph', cls.graph_attrs)
        if config is None:
            cls.dot.render(filename='output', format='png')
        else:
            cls.dot.render(filename=config.output_file, format=config.output_type)

    @classmethod
    def test(cls):
        #cls.test_if()
        cls.test_while()

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
        graph = GenAnchorGraph.generate(struct)
        gen = cls()
        print(gen.generate(graph))
        config = Config(None, 'while', 'svg')
        gen.render(config)

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
        graph = GenAnchorGraph.generate(struct)
        gen = cls()
        print(gen.generate(graph))
        config = Config(None, 'if', 'svg')
        gen.render(config)

def test_mode():
    return __name__ == '__main__'

def test_main():
    GenProceduralGraph.test()

if test_mode():
    test_main()
