class HeirachicalDict:
  def __init__(self, idict, get_parent):
    self.cont = idict
    self.get_parent = get_parent
    

  @classmethod
  def from_iter(cls, iiter, get_parent):
    obj = cls({}, get_parent=get_parent)
    for item in iiter:
      obj.add(item)
    return obj
    

  def __str__(self):
    return '\n'.join([
      '|   '*((l:=len(path))-2) + '+-- '*(l>1) +
      str(item) for path, item in self.unpack().items()
    ])
  

  def add(self, item)->tuple:
    if (path:=self.find(item)) is not None:
      return path
    if (parent:=self.get_parent(item)) is None:
      parent_path = ()
    elif (parent_path:=self.find(parent)) is None:
      parent_path=self.add(parent)
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
      if (path:=HeirachicalDict._find_in_dict(cont, item)) is not None:
        return (key,)+path
    return None
    

  @staticmethod
  def _follow_in_dict(idict, path):
    if path:
      step, *new_path = path
      return HeirachicalDict._follow_in_dict(idict[step], new_path)
    else:
      return idict



if __name__ == '__main__':
  def get_parent_class(obj):
    return None if (a:=obj.__bases__) == () else a[0]

  def is_class(obj):
    return type(obj) == type

  builtin_classes = filter(is_class, __builtins__.__dict__.values())

  e = HeirachicalDict.from_iter(builtin_classes, get_parent_class)
  print(e)
