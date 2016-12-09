#!/bin/sh

echo 'push' >> Misc/foo.txt
git add Misc/foo.txt
git commit -m "only for push"
git push

echo 'Bingo!'
