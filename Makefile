
define generate_graph
	neato   -T$(1) -o result/graphs/legend_$(2).$(1)   result/graphviz/legend_$(2).gv
	$(3)   -T$(1) -o result/graphs/graph_$(2).$(1)    result/graphviz/graph_$(2).gv
endef

define resize_graph
	convert result/graphs/graph_$(2).$(1) -resize 1920x1080 result/graphs/resized_1920x1080_graph_$(2).$(1)
endef

compile:
	./make_graphs.py ${img_type}

draw_items:
	$(call generate_graph,${img_type},items,dot)

draw_tech:
	$(call generate_graph,${img_type},tech,dot)

draw_items_tech:
	$(call generate_graph,${img_type},tech_items,neato)

resize_items:
	$(call resize_graph,${img_type},items)

resize_tech:
	$(call resize_graph,${img_type},tech)

resize_items_tech:
	$(call resize_graph,${img_type},tech_items)

png: img_type=png
png: compile draw_items draw_tech draw_items_tech resize_items resize_tech resize_items_tech

svg: img_type=svg
svg: compile draw_items draw_tech draw_items_tech

clean_result:
	rm -vf result/graphs/*.png
	rm -vf result/graphs/*.svg
	rm -vf result/graphviz/*.gv

clean_icons:
	rm -vf result/icons/generated/*.png

claean_downloaded_icons:
	rm -vf result/icons/original/*.png

clean: clean_result clean_icons

rebuild: clean build

dev: img_type=png
dev: compile draw_items
