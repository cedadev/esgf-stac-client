FROM mcr.microsoft.com/devcontainers/anaconda:0-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

RUN mkdir -p /workspaces
# Install Pystac
RUN cd /workspaces/ \
    && git clone -b asset-search https://github.com/cedadev/pystac \
    && cd pystac/ \
    && pip install -r requirements-dev.txt \
    && pip install -e . --no-deps
# Install Pystac-client
RUN cd /workspaces/ \
    && git clone -b asset-search https://github.com/cedadev/pystac-client \
    && cd pystac-client/ \
    && perl -p -i -w -e 's/pystac==1.4.0/#pystac==1.4.0/g' requirements-min.txt \
    && pip install -r requirements-min.txt \
    && pip install -r requirements-dev.txt \
    && pip install -e . --no-deps
# Mark installed repos as safe
RUN git config --system --add safe.directory /workspaces/pystac
RUN git config --system --add safe.directory /workspaces/pystac-client
