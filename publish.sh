python setup.py sdist bdist_wheel
git commit -v -a -m "publish  `date`"
git push origin "$(git_current_branch)"