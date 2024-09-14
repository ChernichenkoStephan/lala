DATE=$$(date "+%Y_%m_%d")
include ./deployments/.env.plain
$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' ./deployments/.env.plain))

# Help
help:
	@echo "Available commands:"
	@echo "  r                - Run the application with uvicorn (remember to set local envs)" 
	@echo "  l                - Format and lint the code"
	@echo "  bl               - Run the benchmark for the application"

# Deploy

r: l
	rye run python -m uvicorn --app-dir ./src/lala lala.main:app --reload

# Bench

bl:
	rye run python ./src/tests/bench_lala.py

# Linters

l:
	rye fmt
	rye lint ./src