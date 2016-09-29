#!/bin/sh

set -e # exit on error

# first generate the html, since checking out gh-pages will destroy the source
cd docs && make html
cd ..

mkdir -p ../dexpy-html
mv -fv docs/build/html/* ../dexpy-html

# need to set user/email, get from env vars (will need to be set in circle)
git config --global user.email "$GH_EMAIL" > /dev/null 2>&1
git config --global user.name "$GH_NAME" > /dev/null 2>&1

git checkout gh-pages
git rm -rf .
git checkout master .gitignore
git reset HEAD
mv ../dexpy-html/* .
touch .nojekyll
echo "test:
  override:
    - echo \"test\"
" > circle.yml
git add -A
git rm .gitignore -f
git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
git push --force --quiet "https://${GITHUB_DEPLOY_TOKEN}@github.com/${CIRCLE_PROJECT_USERNAME}/${CIRCLE_PROJECT_REPONAME}.git" gh-pages > /dev/null 2>&1
