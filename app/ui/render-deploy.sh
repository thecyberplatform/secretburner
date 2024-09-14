#!/usr/bin/env bash

yarn global add @quasar/cli
export PATH="$(yarn global bin):$PATH"

yarn install

quasar build
