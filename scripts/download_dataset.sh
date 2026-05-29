#!/bin/bash


export HF_TOKEN=...
export HF_HOME=/tmp/hf_cache_$USER

mkdir datasets

# FEText
uv run scripts/download_fetext.py


# CelebA-HQ
mkdir datasets/CelebA-HQ
curl -L -o datasets/CelebA-HQ/celebahq.zip\
  https://www.kaggle.com/api/v1/datasets/download/lamsimon/celebahq
unzip datasets/CelebA-HQ/celebahq.zip -d datasets/CelebA-HQ
mv datasets/CelebA-HQ/celeba_hq/* datasets/CelebA-HQ
rm -f datasets/CelebA-HQ/celebahq.zip
rm -rf datasets/CelebA-HQ/celeba_hq


# FFHQ 
mkdir datasets/FFHQ
curl -L -o datasets/FFHQ/flickrfaceshq-dataset-ffhq.zip\
  https://www.kaggle.com/api/v1/datasets/download/arnaud58/flickrfaceshq-dataset-ffhq
unzip datasets/FFHQ/flickrfaceshq-dataset-ffhq.zip -d datasets/FFHQ 
rm -rf datasets/FFHQ/flickrfaceshq-dataset-ffhq.zip 


# AffectNet
mkdir datasets/AffectNet
curl -L -o datasets/AffectNet/affectnet.zip\
  https://www.kaggle.com/api/v1/datasets/download/mstjebashazida/affectnet
unzip datasets/AffectNet/affectnet.zip -d datasets/AffectNet
mv "datasets/AffectNet/archive (3)"/* "datasets/AffectNet/"
rm -rf "datasets/AffectNet/archive (3)"
rm -rf datasets/AffectNet/affectnet.zip


# RAF-DB
mkdir datasets/RAF-DB
curl -L -o datasets/RAF-DB/raf-db-dataset.zip\
  https://www.kaggle.com/api/v1/datasets/download/shuvoalok/raf-db-dataset
unzip datasets/RAF-DB/raf-db-dataset.zip -d datasets/RAF-DB
mv datasets/RAF-DB/DATASET/* datasets/RAF-DB
rm -rf datasets/RAF-DB/DATASET
rm -rf datasets/RAF-DB/raf-db-dataset.zip


# SFEW
mkdir datasets/SFEW
curl -L -o datasets/SFEW/datasetssfew.zip\
  https://www.kaggle.com/api/v1/datasets/download/airanvillacorta/datasetssfew
unzip datasets/SFEW/datasetssfew.zip -d datasets/SFEW
mv datasets/SFEW/SFEW/* datasets/SFEW
rm -rf datasets/SFEW/datasetssfew.zip
rm -rf datasets/SFEW/SFEW/