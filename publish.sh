# Bump version
# Build new package
# Commit
# and Push
python -c "major, minor = open('version.txt').read().rsplit('.',1);open('version.txt','w').write(major+'.'+str(int(minor)+1))" &&
python setup.py sdist bdist_wheel &&
git commit -v -a -m "publish  `date`" &&
git push