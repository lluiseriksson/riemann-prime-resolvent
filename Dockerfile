FROM ubuntu:24.04

LABEL org.opencontainers.image.source="https://github.com/lluiseriksson/riemann-prime-resolvent" \
      org.opencontainers.image.description="Reproducible Lean 4 and Python environment for the Riemann prime-resolvent programme"

ARG DEBIAN_FRONTEND=noninteractive
ARG ELAN_VERSION=4.2.3
ARG TARGETARCH

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates curl git graphviz make python3 python3-pip python3-venv \
       tar unzip zstd \
    && rm -rf /var/lib/apt/lists/*

# Download a versioned release asset to disk before executing it. This avoids a
# mutable master-branch installer and the unsafe `curl | sh` pattern.
RUN set -eux; \
    case "${TARGETARCH:-amd64}" in \
      amd64) elan_arch="x86_64" ;; \
      arm64) elan_arch="aarch64" ;; \
      *) echo "Unsupported Docker target architecture: ${TARGETARCH}" >&2; exit 2 ;; \
    esac; \
    curl --proto '=https' --tlsv1.2 --fail --silent --show-error --location \
      --retry 5 --retry-all-errors \
      "https://github.com/leanprover/elan/releases/download/v${ELAN_VERSION}/elan-${elan_arch}-unknown-linux-gnu.tar.gz" \
      --output /tmp/elan.tar.gz; \
    tar -xzf /tmp/elan.tar.gz -C /tmp; \
    /tmp/elan-init -y --default-toolchain none --no-modify-path; \
    rm -f /tmp/elan-init /tmp/elan.tar.gz

ENV PATH="/opt/venv/bin:/root/.elan/bin:${PATH}" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    TZ=UTC

WORKDIR /workspace

# Install dependency layers before copying the whole repository so source-only
# changes do not invalidate the Python dependency cache.
COPY requirements.txt requirements-docs.txt ./
COPY subprojects/riemann-one-point-resolvent/requirements.txt /tmp/criterion-requirements.txt
COPY subprojects/riemann-one-point-resolvent/requirements-docs.txt /tmp/criterion-requirements-docs.txt
RUN python3 -m venv /opt/venv \
    && python -m pip install --no-cache-dir \
       -r requirements.txt \
       -r requirements-docs.txt \
       -r /tmp/criterion-requirements.txt \
       -r /tmp/criterion-requirements-docs.txt

COPY . /workspace

CMD ["bash"]
