from setuptools import setup, find_packages

setup(
    name='DeepTune',  # Replace with your package name
    version='0.1.0',
    author='Devasy Patel, Devansh Shah',
    author_email='patel.devasy.23@gmail.com',
    description='A library for fine-tuning famous models with various backbones and loss functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Devasy23/FaceRec',  # Your GitHub repo
    packages=find_packages(),
    install_requires=[
        'tensorflow',  # For PyTorch models
        'deepface',
        'numpy',
        'scikit-learn',  # If needed for metrics
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
