
define generate_graph
	dot   -T$(1)           -o legend_$(2).$(1)       legend_$(2).gv
	dot   -T$(1)           -o graph_$(2)_dot.$(1)    graph_$(2).gv
	neato -T$(1) -Gsep=0.1 -o graph_$(2)_neato.$(1)  graph_$(2).gv
endef

compile:
	./generator.py ${img_type}
	$(call generate_graph,${img_type},items)
	$(call generate_graph,${img_type},tech)
	$(call generate_graph,${img_type},tech_items)

compile_png: img_type=png
compile_png: compile

compile_svg: img_type=svg
compile_svg: compile

clear:
	rm -vf icons/* *gv *png *svg
