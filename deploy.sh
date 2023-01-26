#! /bin/bash
tmpdir=$(mktemp -d /tmp/bookXXX)
mdbook build -d ${tmpdir}
echo "build directory is: ${tmpdir}"

cd ${tmpdir}
touch .nojekyll
git init
echo '*~' > .gitignore
git add .
git branch -M main
git commit -m "latest"

git push -f https://github.com/ngs-docs/2023-snakemake-book-draft main:gh-pages

