#!/bin/bash

# WARNING: This script will completely erase the commit history of the specified branch.
# Use with extreme caution and ensure you have a backup of your repository.

# Check if a branch name is provided
if [ $# -eq 0 ]; then
    echo "No branch name provided. Using 'master' as default."
    branch="master"
else
    branch=$1
fi

# Step 1: Create a new orphan branch (new_branch is a temporary name)
git checkout --orphan new_branch

# Step 2: Add all files and commit
git add -A
git commit -m "Initial commit"

# Step 3: Delete the old branch
git branch -D $branch

# Step 4: Rename the orphan branch to the original branch name
git branch -m $branch

# Step 5: Force push to overwrite the remote branch
git push -f origin $branch

echo "Repository history has been rewritten!"

