

start:
	@python3 belltest.py

demo:
	@python3 showcase/s_1/example.py
	@python3 showcase/s_2/example.py
	@python3 showcase/s_3/example.py
	@python3 showcase/s_4/example.py

s_1:
	@python3 showcase/s_1/example.py

s_2:
	@python3 showcase/s_2/example.py

s_3:
	@python3 showcase/s_3/example.py

s_4:
	@python3 showcase/s_4/example.py

push:
	@git add .
	@git commit -am "New release!" || true
	@git push