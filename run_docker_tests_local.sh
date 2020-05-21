#!/bin/bash
set -e

RUN="docker run --shm-size 1G --rm panda /bin/sh -c"

#docker pull docker.io/commaai/panda:latest
docker build --cache-from docker.io/commaai/panda:latest -t panda -f Dockerfile.panda .

$RUN "cd /tmp/openpilot/panda/tests/safety && ./test.sh"
$RUN "cd /tmp/openpilot/panda/tests/linter_python/ && ./flake8_panda.sh"
$RUN "cd /tmp/openpilot/panda/tests/linter_python/ && ./pylint_panda.sh"
