A collection of KiCad/*.pretty by git subtree.

The script `sync.py` will import all prettys projects from
[KiCad](https://github.com/KiCad/) to current git repo with subtree.

### Usage

    mkdir fresh_project
    cd fresh_project
    git init
    ...copy sync.py to current directory...
    ./sync.py

To show helps:

    ./sync.py -h


Troubleshooting
---------------

Sometimes, import will fail with error message `Working tree has
modifications.  Cannot add.`. Just remove related local directory and
git remote manually, do a `git reset --hard` and rerun with `sync.py
-u`.
