from pydsptools.graphviz.entity import Entity

class Edge(Entity):
  def __init__(self, name_from, name_to, color, weight):
    super().__init__(color)
    self.__weight = weight
    self.__name_from = self.normalize_name(name_from)
    self.__name_to = self.normalize_name(name_to)

  def name_from(self):
    return self.__name_from

  def name_to(self):
    return self.__name_to

  def weight(self):
    return self.__weight

  def compile(self):
    return self.load_template('main/edge.gv').format(
      node_from = self.name_from(),
      node_to = self.name_to(),
      color = self.color(),
      weight = self.weight()
    ) + '\n'
