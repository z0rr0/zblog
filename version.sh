#!/usr/bin/env bash

GIT_DIR="$PWD/.git"
TARGET="blog/version.txt"

if [[ ! -d "${GIT_DIR}" ]]; then
    echo "ERROR: git directory not found"
    exit 1
fi

TAG="$(git tag | sort --version-sort | tail -1)"
VER="$(git log --oneline | head -1)"

if [[ -z "$TAG" ]]; then
    TAG="N/A"
fi
echo "git:${VER:0:7} ${TAG}" > ${TARGET}
