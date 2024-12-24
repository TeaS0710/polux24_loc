import msgpack

class DataWrapper:
  def __init__(self):
    pass
  
  def encode(self):
    msgpack.packb(vars(self), use_bin_type=True)

  @classmethod
  def decode(cls, data):
    return cls(**msgpack.unpackb(data, raw=False))
