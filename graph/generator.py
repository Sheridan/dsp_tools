#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import os.path

unknown_icon = "https://dsp-wiki.com/images/1/10/Icon_Unknown.png"

class CGenerator:
  def __init__(self):
    with open('data.json') as json_file:
      self.data = json.load(json_file)

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

  def get_icon_filename(self, item_key):
    if item_key in self.data["items"]:
      item = self.data["items"][item_key]
      return self.download_icon(item["icon"], 'icons/{}.png'.format(item_key))
    return self.download_icon(unknown_icon, 'icons/unknown.png')

  def get_color(self, name):
    # print(name)
    return self.data["colors"][name]

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

  def generate_graphviz_nodes(self, gv_file):
    for item_key in self.data["items"]:
      print("Generating node {}".format(item_key))
      item = self.data["items"][item_key]
      gv_file.write("""
  {0} [label=<
             <table border="0" cellborder="0" cellspacing="0">
              <tr>
                <td colspan="2">{1}</td>
              </tr>
              <tr>
                <td><img src='{2}' /></td>
                <td>Usages: {5}</td>
              </tr>
              {4}
             </table>
             >, fillcolor="#{3}"];
          """.format(
          item_key,
          item["name"],
          self.get_icon_filename(item_key),
          self.get_color(item["type"]),
          self.get_flags_icons(item),
          self.count_usage(item_key)))

  def generate_graphviz_edges(self, gv_file):
    for item_key in self.data["items"]:
      print("Generating edge {}".format(item_key))
      item = self.data["items"][item_key]
      for recipe in item["recipes"]:
        print("Recipe {}".format(recipe["assembler"]))
        if "recipe" in recipe:
          for recipe_item in recipe["recipe"]:
            gv_file.write("""
  {1} -> {0} [color="#{2}"];
          """.format(
                item_key,
                recipe_item,
                self.get_color(recipe["assembler"])))


  def generate_graphviz(self):
    with open('graph.gv', "w") as gv_file:
      gv_file.write("digraph g{\n")
      gv_file.write('graph [overlap=false, splines=ortho, ratio=0.5625, bgcolor="#{0}", fontcolor="#{1}", fontname=Roboto, fontsize=10];\n'.format(
            self.get_color("background"),
            self.get_color("font")))
      gv_file.write('node [shape=box, style=filled, fontcolor="#{0}", color="#{0}"];\n'.format(
            self.get_color("font")))
      gv_file.write('edge [fontcolor="#{0}", color="#{0}"];\n'.format(
            self.get_color("font")))
      self.generate_graphviz_nodes(gv_file)
      self.generate_graphviz_edges(gv_file)
      gv_file.write("}\n")

  def main(self):
    self.generate_graphviz()
    # print(json.dumps(self.data, indent=2))

g = CGenerator()
g.main()
