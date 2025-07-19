.PHONY: all data map path clean

all: data map path

data:
	@echo "1) Parsing data..."
	python coffee_map.py

map: data
	@echo "2) Drawing map..."
	python map_draw.py

path: map
	@echo "3) Computing & plotting shortest path..."
	python map_direct_save.py

clean:
	rm -f dataFile/mas_map.csv img/map.png dataFile/home_to_cafe.csv img/map_final.png
	@echo "Artifacts removed."
