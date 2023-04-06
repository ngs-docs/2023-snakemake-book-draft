# Installing software to build & test this book

## Create conda environment with base software

```
mamba create -n mdbook -y rust snakemake-minimal pandas sourmash
```

and activate:
```
mamba activate mdbook
```

## Clone the repository

```
cd ~/
git clone https://github.com/ngs-docs/2023-snakemake-book-draft
cd 2023-snakemake-book-draft
```

## Install mdbook & plugins:

We use [mdbook](https://github.com/rust-lang/mdBook) as well as
[mdbook-admonish](https://github.com/tommilligan/mdbook-admonish) and
[mdbook-cmdrun](https://crates.io/crates/mdbook-cmdrun).

```
cargo install mdbook mdbook-admonish mdbook-cmdrun
```

## Build book

```
make
```

## Run snakemake tests

```
make test
```
