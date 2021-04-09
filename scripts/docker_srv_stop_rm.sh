#!/bin/bash

set -e -x

sudo docker container stop vocabulary_srv_container
sudo docker container rm vocabulary_srv_container
