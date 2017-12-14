# Ubuntu Desktop (GUI) ssh manager
GUI ssh manager for Linux (Ubuntu)

![alt tag](https://raw.githubusercontent.com/Doka-NT/ssh-manager/master/screenshot.png)
# Requirements
- python 3.5+
- sudo apt install python3-stdeb

# Run
```bash
# To run console version type (use -h option to see all available options):
ssh-manager
# To run GUI version type:
ssh-manager-gtk 
```

# Building deb package
```bash
python3.5 setup.py --command-packages=stdeb.command bdist_deb
```

# Config
Application can be configured by json configuration file. 
All connections defines in section connections, like provided examples.
