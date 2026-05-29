#!/bin/bash

export KAGGLE_API_TOKEN=...
export TMPDIR=$HOME/kaggle_tmp

mkdir -p $TMPDIR

uv run kaggle datasets create --dir-mode zip -p datasets
