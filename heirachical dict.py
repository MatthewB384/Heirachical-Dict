class OrphanError(ValueError):
  'Raised when you try to find the parent of an object that doesn\'t have one'


class HeirachicalDict:
  def __init__(self, idict, get_parent):
    self.cont = idict
    self.get_parent = get_parent
    

  @classmethod
  def from_iter(cls, iiter, get_parent):
    obj = cls({}, get_parent)
    for item in iiter:
      obj.add(item)
    return obj
    

  def __str__(self):
    return '\n'.join([
      '|   '*((l:=len(path))-2) + '+-- '*(l>1) +
      str(item) for path, item in self.unpack().items()
    ])
  

  def add(self, item)->tuple:
    try:
      return self.find(item)
    except KeyError:
      try:
        parent_path = self.add(self.get_parent(item))
      except OrphanError: #F
        parent_path = ()
      finally:
        self.follow(parent_path)[item] = {}
        return parent_path + (item,)

      
  def find(self, item):
    return self._find_in_dict(self.cont, item)
  

  def follow(self, path):
    return self._follow_in_dict(self.cont, path)


  def unpack(self):
    return self._unpack_dict(self.cont)


  @staticmethod
  def _unpack_dict(idict):
    out = {}
    for item, cont in idict.items():
      out[item,] = item
      for path, icont in HeirachicalDict._unpack_dict(cont).items():
        out[(item,)+path] = icont
    return out

  
  @staticmethod
  def _find_in_dict(idict, item)->tuple:
    if item in idict:
      return item,
    for key, cont in idict.items():
      try:
        return (key,) + HeirachicalDict._find_in_dict(cont, item)
      except KeyError:
        continue
    raise KeyError
    

  @staticmethod
  def _follow_in_dict(idict, path):
    if path:
      step, *new_path = path
      return HeirachicalDict._follow_in_dict(idict[step], new_path)
    else:
      return idict



if __name__ == '__main__':
  def get_parent_class(obj):
    if (a:=obj.__bases__) == ():
      raise OrphanError
    else:
      return a[0]


  builtin_classes = filter(
    lambda obj: isinstance(obj, type),
    __builtins__.__dict__.values()
  )

  e = HeirachicalDict.from_iter(builtin_classes, get_parent_class)
  print(e)
