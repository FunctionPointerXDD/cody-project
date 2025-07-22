.PHONY: all data map path clean

all: data map path

data:
	@echo "1) Parsing data..."
	python caffee_map.py

map: data
	@echo "2) Drawing map..."
	python map_draw.py

path: map
	@echo "3) Computing & plotting shortest path..."
	python map_direct_save.py

clean:
	rm -f results/map.png results/home_to_cafe.csv results/map_final.png
	@echo "Artifacts removed."
