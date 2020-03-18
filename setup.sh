#!/usr/bin/env bash
# ==============================================================================
# File      : setup.sh
# Author    : Max von Hippel
# Authored  : 13 March 2020
# Purpose   : to install the dependencies needed for Korg
# How to run: $ bash setup.sh
# ==============================================================================

# Install Spin
git clone https://github.com/nimble-code/Spin.git && cd Spin && make install && cd ..
# If this doesn't work, the binary is written to Spin/Src/spin, so you can put it in
# $HOME/.local/bin/. and then everything should work property, if you are on a *nix
# system.

# Installs green so you can run the tests with my make targets
pip3 install green

# Makes a dir to write output to
mkdir -p out

# Makes a dir to write logs to
mkdir -p logs