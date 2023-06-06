FROM xiangxiaoyu/sd-webui:basic

WORKDIR ${ROOT}/extensions
COPY ./index.json .
COPY ./download.py .
RUN --mount=type=cache,target=/root/.cache/pip \
  python -u ./download.py

WORKDIR ${ROOT}/repositories
RUN git clone https://github.com/isl-org/MiDaS.git midas

WORKDIR ${ROOT}

RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update && \
  # extensions needs those
  apt-get install -y g++ && \
  apt-get clean
  # ffmpeg libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev

RUN --mount=type=cache,target=/root/.cache/pip \
  pip install diffusers && \
  pip install scikit-learn clip-interrogator rembg trimesh dynamicprompts pycocotools vispy send2trash color_matcher segmentation-refinement transforms3d image-reward && \
  pip install git+https://github.com/facebookresearch/segment-anything.git

RUN --mount=type=cache,target=/root/.cache/pip \
  pip install openai boto3 chardet translators

ENV NVIDIA_VISIBLE_DEVICES=all
ENV CLI_ARGS=""
EXPOSE 7860
ENTRYPOINT python -u webui.py --listen --port 7860 ${CLI_ARGS}


# sudo docker run -it --rm  -p 7860:7860 --entrypoint "/bin/bash"  \
# --mount type=bind,source=/home/xcd/sd-ckpt,target=/stable-diffusion-webui/models/Stable-diffusion \
# extension