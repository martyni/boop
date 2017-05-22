from setuptools import setup
from pip.req import parse_requirements
import app

install_reqs = parse_requirements('requirements.txt')

reqs = [ str(ir.req) for i in install_reqs ]

setup(name='app',
      version=app.__version__,
      description='app',
      url='http://github.com/martyni/jenkins_test',
      author='martyni',
      author_email='martynjamespratt@gmail.com',
      license='MIT',
      install_requires=reqs,
      packages=['app'],
      zip_safe=False,
      entry_points = {
         'console_scripts': ['boop=app:main'],
      },
      include_package_data=True
      )
