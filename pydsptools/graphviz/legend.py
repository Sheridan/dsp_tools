import sys
from pydsptools.options import options
from pydsptools.graphviz.entity import Entity

class Legend(Entity):
  def __init__(self, name):
    super().__init__("background")
    self.__name = name
    print("Generating legend {0}".format(self.__name))
    self.__cache = {}
    self.__legend = open('result/graphviz/legend_{0}.gv'.format(self.__name), "w")
    self.__legend.write('digraph g {\n')
    self.__generate_options()

  def __del__(self):
    self.__legend.write('}\n')
    self.__legend.close()

  def __generate_options(self):
    for group in options['graphviz']['default']:
      self.__legend.write('  {0} ['.format(group))
      for option_key in options['graphviz']['default'][group]:
        option_value = options['graphviz']['default'][group][option_key]
        if 'legend' in options['graphviz'] and group in options['graphviz']['legend'] and option_key in options['graphviz']['legend'][group]:
          option_value = options['graphviz']['legend'][group][option_key]
        if 'color' in option_key:
          option_value = options.color(option_value)
        self.__legend.write(' {0}="{1}" '.format(option_key, option_value))
      self.__legend.write('];\n')

  def __append_group_node(self, name, description):
    if name not in self.__cache:
      self.__cache[name] = []
      self.__legend.write(self.load_template('legend/node_group.gv').format(
        group_name = name,
        title = description,
        color = options.color('background')
      ) + '\n')

  def append_node_color(self, color, description):
    self.__append_group_node('colored_nodes', 'Nodes colors')
    if color not in self.__cache['colored_nodes']:
      self.__cache['colored_nodes'].append(color)
      self.__legend.write(self.load_template('legend/node_color.gv').format(
        node_name = self.normalize_name(description),
        group_name = 'colored_nodes',
        title = description,
        color = options.color(color),
        group_edge_color = options.color('foreground')
      ) + '\n')

  def append_edge_color(self, color, description):
    self.__append_group_node('colored_edges', 'Arrows colors')
    if color not in self.__cache['colored_edges']:
      self.__cache['colored_edges'].append(color)
      self.__legend.write(self.load_template('legend/edge_color.gv').format(
        node_name = self.normalize_name(description),
        group_name = 'colored_edges',
        title = description,
        color = options.color(color),
        node_color = options.color('background'),
        group_edge_color = options.color('foreground')
      ) + '\n')

  def append_node_flag(self, icon, description):
    self.__append_group_node('flag_nodes', 'Flags')
    if icon not in self.__cache['flag_nodes']:
      self.__cache['flag_nodes'].append(icon)
      self.__legend.write(self.load_template('legend/flag.gv').format(
        node_name = self.normalize_name(description),
        group_name = 'flag_nodes',
        flag_icon = icon,
        flag_description = description,
        color = options.color('background'),
        group_edge_color = options.color('foreground')
      ) + '\n')
