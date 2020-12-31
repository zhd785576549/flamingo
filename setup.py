from setuptools import setup, find_packages

setup(
    name="flamingo",
    author="Dong Zhang",
    author_email="zhangd@lhcis.com",
    version="1.0.0",
    description="An async faster web framework.",
    license="MIT License",
    packages=find_packages(),
    keywords="Async Faster Python Web Framework",
    include_package_data=True,
    platforms="any",
    entry_points={
        "console_scripts": [
            'flamingo = flamingo.bin.flamingo:execute_from_argv',
        ]
    },
    install_requires=[
        "uvicorn",
        "bidict",
        "werkzeug",
    ],
    classifiers=[
        "Development Status :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False
)
