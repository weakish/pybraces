try:
    from setuptools import setup
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install as _install


def _post_install(install_lib):
    import shutil
    shutil.copy('pyend.pth', install_lib)

class install(_install):
    def run(self):
        self.path_file = 'pyend'
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post install task")

setup(
    cmdclass={'install': install},
    name="pyend",
    version="0.0.0",
    download_url='git@github.com:weakish/pyend.git',
    packages = ["pyend", "pyend.codec"],
    author='Jakukyo Friel',
    author_email='weakish@gmail.com',
    url="https://github.com/weakish/pyend",
    license='MIT',
    description="Pyend let you use `end` as block delimiter in Python.",
    long_description=open('README.md').read(),
    keywords='python end syntax indentation codec',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
