#!/bin/sh

GH_PAGES_SOURCES="docs/source docs/Makefile"

git checkout gh-pages
rm -rf docs/build docs/_sources docs/_static
git rm -rf .
git checkout master $GH_PAGES_SOURCES .gitignore
git reset HEAD
cd docs && make html
mv -fv docs/build/html/* .
rm -rf $GH_PAGES_SOURCES docs/build
touch .nojekyll
git add -A
git rm .gitignore -f
git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master
