#!/bin/sh

# move sample_code away
# run pdoc3
mv docs test_results
rm -rf html
mv run.py ../
mv wsgi.py ../
mv reference ../
doc.sh
mv ../reference .
mv html/curr_portoflio docs || true
mv html/financial-dump docs || true
mv ../run.py .
mv test_results docs