A collection of KiCad/*.pretty by git subtree.

### Usage

    ./sync.py

To show helps:

    ./sync.py -h


Troubleshooting
---------------

Sometimes, import will fail with error message `Working tree has
modifications.  Cannot add.`. Just remove related local directory and
git remote manually, do a `git reset --hard` and rerun with `sync.py
-u`.
