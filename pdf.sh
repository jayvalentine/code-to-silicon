#!/bin/bash

# Bash script to build a LaTeX report using pdflatex and biber.
# It is assumed that both are on the PATH.

pdflatex $1
biber $1
pdflatex $1

echo Built $1