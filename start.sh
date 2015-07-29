#!/bin/bash

sudo python shadowmirror.py &
sudo python zmq_rx.py &

