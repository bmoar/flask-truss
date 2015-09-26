#!/usr/bin/env bash

set -eu
set -o pipefail

nosetests --with-coverage --cover-package=flask_truss --cover-branches $@
