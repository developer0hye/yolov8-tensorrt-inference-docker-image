# --------------------------------------------------------------
# Licensed under the MIT License.
# --------------------------------------------------------------
# Dockerfile to simply run yolov8 faster with TensorRT

# Find the base image from https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch
FROM ultralytics/ultralytics:latest

LABEL author="Yonghye Kwon" 
LABEL email="developer.0hye@gmail.com"

# Download the exporter.py from the ultralytics github, the ultralytics/ultralytics:latest image does not have its updated version yet.
# It allows you to export the dynamic shape fp16 mdoel
RUN \
    apt-get update -y && \
    apt-get install -y wget && \
    cd /usr/src/ultralytics/ultralytics/engine && \
    wget -O exporter.py https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/engine/exporter.py

RUN mkdir /app/
COPY . /app/
WORKDIR /app/
