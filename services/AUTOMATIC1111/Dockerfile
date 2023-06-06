FROM alpine/git:2.36.2 as download

COPY clone.sh /clone.sh

RUN . /clone.sh taming-transformers https://github.com/CompVis/taming-transformers.git 24268930bf1dce879235a7fddd0b2355b84d7ea6 \
  && rm -rf data assets **/*.ipynb

RUN . /clone.sh stable-diffusion-stability-ai https://github.com/Stability-AI/stablediffusion.git 47b6b607fdd31875c9279cd2f4f16b92e4ea958e \
  && rm -rf assets data/**/*.png data/**/*.jpg data/**/*.gif

RUN . /clone.sh CodeFormer https://github.com/sczhou/CodeFormer.git c5b4593074ba6214284d6acd5f1719b6c5d739af \
  && rm -rf assets inputs

RUN . /clone.sh BLIP https://github.com/salesforce/BLIP.git 48211a1594f1321b00f14c9f7a5b4813144b2fb9
RUN . /clone.sh k-diffusion https://github.com/crowsonkb/k-diffusion.git 5b3af030dd83e0297272d861c19477735d0317ec
RUN . /clone.sh clip-interrogator https://github.com/pharmapsychotic/clip-interrogator 2486589f24165c8e3b303f84e9dbbea318df83e8


FROM python:3.10.9-slim

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update && \
  apt-get install -y wget git && \
  # opencv needs
  apt-get install -y libglib2.0-0 libgl1 && \
  apt-get clean
  # ffmpeg libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install xformers==0.0.20
# torch will be co-installed with xformers


RUN --mount=type=cache,target=/root/.cache/pip \
  git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git && \
  cd stable-diffusion-webui && \
  git reset --hard 20ae71faa8ef035c31aa3a410b707d792c8203a3 && \
  pip install -r requirements_versions.txt

  

ENV ROOT=/stable-diffusion-webui


COPY --from=download /repositories/ ${ROOT}/repositories/
RUN mkdir ${ROOT}/interrogate && cp ${ROOT}/repositories/clip-interrogator/data/* ${ROOT}/interrogate
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install -r ${ROOT}/repositories/CodeFormer/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
  pip install pyngrok \
  git+https://github.com/TencentARC/GFPGAN.git@8d2447a2d918f8eba5a4a01463fd48e45126a379 \
  git+https://github.com/openai/CLIP.git@d50d76daa670286dd6cacf3bcd80b5e4823fc8e1 \
  git+https://github.com/mlfoundations/open_clip.git@bb6e834e9c70d9c27d0dc3ecedeebeaeb1ffad6b

# Note: don't update the sha of previous versions because the install will take forever
# instead, update the repo state in a later step

# TODO: either remove if fixed in A1111 (unlikely) or move to the top with other apt stuff
# RUN apt-get -y install libgoogle-perftools-dev && apt-get clean
# ENV LD_PRELOAD=libtcmalloc.so

ARG SHA=20ae71faa8ef035c31aa3a410b707d792c8203a3
RUN --mount=type=cache,target=/root/.cache/pip \
  cd stable-diffusion-webui && \
  git fetch && \
  git reset --hard ${SHA} && \
  pip install -r requirements_versions.txt



# stage of dowload params in .cache dir
RUN mkdir -p /root/.cache/huggingface/hub/models--openai--clip-vit-large-patch14/snapshots && \
  GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/openai/clip-vit-large-patch14 /root/.cache/huggingface/hub/models--openai--clip-vit-large-patch14/snapshots/8d052a0f05efbaefbc9e8786ba291cfdf93e5bff && \
  wget https://huggingface.co/openai/clip-vit-large-patch14/resolve/main/pytorch_model.bin -O /root/.cache/huggingface/hub/models--openai--clip-vit-large-patch14/snapshots/8d052a0f05efbaefbc9e8786ba291cfdf93e5bff/pytorch_model.bin


WORKDIR ${ROOT}
ENV NVIDIA_VISIBLE_DEVICES=all
ENV CLI_ARGS=""
EXPOSE 7860
ENTRYPOINT python -u webui.py --listen --port 7860 ${CLI_ARGS}
