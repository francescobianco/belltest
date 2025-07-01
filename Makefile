

start:
	@python3 belltest.py

push:
	@git add .
	@git commit -am "New release!" || true
	@git push