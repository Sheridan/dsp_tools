import sys
from pydsptools.options import options
from pydsptools.graphviz.entity import Entity

class Graph(Entity):
  def __init__(self, name):
    super().__init__("background")
    self.__name = name
    print("Generating graph {0}".format(self.__name))
    self.__graph = open('result/graphviz/graph_{0}.gv'.format(self.__name), "w")
    self.__graph.write('digraph g {\n')
    self.__generate_options()
    self.__nodes = []
    self.__edges = []

  def __del__(self):
    self.__graph.write('  subgraph cluster_legend {{ rank="max"; label="Legend"; legend [image="result/graphs/legend_{1}.{0}" label="" shape="none"]; }}\n'.format(sys.argv[1], self.__name))
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
    self.__nodes.append(node)

  def append_edge(self, edge):
    self.__edges.append(edge)

  def compile(self):
    print("Compiling graph...")
    sorted_types = {}
    for key, value in dict(sorted(options["rank_order"].items(), key=lambda item: item[1])).items():
      sorted_types.setdefault(value, list()).append(key)
    subgraph_index = 0
    for i in sorted_types.keys():
      nodes = []
      for node in self.__nodes:
        if node.type() in sorted_types[i]:
          nodes.append(self.compact_string(node.compile()))
      if len(nodes) > 0:
        print("Compiled type {0}: {1} -> {2}".format(i, sorted_types[i], len(nodes)))
        if node.type() != "tech":
          self.__graph.write(self.load_template_raw('main/subgraph.gv').format(
            subgraph_items = ''.join(nodes),
            subgraph_index = subgraph_index
          ))
        else:
          self.__graph.write(''.join(nodes))
        subgraph_index += 1
    for edge in self.__edges:
      self.__graph.write(self.compact_string(edge.compile()))
