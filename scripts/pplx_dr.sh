#!/usr/bin/env bash

# pplx_dr.sh - Perplexity Deep Research API wrapper
# Usage: ./pplx_dr.sh "your research query"

set -e

# Check if query argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No query provided" >&2
    echo "Usage: $0 \"your research query\"" >&2
    exit 1
fi

QUERY="$1"

# Check if PERPLEXITY_API_KEY is set in environment
if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "Error: PERPLEXITY_API_KEY environment variable not set" >&2
    exit 1
fi

# Make API request
curl -s -X POST "https://api.perplexity.ai/chat/completions" \
    -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"sonar-deep-research\",
        \"messages\": [
            {
                \"role\": \"user\",
                \"content\": $(printf '%s' "$QUERY" | jq -Rs .)
            }
        ]
    }"
