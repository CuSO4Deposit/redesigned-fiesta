set shell := ["bash", "-c"]

# Generate the sanitized public data (does not build the site).
data:
	nix shell .#uv -c uv run python -m pipeline build

# Build the static site from the generated data.
site:
	nix run .#hugo -- --gc --minify

# The full public build: data first, then the site that consumes it.
build: data site

# Preview the site locally.
serve:
	nix run .#hugo -- server

# Run the pipeline tests.
test:
	nix shell .#uv -c uv run pytest

# Export the public Logseq pages into content/.
export:
	nix run .#schrodinger -- export --graph ~/Documents/Logseq --out . --assets-dir static/assets --clean
