set shell := ["bash", "-c"]

# List available recipes.
[private]
default:
	@just --list

# Generate the sanitized public data (does not build the site).
data:
	nix shell .#uv -c uv run python -m pipeline build

# Build the static site from the generated data.
site:
	nix run .#hugo -- --gc --minify

# The full public build: data first, then the site that consumes it.
build: data site

# End to end: export, translate, build, commit, then push.
all: export translate build commit push

# Preview the site locally.
serve:
	nix run .#hugo -- server

# Run the pipeline tests.
test:
	nix shell .#uv -c uv run pytest

# Export the public Logseq pages into content/.
export:
	nix run .#schrodinger -- export --graph ~/Documents/Logseq --out . --assets-dir static/assets --clean

# Translate changed pages to English (needs LLM_API_KEY).
translate:
	nix shell .#uv -c uv run python -m pipeline translate

# Adopt existing .en.md files without calling the model.
translate-seed:
	nix shell .#uv -c uv run python -m pipeline translate --seed

# Stage everything and commit with an automatic message (no-op if clean).
commit:
	git add -A
	git diff --cached --quiet || git commit -m "content: sync from Logseq ($(date +%F))"

# Push the current branch to its upstream.
push:
	git push
