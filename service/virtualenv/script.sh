#!/usr/bin/bash

if ! grep "WORKON_HOME" ~/.bashrc; then echo -e "export PATH='$PATH:/home/projects/.local/bin'\nexport WORKON_HOME='~/.virtualenv'\nexport VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3\nsource /home/projects/.local/bin/virtualenvwrapper.sh" | tee -a ~/.bashrc; else echo 'exists!'; fi

# must being installed under user 'projects' so that 'vagrant' doesn't have such virtualenvwrapper
yes | pip3 install virtualenvwrapper --user

