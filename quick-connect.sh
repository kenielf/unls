#!/usr/bin/env sh
# <!-- Set the default folder -->
if [ -n "${ADIR}" ]; then
    directory="${ADIR}"
else
    directory="${HOME}/Projects/unls"
fi

# <!-- Source the file -->
. "${directory}/.env/bin/activate" || \
    exit "${1}"

"${directory}/src/unls" && \
    notify-send -i "applications-education" \
        "University Network" "Connected successfully!"

deactivate
