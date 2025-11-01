#!/usr/bin/env bash
set -euo pipefail

# Activate venv if present
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi

# Load Auth0 env and fetch tokens (used by tests)
source ./setup.sh
fetch_assistant || true
fetch_director || true
fetch_producer || true

# Test environment variables
export FLASK_SKIP_APP_INIT_FOR_TESTS=1
export FLASK_TESTING=1
export DATABASE_URL_TEST=${DATABASE_URL_TEST:-sqlite:////tmp/capstone_test.db}

# Run pytest
pytest -q --maxfail=1


