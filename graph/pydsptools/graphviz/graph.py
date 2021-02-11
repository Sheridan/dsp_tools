import sys
from pydsptools.options import options
from pydsptools.graphviz.entity import Entity

class Graph(Entity):
  def __init__(self, name):
    super().__init__("background")
    self.__name = name
    print("Generating graph {0}".format(self.__name))
    self.__graph = open('result/graph_{0}.gv'.format(self.__name), "w")
    self.__graph.write('digraph g {\n')
    self.__generate_options()
    self.__graph.write('  subgraph cluster_0 {{ label="Legend"; legend [image="result/legend_{1}.{0}" label="" shape="none"]; }}\n'.format(sys.argv[1], self.__name))

  def __del__(self):
    self.__graph.write('}\n')
    self.__graph.close()

  def __generate_options(self):
    for group in options['graphviz']['default']:
      self.__graph.write('  {0} ['.format(group))
      for option_key in options['graphviz']['default'][group]:
        option_value = options['graphviz']['default'][group][option_key]
        if self.__name in options['graphviz'] and group in options['graphviz'][self.__name] and option_key in options['graphviz'][self.__name][group]:
          option_value = options['graphviz'][self.__name][group][option_key]
        if 'color' in option_key:
          option_value = options.color(option_value)
        self.__graph.write(' {0}="{1}" '.format(option_key, option_value))
      self.__graph.write('];\n')

  def append_node(self, node):
    self.__graph.write(node.compile())

  def append_edge(self, edge):
    self.__graph.write(edge.compile())
