# system-manager
Python application to manage packages installed and removed on an arch system

This application installs packages using pacman or yay and stores the package name in a json file.

When you need to reinstall, the json file already contains all packages installed. The application will "sync" the system
according to the install and uninstall list in the json file.

Usage:

**Add package**

    sm.py -a <package>

Installs a package and upon successfull install write the package to the install section of the json file

**Remove package**

    sm.py -r <package>

Removes the package from the system, removes it from the install section and adds it to the uninstall section

**Sync**

    sm.py -s
    
Usefull for new installs. Uses the json file to install and remove packages so the system is in sync with the json packages lists.




