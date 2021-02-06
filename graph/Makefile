
compile:
	./generator.py
	dot   -T${img_type} -o production_dot.${img_type} graph.gv
	neato -T${img_type} -Gsep=0.1 -o production_neato.${img_type} graph.gv
	# twopi -T${img_type} -o production_twopi.${img_type} graph.gv
	# fdp   -T${img_type} -o production_fdp.${img_type}   graph.gv

compile_png: img_type=png
compile_png: compile

compile_svg: img_type=svg
compile_svg: compile

clear:
	rm -vf icons/* *gv *png *svg
