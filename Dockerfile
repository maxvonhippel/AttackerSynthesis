FROM ubuntu:latest
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y upgrade
RUN DEBIAN_FRONTEND="noninteractive" \
	apt-get install -y apt-utils python3-pip
RUN python3 -m pip install --upgrade pip
RUN DEBIAN_FRONTEND="noninteractive"     \
	apt-get install -y build-essential   \
                       python-dev        \
                       python-setuptools \
                       git               \
                       bison             \
                       flex              \
                       graphviz          \
                       time              \
                       tree
RUN pip3 install green
# Install Spin
RUN git clone https://github.com/nimble-code/Spin.git
WORKDIR Spin
WORKDIR Bin
RUN gunzip spin651_linux64.gz
RUN chmod +x spin651_linux64
RUN cp spin651_linux64 /usr/local/bin/spin
WORKDIR ../..
# Copy KORG
COPY . KORG
WORKDIR KORG
ENV REPRDIR=example.attacks/redo.korg.results.with.partial.order.reduction
RUN mv $REPRDIR/alternativeCharacterize.py korg/Characterize.py
RUN pip3 install .
# Test KORG installation
RUN make test
# Reproduce results from KORG ArXiV paper
RUN make clean
RUN make experimentKorg
RUN tree out
RUN python3 analysis/compare2arxiv.py
entrypoint [""]