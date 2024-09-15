#!/usr/bin/env bash

npm install -g @quasar/cli
export PATH="$(npm bin -g):$PATH"

npm install

quasar build
