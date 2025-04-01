
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from compas.data import Data
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Line

from compas_buff.data import point_pb2 as PointData
from compas_buff.data import line_pb2 as LineData
from compas_buff.data import vector_pb2 as VectorData
from compas_buff.data import message_pb2 as AnyData

# from google.protobuf import any_pb2


class Element(Data):
    """Mock class to simulate a data structure"""

    def __init__(self, frame, xsize, ysize, zsize, name=None):
        super(Element, self).__init__(name)
        self.name = name
        self.frame = frame
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize

def point_to_pb(point):
    point_data = PointData.PointData()
    point_data.guid = str(point.guid)
    point_data.name = point.name
    point_data.x = point.x
    point_data.y = point.y
    point_data.z = point.z
    return point_data


def vector_to_pb(vector):
    vector_data = VectorData.VectorData()
    vector_data.guid = str(vector.guid)
    vector_data.name = vector.name
    vector_data.x = vector.x
    vector_data.y = vector.y
    vector_data.z = vector.z
    return vector_data


def line_to_pb(line):
    line_data = LineData.LineData()
    line_data.guid = str(line.guid)
    line_data.name = line.name
    line_data.start.CopyFrom(point_to_pb(line.start))
    line_data.end.CopyFrom(point_to_pb(line.end))
    return line_data


def frame_to_pb():
    frame_data = FrameData.FrameData()
    frame_data.guid = str(frame.guid)
    frame_data.name = frame.name
    frame_data.point.CopyFrom(point_to_pb(frame.point))
    frame_data.xaxis.CopyFrom(vector_to_pb(frame.xaxis))
    frame_data.yaxis.CopyFrom(vector_to_pb(frame.yaxis))
    return frame_data


def element_to_pb(element):
    element_data = ElementData.ElementData()
    element_data.guid = str(element.guid)
    element_data.name = element.name
    element_data.frame.CopyFrom(frame_to_pb(element.frame))
    element_data.xsize = element.xsize
    element_data.ysize = element.ysize
    element_data.zsize = element.zsize
    return element_data


SERIALIZERS = {
    Point: point_to_pb,
    Vector: vector_to_pb,
    Line: line_to_pb,
    Frame: frame_to_pb,
    Element: element_to_pb,
}

# no return enum type
def serialize_any(obj):
    """Serialize any object to a protobuf message"""
    message = AnyData.MessageData()
    # any_data = AnyData.AnyData()

    if isinstance(obj, list):
        message.data.list.CopyFrom(serialize_list(obj))
    elif isinstance(obj, dict):
        message.data.dict.CopyFrom(serialize_dict(obj))
        print(serialize_dict(obj))
    else:
        serializer = SERIALIZERS.get(type(obj))
        if not serializer:
            raise ValueError(f"Unsupported type: {type(obj)}")
        message.data.CopyFrom(serializer(obj))
    return any_data


def serialize_list(data_list):
    """Serialize a Python list containing mixed data types."""
    list_data = AnyData.ListData()
    for item in data_list:
        list_data.data.append(serialize_any(item))
        print(list_data)
    return list_data

def serialize_dict(data_dict):
    """Serialize a Python dictionary containing mixed data types."""
    dict_data = AnyData.DictData()
    for key, value in data_dict.items():
        dict_data.data[key].CopyFrom(serialize_any(value))
    return dict_data

def serialize_message(data):
    """Serialize a top-level protobuf message."""
    message = AnyData.MessageData()
    message.data.CopyFrom(serialize_any(data))
    return message.SerializeToString()

def main():
    # Example nested data structure
    frame = Frame.worldXY()
    element = Element(frame, 1.0, 2.0, 3.0, name="Element")
    nested_data = {
        "point": Point(1.0, 2.0, 3.0),
        "list": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0)]],  # Nested list
        "frame": frame,
        "element": element,
    }

    # Serialize and save
    binary_data = serialize_message(nested_data)

    # binary_data = serialize_message(nested_data)
    with open("nested_data.bin", "wb") as f:
        f.write(binary_data)

    # Deserialize and load
    with open("nested_data.bin", "rb") as f:
        binary_data = f.read()
        proto_data = AnyData.MessageData()
        proto_data.ParseFromString(binary_data)
        print(proto_data)

if __name__ == "__main__":
    main()
