import enum
import xml.etree.ElementTree as ET
import datetime


class LineType(enum.Enum):
    SOLID = 1
    DASH = 2
    DOTS = 3
    ZIGZAG = 4


class NodeShape(enum.Enum):
    ROUND_RECTANGLE = 1


class Network:
    __NETWORK_NODE_LABEL_SELECTION: bool = False
    __NETWORK_HEIGHT: float = 400.0
    __NETWORK_ANNOTATION_SELECTION: bool = False
    __NETWORK_NODE_SELECTION: bool = True
    __NETWORK_DEPTH: float = 0.0
    __NETWORK_SIZE: float = 550.0
    __NETWORK_SCALE_FACTOR: float = 1.0
    __NETWORK_WIDTH: float = 550.0
    __NETWORK_CENTER_X_LOCATION: float = 0.0
    __NETWORK_FORCE_HIGH_DETAIL: bool = False
    __NETWORK_EDGE_SELECTION: bool = True
    __NETWORK_TITLE: str = ""
    __NETWORK_CENTER_Y_LOCATION: float = 0.0
    __NETWORK_CENTER_Z_LOCATION: float = 0.0
    __NETWORK_BACKGROUND_PAINT: str = '#FFFFFF'

    def __init__(self):
        pass

    def generate(self) -> dict:
        return {
            'network': {
                'visualProperty': [
                    {
                        'default': self.__NETWORK_NODE_LABEL_SELECTION,
                        'name': 'NETWORK_NODE_LABEL_SELECTION'
                    },
                    {
                        'default': self.__NETWORK_HEIGHT,
                        'name': 'NETWORK_HEIGHT'
                    },
                    {
                        'default': self.__NETWORK_ANNOTATION_SELECTION,
                        'name': 'NETWORK_ANNOTATION_SELECTION'
                    },
                    {
                        'default': self.__NETWORK_NODE_SELECTION,
                        'name': 'NETWORK_NODE_SELECTION'
                    },
                    {
                        'default': self.__NETWORK_DEPTH,
                        'name': 'NETWORK_DEPTH'
                    },
                    {
                        'default': self.__NETWORK_SIZE,
                        'name': 'NETWORK_SIZE'
                    },
                    {
                        'default': self.__NETWORK_SCALE_FACTOR,
                        'name': 'NETWORK_SCALE_FACTOR'
                    },
                    {
                        'default': self.__NETWORK_WIDTH,
                        'name': 'NETWORK_WIDTH'
                    },
                    {
                        'default': self.__NETWORK_CENTER_X_LOCATION,
                        'name': 'NETWORK_CENTER_X_LOCATION'
                    },
                    {
                        'default': self.__NETWORK_FORCE_HIGH_DETAIL,
                        'name': 'NETWORK_FORCE_HIGH_DETAIL'
                    },
                    {
                        'default': self.__NETWORK_EDGE_SELECTION,
                        'name': 'NETWORK_EDGE_SELECTION'
                    },
                    {
                        'default': self.__NETWORK_TITLE,
                        'name': 'NETWORK_TITLE'
                    },
                    {
                        'default': self.__NETWORK_CENTER_Y_LOCATION,
                        'name': 'NETWORK_CENTER_Y_LOCATION'
                    },
                    {
                        'default': self.__NETWORK_CENTER_Z_LOCATION,
                        'name': 'NETWORK_CENTER_Z_LOCATION'
                    },
                    {
                        'default': self.__NETWORK_BACKGROUND_PAINT,
                        'name': 'NETWORK_BACKGROUND_PAINT'
                    }
                ]
            }
        }


class Node:
    __NODE_X_LOCATION: float = 0.0
    __NODE_LABEL_COLOR: str = '#333333'
    __NODE_LABEL_WIDTH: float = 200.0
    __NODE_PAINT: str = '#1E90FF'
    __NODE_VISIBLE: bool = True
    __NODE_BORDER_STROKE: LineType = LineType.SOLID
    __NODE_BORDER_TRANSPARENCY: int = 255
    __NODE_LABEL_TRANSPARENCY: int = 255
    __NODE_NESTED_NETWORK_IMAGE_VISIBLE: bool = True
    __NODE_BORDER_WIDTH: float = 0.0
    __NODE_LABEL_FONT_SIZE: int = 12
    __NODE_LABEL: str = ''
    __NODE_FILL_COLOR: str = '#33FFFF'
    __NODE_BORDER_PAINT: str = '#006699'
    __COMPOUND_NODE_SHAPE: NodeShape = NodeShape.ROUND_RECTANGLE
    __NODE_Y_LOCATION: float = 0.0
    __NODE_Z_LOCATION: float = 0.0
    __NODE_WIDTH: float = 70.0
    __NODE_SELECTED: bool = False
    __NODE_DEPTH: float = 0.0
    __NODE_SIZE: float = 35.0
    __NODE_SHAPE: NodeShape = NodeShape.ROUND_RECTANGLE
    __COMPOUND_NODE_PADDING: float = 10.0

    def __init__(self):
        pass

    def generate(self):
        return {
            'node': {
                'dependency': [],
                'visualProperty': [
                    {
                        'default': self.__NODE_X_LOCATION,
                        'name': 'NODE_X_LOCATION'
                    },
                    {
                        'default': self.__NODE_LABEL_COLOR,
                        'name': 'NODE_LABEL_COLOR'
                    },
                    {
                        'default': self.__NODE_LABEL_WIDTH,
                        'name': 'NODE_LABEL_WIDTH'
                    },
                    {
                        'default': self.__NODE_PAINT,
                        'name': 'NODE_PAINT'
                    },
                    {
                        'default': self.__NODE_VISIBLE,
                        'name': 'NODE_VISIBLE'
                    },
                    {
                        'default': self.__NODE_BORDER_STROKE,
                        'name': 'NODE_BORDER_STROKE'
                    },
                    {
                        'default': self.__NODE_BORDER_TRANSPARENCY,
                        'name': 'NODE_BORDER_TRANSPARENCY'
                    },
                    {
                        'default': self.__NODE_LABEL_TRANSPARENCY,
                        'name': 'NODE_LABEL_TRANSPARENCY'
                    },
                    {
                        'default': self.__NODE_NESTED_NETWORK_IMAGE_VISIBLE,
                        'name': 'NODE_NESTED_NETWORK_IMAGE_VISIBLE'
                    },
                    {
                        'default': self.__NODE_BORDER_WIDTH,
                        'name': 'NODE_BORDER_WIDTH'
                    },
                    {
                        'default': self.__NODE_LABEL_FONT_SIZE,
                        'name': 'NODE_LABEL_FONT_SIZE'
                    },
                    {
                        'default': self.__NODE_LABEL,
                        'name': 'NODE_LABEL'
                    },
                    {
                        'default': self.__NODE_FILL_COLOR,
                        'name': 'NODE_FILL_COLOR'
                    },
                    {
                        'default': self.__NODE_BORDER_PAINT,
                        'name': 'NODE_BORDER_PAINT'
                    },
                    {
                        'default': self.__COMPOUND_NODE_SHAPE,
                        'name': 'COMPOUND_NODE_SHAPE'
                    },
                    {
                        'default': self.__NODE_Y_LOCATION,
                        'name': 'NODE_Y_LOCATION'
                    },
                    {
                        'default': self.__NODE_Z_LOCATION,
                        'name': 'NODE_Z_LOCATION'
                    },
                    {
                        'default': self.__NODE_WIDTH,
                        'name': 'NODE_WIDTH'
                    },
                    {
                        'default': self.__NODE_SELECTED,
                        'name': 'NODE_SELECTED'
                    },
                    {
                        'default': self.__NODE_DEPTH,
                        'name': 'NODE_DEPTH'
                    },
                    {
                        'default': self.__NODE_SIZE,
                        'name': 'NODE_SIZE'
                    },
                    {
                        'default': self.__NODE_SHAPE,
                        'name': 'NODE_SHAPE'
                    },
                    {
                        'default': self.__COMPOUND_NODE_PADDING,
                        'name': 'COMPOUND_NODE_PADDING'
                    }
                ]
            }
        }


class Edge:
    __EDGE_LABEL: str = ''
    __EDGE_PAINT: str = '#323232'
    __EDGE_LABEL_COLOR: str = '#000000'
    __EDGE_VISIBLE: bool = True
    __EDGE_WIDTH: float = 3.0
    __EDGE_LABEL_WIDTH: float = 200.0
    __EDGE_LINE_TYPE: LineType = LineType.SOLID

    def __init__(self):
        pass

    def generate(self):
        return {
            'edge': {
                'dependency': [],
                'visualProperty': [
                    {
                        'default': self.__EDGE_LABEL,
                        'name': 'EDGE_LABEL'
                    },
                    {
                        'default': self.__EDGE_PAINT,
                        'name': 'EDGE_PAINT'
                    },
                    {
                        'default': self.__EDGE_LABEL_COLOR,
                        'name': 'EDGE_LABEL_COLOR'
                    },
                    {
                        'default': self.__EDGE_VISIBLE,
                        'name': 'EDGE_VISIBLE'
                    },
                    {
                        'default': self.__EDGE_WIDTH,
                        'name': 'EDGE_WIDTH'
                    },
                    {
                        'default': self.__EDGE_LABEL_WIDTH,
                        'name': 'EDGE_LABEL_WIDTH'
                    },
                    {
                        'default': self.__EDGE_LINE_TYPE,
                        'name': 'EDGE_LINE_TYPE'
                    }
                ]
            }
        }


class VisualStyle:
    __name: str = "default"
    __network: Network
    __node: Node
    __edge: Edge

    def __init__(self, network: Network, node: Node, edge: Edge):
        self.__network = network
        self.__node = node
        self.__edge = edge

    def generate(self) -> dict:
        return {
            'name': self.__name,
            'network': self.__network.generate()['network'],
            'node': self.__node.generate()['node'],
            'edge': self.__edge.generate()['edge']
        }

    def changeName(self, name: str):
        self.__name = name

        return self


class Style:
    __styleNames: set = set()
    __style: dict = {
        'visualStyle': []
    }
    __style_xml: ET
    __DOCUMENT_VERSION: str = '3.0'

    def __init__(self):
        self.__style_xml = ET.Element('vizmap')
        self.__style_xml.set('id', 'VizMap-' +
                             str(datetime.datetime.now().date())
                             )
        self.__style_xml.set('documentVersion', self.__DOCUMENT_VERSION)

    def addVisualStyle(self, visualStyle: VisualStyle):
        vs = visualStyle.generate()
        if vs['name'] not in self.__styleNames:
            self.__styleNames.add(vs['name'])
        else:
            raise Exception(f'Visual style with {vs["name"]} already exists!')

        self.__style['visualStyle'].append(vs)

        return self

    def generate(self) -> dict:

        return self.__style

    def generate_xml(self):
        for vs in self.__style['visualStyle']:
            vs_xml = ET.SubElement(self.__style_xml, 'visualStyle')
            vs_xml.set('name', vs['name'])

            for conf_name in ['network', 'node', 'edge']:
                conf = ET.SubElement(vs_xml, conf_name)

                for var, data in vs[conf_name].items():
                    for i, var_data in enumerate(data):
                        conf_part = ET.SubElement(conf, var)
                        for name, value in var_data.items():
                            conf_part.set(name, str(value))

        return self.__style_xml


if __name__ == "__main__":
    vs_1 = VisualStyle(Network(), Node(), Edge()).changeName('v1')
    vs_2 = VisualStyle(Network(), Node(), Edge()).changeName('v2')
    vs_3 = VisualStyle(Network(), Node(), Edge()).changeName('v3')

    style = Style() \
        .addVisualStyle(vs_1) \
        .addVisualStyle(vs_2) \
        .addVisualStyle(vs_3)

    ET.dump(style.generate_xml())
