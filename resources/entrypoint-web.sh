#!/bin/sh

rm -rf /run/httpd/*
exec httpd -DFOREGROUND
