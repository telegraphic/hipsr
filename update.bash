#!/bin/bash
cp -R ../../hipsr/documentation/docs_build/html/ ./
git add *
git commit -a -m "Updated documentation"
git push github gh-pages