import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discordpy-replit-heroku",
    version="0.0.1",
    author="1__hi__1",
    description="Host a repl based discord.py bot indefinetly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syntax-corp/discordpy-replit-heroku",
    project_urls={
        "Issue tracker": "https://github.com/syntax-corp/discordpy-replit-heroku/issues",
      },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
