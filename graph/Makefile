
define generate_graph
	dot   -T$(1)           -o result/legend_$(2).$(1)       result/legend_$(2).gv
	dot   -T$(1)           -o result/graph_$(2)_dot.$(1)    result/graph_$(2).gv
	# neato -T$(1) -Gsep=0.1 -o result/graph_$(2)_neato.$(1)  result/graph_$(2).gv
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

clean_result:
	rm -vf result/*

clean_icons:
	rm -vf icons/*

clean: clean_result clean_icons
