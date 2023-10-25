import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Co-op",
    version="0.0.1",
    author="Anonymous Author",
    author_email="anonymous@anonymous.com",
    description="Counterfactual operators (Co-op) lib to improve causal inferences from visualizations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="anonymous",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
