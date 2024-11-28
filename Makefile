PYTHON = python3
PIP = pip3
ARG = datasets/data_12x12_10vic
# dentro da pasta datasets em um campo vc deve mudar o nome de algumas pastas
all:
	$(PYTHON) main.py $(ARG)