from setuptools import setup

setup(name='esfood',
      version='0.1',
      author='Dmytro Hrishko',
      author_email='dimagrshk@gmail.com',
      packages=['esparse'],
      install_requires=["elasticsearch", "requests", "bs64", "lxml"])
