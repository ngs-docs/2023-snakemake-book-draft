all: build

build: .PHONY
	mdbook build -d book

serve: .PHONY
	mdbook serve --open

sync: build .PHONY
	./farm-sync.sh

gh-pages: .PHONY
	./deploy.sh

run.sh: .PHONY
	./find-snakefiles.py code -l -o run.sh

test: run.sh
	bash run.sh

.PHONY:
