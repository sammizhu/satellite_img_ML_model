from setuptools import setup, find_packages

setup(
    name="MOSAIKS_feature",  
    version="0.1.0",
    author="Sammi Zhu",
    author_email="sammizhu@college.harvard.edu",
    description="A library for processing features and polygon overlap analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sammizhu/satellite_img_ML_model", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy", 
        "pandas",
        "shapely.geometry",
        "unittest",
    ],
)