
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from compas.data import Data
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Line

import compas_buff.data.point_pb2 as point_pb2
# from compas_buff.data import vector_pb2 as VectorData
# from compas_buff.data import line_pb2 as LineData

print(sys.path)

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
  point_data = point_pb2.PointData()
  point_data.guid = point.guid.__str__()
  point_data.name = point.name
  point_data.x = point.x
  point_data.y = point.y
  point_data.z = point.z
  return point_data

def vector_to_pb():
  pass

def line_to_pb():
  pass

def frame_to_pb():
  pass

def element_to_pb():
  pass

SERIALIZERS = {
  Point: point_to_pb
  # Vector: vector_to_pb,
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
  print(point_data)

  # Serialize the message
  binary_data = serialize_message(point_data)
  #
  with open("point.bin", "wb") as f:
    f.write(binary_data)

if __name__ == "__main__":
  main()
















