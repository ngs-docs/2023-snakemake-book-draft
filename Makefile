all: build

build: .PHONY
	mdbook build

serve: .PHONY
	mdbook serve --open

sync: build .PHONY
	./farm-sync.sh

.PHONY:
