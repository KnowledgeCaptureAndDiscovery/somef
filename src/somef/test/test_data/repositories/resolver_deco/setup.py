from setuptools import setup


setup(name='resolver_deco',
      version='1.0.4',
      description='Decorator for resolve function arguments',
      classifiers=[
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3",
          "Development Status :: 5 - Production/Stable",
      ],
      author='Alexander Zelenyak',
      author_email='zzz.sochi@gmail.com',
      license='BSD',
      url='https://github.com/zzzsochi/resolver_deco',
      keywords=['dotted'],
      py_modules=['resolver_deco'],
      install_requires=['zope.dottedname'],
      tests_require=['pytest'],
)
