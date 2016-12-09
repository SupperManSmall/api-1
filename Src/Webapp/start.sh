#!/bin/sh
uwsgi -s 127.0.0.1:9090 --daemonize /home/git/AutoTest/Output/Log/uwsgi.log -w webapp.py
