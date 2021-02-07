#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import os.path
import sys

unknown_icon = "https://dsp-wiki.com/images/1/10/Icon_Unknown.png"
icon_size = 64

class CGenerator:
  def __init__(self):
    with open('data.json') as json_file:
      self.data = json.load(json_file)
    self.used_assemblers_keys = []
    self.used_types_keys = []
    self.graphs_list = []

  def download_icon(self, icon_url, icon_filename):
    if not os.path.isfile(icon_filename):
      with open(icon_filename, 'wb') as icon_file:
        response = requests.get(icon_url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            icon_file.write(block)
    return icon_filename

  def get_icon_filename(self, group, key):
    if key in self.data[group]:
      item = self.data[group][key]
      return self.download_icon(item["icon"], 'icons/{0}_{1}.png'.format(group, key))
    return self.download_icon(unknown_icon, 'icons/unknown.png')

  def get_color(self, group, name):
    # print(name)
    return self.data["colors"][group][name]

  def get_flags_icons(self, item):
    if "flags" in item:
      flags=""
      for flag in item["flags"]:
        flags += " {0} ".format(self.data["icons"][flag])
      return '<tr><td colspan="2">{0}</td></tr>'.format(flags)
    return ""

  def count_usage(self, target_item_key):
    count = 0
    for item_key in self.data["items"]:
      item = self.data["items"][item_key]
      for recipe in item["recipes"]:
        if "recipe" in recipe:
          for recipe_item in recipe["recipe"]:
            if target_item_key == recipe_item:
              count+=1
    return count

  def generate_items_nodes(self, gv_file):
    for item_key in self.data["items"]:
      print("Generating node {}".format(item_key))
      item = self.data["items"][item_key]
      self.used_types_keys.append(item["type"])
      gv_file.write("""  item_{0} [label=<
             <table border="0" cellborder="0" cellspacing="0">
              <tr>
                <td colspan="2">{1}</td>
              </tr>
              <tr>
                <td fixedsize="true" width="{6}" height="{6}"><img src='{2}' /></td>
                <td>Usages: {5}</td>
              </tr>
              {4}
             </table>
             >, fillcolor="#{3}"];
""".format(
          item_key,
          item["name"],
          self.get_icon_filename("items", item_key),
          self.get_color("nodes", item["type"]),
          self.get_flags_icons(item),
          self.count_usage(item_key),
          icon_size))

  def generate_items_edges(self, gv_file):
    for item_key in self.data["items"]:
      print("Generating edge {}".format(item_key))
      item = self.data["items"][item_key]
      for recipe in item["recipes"]:
        print("Recipe {}".format(recipe["assembler"]))
        if "recipe" in recipe:
          for recipe_item in recipe["recipe"]:
            self.used_assemblers_keys.append(recipe["assembler"])
            gv_file.write('  item_{1} -> item_{0} [color="#{2}"];\n'.format(
                item_key,
                recipe_item,
                self.get_color("edges", recipe["assembler"])))

  def generate_options(self, gv_file, splines, ratio, minlen):
      gv_file.write('  graph [overlap=false, splines={2}, ratio={3}, bgcolor="#{0}", fontcolor="#{1}", fillcolor="#{0}", fontname=Roboto, fontsize=10];\n'.format(
        self.get_color("main", "background"),
        self.get_color("main", "font"),
        splines,
        ratio))
      gv_file.write('  node [shape=box, style="rounded,filled", fontcolor="#{0}", color="#{0}"];\n'.format(
            self.get_color("main", "font")))
      gv_file.write('  edge [fontcolor="#{0}", color="#{0}", penwidth=3, minlen={1}];\n'.format(
            self.get_color("main", "font"),
            minlen))

  def generate_tech_nodes(self, gv_file):
    self.used_types_keys.append("tech")
    for tech_key in self.data["technologies"]:
      print("Generating node {}".format(tech_key))
      tech = self.data["technologies"][tech_key]
      gv_file.write("""  tech_{0} [label=<
             <table border="0" cellborder="0" cellspacing="0">
              <tr>
                <td>{1}</td>
              </tr>
              <tr>
                <td fixedsize="true" width="{4}" height="{4}"><img src='{2}' /></td>
              </tr>
             </table>
             >, fillcolor="#{3}"];
""".format(
          tech_key,
          tech["name"],
          self.get_icon_filename("technologies", tech_key),
          self.get_color("nodes", "tech"),
          icon_size))

  def generate_tech_edges(self, gv_file):
    for tech_key in self.data["technologies"]:
      print("Generating edge {}".format(tech_key))
      tech = self.data["technologies"][tech_key]
      for parent_tech_key in tech["requirements"]:
        gv_file.write('  tech_{0} -> tech_{1} [color="#{2}"];\n'.format(
            parent_tech_key,
            tech_key,
            self.get_color("edges", "tech")))
      if "items" in self.graphs_list:
        for item_key in tech["unlocks"]:
          gv_file.write('  tech_{0} -> item_{1} [color="#{2}"];\n'.format(
              tech_key,
              item_key,
              self.get_color("edges", "unlocks")))
        for item_key in tech["resources"]:
          gv_file.write('  item_{1} -> tech_{0} [color="#{2}"];\n'.format(
              tech_key,
              item_key,
              self.get_color("edges", "resources")))

  def generate_graph(self, graphs_list):
    self.graphs_list = graphs_list
    self.used_types_keys = []
    self.used_assemblers_keys = []
    with open('graph_{0}.gv'.format('_'.join(self.graphs_list)), "w") as gv_file:
      gv_file.write("digraph g {\n")
      self.generate_options(gv_file, "ortho", 9/16, 4)
      if "items" in self.graphs_list:
        self.generate_items_nodes(gv_file)
        self.generate_items_edges(gv_file)
      if "tech" in self.graphs_list:
        self.generate_tech_nodes(gv_file)
        self.generate_tech_edges(gv_file)
      gv_file.write('subgraph cluster_0 {{ label="Legend"; legend [image="legend_{1}.{0}", label="", shape="none"]; }}\n'.format(sys.argv[1], '_'.join(self.graphs_list)))
      gv_file.write("}\n")
    self.generate_legend()

  def generate_legend(self):
    with open('legend_{0}.gv'.format('_'.join(self.graphs_list)), "w") as gv_file:
      gv_file.write('digraph g {\n')
      self.generate_options(gv_file, "ortho", "auto", 1)
      if "items" in self.graphs_list:
        gv_file.write('types [label="Types", fillcolor="#{0}"]; assemblers [label="Assemblers", fillcolor="#{0}"]; flags [label="Flags", fillcolor="#{0}"]; '.format(
              self.get_color("main", "background")
            ))
        for icon_key in self.data["legend"]["icons"]:
          gv_file.write('  {0} [label="{1} {2}", fillcolor="#{3}"]; flags ->{0} [penwidth=1];\n'.format(
                icon_key,
                self.data["icons"][icon_key],
                self.data["legend"]["icons"][icon_key],
                self.get_color("main", "background")
              ))
      used_nodes_keys = set(self.used_types_keys)
      print(used_nodes_keys)
      for node_color_key in self.data["legend"]["colors"]["nodes"]:
        print(node_color_key)
        if node_color_key in used_nodes_keys:
          gv_file.write('  {0} [label="{1}", fillcolor="#{2}"];\n'.format(
                node_color_key,
                self.data["legend"]["colors"]["nodes"][node_color_key],
                self.get_color("nodes", node_color_key)
              ))
          if "items" in self.graphs_list:
            gv_file.write('  types -> {0} [penwidth=1];\n'.format(
                  node_color_key,
                  self.data["legend"]["colors"]["nodes"][node_color_key],
                  self.get_color("nodes", node_color_key)
                ))
      used_edges_keys = set(self.used_assemblers_keys)
      print(used_edges_keys)
      for edge_color_key in self.data["legend"]["colors"]["edges"]:
        if edge_color_key in used_edges_keys:
          gv_file.write('  {0}_a [label="{1}", fillcolor="#{2}"]; {0}_b [shape=point]; assemblers -> {0}_a [penwidth=1]; {0}_a -> {0}_b [color="#{3}"]; \n'.format(
                edge_color_key,
                self.data["legend"]["colors"]["edges"][edge_color_key],
                self.get_color("main", "background"),
                self.get_color("edges", edge_color_key)
              ))
      gv_file.write("  }\n")

  def main(self):
    self.generate_graph(["items"])
    self.generate_graph(["tech"])
    self.generate_graph(["tech", "items"])

g = CGenerator()
g.main()
