

start:
	@python3 belltest.py

demo:
	@python3 showcase/demo_hidden_vs_none.py

auto_chsh:
	@python3 showcase/auto_chsh.py

push:
	@git add .
	@git commit -am "New release!" || true
	@git push