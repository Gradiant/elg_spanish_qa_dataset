#!/bin/bash

NAME=elg_spanish_qa_dataset
TAG=1.0
docker build -t ${NAME}:${TAG} .
