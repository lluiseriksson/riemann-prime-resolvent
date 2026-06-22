FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git python3 zstd unzip make texlive-latex-base \
    texlive-latex-recommended texlive-fonts-recommended \
  && rm -rf /var/lib/apt/lists/*

RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf \
    | sh -s -- -y
ENV PATH="/root/.elan/bin:${PATH}"

WORKDIR /workspace
COPY . /workspace
RUN lake exe cache get && lake build && lake env lean oracle_check.lean

CMD ["bash"]
