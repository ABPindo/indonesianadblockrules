#!/bin/sh

# Switch branches
git checkout master

# add all added/modified files
git add .

# Record changes to the repository with message
git commit -am "Automatically generated"

# push to git remote repository
git push
