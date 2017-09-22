from distutils.core import setup

setup(name='SshManager',
      version='2.0',
      description='Ssh manager for Linux (Ubuntu)',
      author='Soshnikov Artem',
      author_email='ssh-manager@skobka.com',
      url='https://github.com/Doka-NT/ssh-manager',
      py_modules=['application', 'ssh-manager', 'ssh-manager-gtk'],
      packages=['gui', 'manager'],
      scripts=['ssh-manager', 'ssh-manager-gtk'],
      data_files=[('share/applications/ssh-manager', ['ssh-manager.desktop']),
                  ('share/pixmaps', ['ssh-manager.png'])],
      )
