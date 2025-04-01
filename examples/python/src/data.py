import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from compas.data import Data
from compas.geometry import Frame, Line, Point, Vector
from google.protobuf import any_pb2, message

from compas_buff.data import line_pb2 as LineData
from compas_buff.data import message_pb2 as AnyData
from compas_buff.data import point_pb2 as PointData
from compas_buff.data import vector_pb2 as VectorData


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

    return point_data, AnyData.AnyDataType.POINT


def vector_to_pb(vector):
    vector_data = VectorData.VectorData()
    vector_data.guid = str(vector.guid)
    vector_data.name = vector.name
    vector_data.x = vector.x
    vector_data.y = vector.y
    vector_data.z = vector.z
    return vector_data, AnyData.AnyDataType.VECTOR


def line_to_pb(line):
    line_data = LineData.LineData()
    line_data.guid = str(line.guid)
    line_data.name = line.name
    line_data.start.CopyFrom(point_to_pb(line.start))
    line_data.end.CopyFrom(point_to_pb(line.end))
    return line_data, AnyData.AnyDataType.LINE


def frame_to_pb():
    frame_data = FrameData.FrameData()
    frame_data.guid = str(frame.guid)
    frame_data.name = frame.name
    frame_data.point.CopyFrom(point_to_pb(frame.point))
    frame_data.xaxis.CopyFrom(vector_to_pb(frame.xaxis))
    frame_data.yaxis.CopyFrom(vector_to_pb(frame.yaxis))
    return frame_data, AnyData.AnyDataType.FRAME


def element_to_pb(element):
    element_data = ElementData.ElementData()
    element_data.guid = str(element.guid)
    element_data.name = element.name
    element_data.frame.CopyFrom(frame_to_pb(element.frame))
    element_data.xsize = element.xsize
    element_data.ysize = element.ysize
    element_data.zsize = element.zsize
    return element_data, AnyData.AnyDataType.ELEMENT


SERIALIZERS = {
    Point: point_to_pb,
    Vector: vector_to_pb,
    Line: line_to_pb,
    Frame: frame_to_pb,
    Element: element_to_pb,
}

# no return enum type
def serialize_any(obj):
    """Serialize any object to a protobuf Any message"""

    if isinstance(obj, list):
        offset = serialize_list(obj)
        type_enum = AnyData.AnyData().ListData
    elif isinstance(obj, dict):
        offset = serialize_dict(obj)
        type_enum = AnyData.AnyData().DictData
    else:
        serializer = SERIALIZERS.get(type(obj))
        if not serializer:
            raise ValueError(f"Unsupported type: {type(obj)}")
        offset, type_enum = serializer(obj)
        print(f"offset: {offset}")
        print(f"type_enum: {type_enum}")
    return offset, type_enum


def serialize_any_wrapper(obj):
    """Wraps AnyData inside AnyDataWrapper."""
    any_data = any_pb2.Any()
    assert any_data.Is(obj.DESCRIPTOR)
    return any_data.MergeFrom(serialize_any(obj)[0])


def serialize_list(data_list):
    """Serialize a Python list containing mixed data types."""
    list_data = AnyData.ListData()
    for item in data_list:
        list_data.data.append(serialize_any_wrapper(item))
    return list_data


def serialize_dict(data_dict):
    """Serialize a Python dictionary containing mixed data types."""
    dict_data = AnyData.DictData()
    for key, value in data_dict.items():
        dict_data.data[key].CopyFrom(serialize_any_wrapper(value))
    return dict_data


def serialize_message(data):
    """Serialize a top-level protobuf message."""
    message = AnyData.MessageData()
    serialized_data = serialize_any(data)
    return message.SerializeToString(serialized_data)


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

    nested_list = [
        Point(1.0, 2.0, 3.0),
        Vector(4.0, 5.0, 6.0),
    ]

    point = Point(1.0, 2.0, 3.0)

    # Serialize and save
    binary_data = serialize_message(nested_data)
    # binary_data = serialize_message(point)

    # binary_data = serialize_message(nested_data)
    with open("nested_data.bin", "wb") as f:
        f.write(binary_data)

    # Deserialize
    with open("nested_data.bin", "rb") as f:
        binary_data = f.read()
        proto_data = AnyData.MessageData()
        proto_data.ParseFromString(binary_data)
        print(proto_data)


if __name__ == "__main__":
    main()
