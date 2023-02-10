all: build

build: .PHONY
	mdbook build -d book

serve: .PHONY
	mdbook serve --open

sync: build .PHONY
	./farm-sync.sh

gh-pages: .PHONY
	./deploy.sh

.PHONY:
