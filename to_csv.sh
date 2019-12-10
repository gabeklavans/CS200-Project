#!/bin/bash

for filename in *.mid; do
    midicsv $filename > $filename'.csv'
done