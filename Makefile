

start:
	@python3 belltest.py

demo:
	@python3 showcase/s_05/example.py
	@python3 showcase/s_10/example.py
	@python3 showcase/s_15/example.py
	@python3 showcase/s_20/example.py
	@python3 showcase/s_25/example.py
	@python3 showcase/s_30/example.py
	@python3 showcase/s_35/example.py
	@python3 showcase/s_40/example.py

s_05:
	@python3 showcase/s_05/example.py

s_10:
	@python3 showcase/s_10/example.py

s_15:
	@python3 showcase/s_15/example.py

s_20:
	@python3 showcase/s_20/example.py

s_25:
	@python3 showcase/s_25/example.py

s_30:
	@python3 showcase/s_30/example.py

s_35:
	@python3 showcase/s_35/example.py

s_40:
	@python3 showcase/s_40/example.py

push:
	@git add .
	@git commit -am "New release!" || true
	@git push