from setuptools import setup
import app
setup(name='app',
      version=app.__version__,
      description='app',
      url='http://github.com/martyni/jenkins_test',
      author='martyni',
      author_email='martynjamespratt@gmail.com',
      license='MIT',
      packages=['app'],
      zip_safe=False,
      entry_points = {
         'console_scripts': ['poop=app:main'],
      },
      include_package_data=True
      )
