#!/usr/bin/env python3

from pydsptools.generator import Generator

if __name__ == '__main__':
  for graph in [["items"], ["tech"], ["tech", "items"]]:
    Generator(graph).main()
