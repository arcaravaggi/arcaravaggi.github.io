#!/bin/bash
# Build
hugo --minify
# Deploy
cd public
git init
git add .
git commit -m "Deploy site"
git branch -M main
git remote add origin https://github.com/arcaravaggi/arcaravaggi.github.io.git
git push -f origin main