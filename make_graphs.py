#!/usr/bin/env python3

from pydsptools.graphviz.graphviz import Graphviz

if __name__ == '__main__':
  for graph in [["items"], ["tech"], ["tech", "items"]]:
    Graphviz(graph).main()
