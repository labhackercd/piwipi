import setuptools

setuptools.setup(
    name="piwipi",
    version="0.0.0",
    url="https://github.com/labhackercd/piwipi",

    author="Dirley Rodrigues",
    author_email="dirleyrls@gmail.com",

    description="Export EWS calendar events to JSON.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'click == 4.1',
        'pyexchange == 0.6',
        'py-dateutil == 2.2'
    ],

    entry_points={
        'console_scripts': {
            'piwipi = piwipi.main:main'
        }
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
