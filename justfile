set shell := ["bash", "-c"]

# Generate the sanitized public data (does not build the site).
data:
	uv run python -m pipeline build

# Build the static site from the generated data.
site:
	hugo --gc --minify

# The full public build: data first, then the site that consumes it.
build: data site

# Preview the site locally.
serve:
	hugo server

# Run the pipeline tests.
test:
	uv run pytest
