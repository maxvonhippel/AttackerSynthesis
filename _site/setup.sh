#!/usr/bin/env bash
# ==============================================================================
# File      : setup.sh
# Author    : Max von Hippel
# Authored  : 13 March 2020
# Purpose   : to install the dependencies needed for Korg
# How to run: $ bash setup.sh
# ==============================================================================

# Install Spin
git clone https://github.com/nimble-code/Spin.git && cd Spin && make install 

# Installs green so you can run the tests with my make targets
pip3 install green