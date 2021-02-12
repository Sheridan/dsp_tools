
define generate_graph
	dot   -T$(1) -o result/graphs/legend_$(2).$(1)   result/graphviz/legend_$(2).gv
	dot   -T$(1) -o result/graphs/graph_$(2).$(1)    result/graphviz/graph_$(2).gv
  convert result/graphs/graph_$(2).$(1) -resize 1920x1080 result/graphs/resized_1920x1080_graph_$(2).$(1)
endef

compile:
	./make_graphs.py ${img_type}

draw:
	$(call generate_graph,${img_type},items)
	$(call generate_graph,${img_type},tech)
	$(call generate_graph,${img_type},tech_items)

all: img_type=png
all: compile draw

compile_png: img_type=png
compile_png: compile

compile_svg: img_type=svg
compile_svg: compile

clean_result:
	rm -vf result/*

clean_icons:
	rm -vf icons/*

clean: clean_result clean_icons
