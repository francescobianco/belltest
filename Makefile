

start:
	@python3 belltest.py

demo:
	@python3 showcase/demo_hidden_vs_none.py

minimal:
	@python3 showcase/minimal_s_gt_2.py

auto_chsh:
	@python3 showcase/auto_chsh.py

push:
	@git add .
	@git commit -am "New release!" || true
	@git push