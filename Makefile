all: build

build: .PHONY
	mdbook build

serve: .PHONY
	mdbook serve --open

sync: .PHONY
	./farm-sync.sh

.PHONY:
