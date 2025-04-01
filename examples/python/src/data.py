
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
    return point_data, AnyData.AnyData().point


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
    pass


def element_to_pb():
    pass


SERIALIZERS = {
    Point: point_to_pb,
    Vector: vector_to_pb,
    # Line: line_to_pb,
    # Frame: frame_to_pb,
}


def serialize_any(builder, obj):
    serizlizer = SERIALIZERS.get(type(obj))
    if not serizlizer:
        raise ValueError(f"Unsupported type: {type(obj)}")


def serialize_message(func):
    return func.SerializeToString()


def main():
    point = Point(1.0, 2.0, 3.0)
    point_data = point_to_pb(point)
    print(f"Point data: {point_data}")

    # line = Line(Point(1.0, 1.0, 2.0), Point(1, 1, 1))
    # line_data = line_to_pb(line)
    #
    # print(f"Line data: {line_data}")

    # Serialize the message
    # binary_data = serialize_message(point_data)
    #
    # with open("point.bin", "wb") as f:
    #     f.write(binary_data)


if __name__ == "__main__":
    main()
