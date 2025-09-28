#!/bin/bash

echo "${APP_NAME^^} - NextJS CONTAINER STARTING..."


# Check for required env vars, exit as failure if missing these critical env vars.
if [[ -z "${APP_ENV}" ]]; then
    echo "█████████████████████████████████████████████████████████████████████████████████████████████████████████████"
    echo "█ CRITICAL ERROR: Missing 'APP_ENV' environment variables."
    echo "█████████████████████████████████████████████████████████████████████████████████████████████████████████████"
    echo "APP_ENV=" $APP_ENV
    echo "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
    exit
fi

# CI TEST DOWN THE TRACK

# ====================================================================================
# Run inbuilt nextjs server if ENV is LOCAL
# ====================================================================================
if [ "${APP_ENV^^}" = "DEVELOPMENT" ]; then
    # Install dependencies (idk why it's not installing the latest ones in the docker image)
    npm install
    # Run developments
    echo "  "
    echo "======= Starting inbuilt nextjs webserver ==================================================================="
    npm run dev
    exit
fi

npm run start