from setuptools import setup, find_packages

classifiers = [
	"Development Status :: 4 - Beta",
	"Intended Audience :: Developers",
	"Operating System :: Microsoft :: Windows",
	"License :: OSI Approved :: MIT License",
	"Natural Language :: English",
	"Topic :: Multimedia :: Sound/Audio :: Speech",
	"Programming Language :: Python :: 3"
]

setup(
	name="software-automatic-mouth",
	version="1.0.0",
	description="A simple retro text-to-speech library",
	long_description=open("README.md").read() + '\n\n' + open("CHANGELOG.txt").read(),
	url='',
	author="flarfmatter",
	author_email="flarfmatter.contact@gmail.com",
	license="MIT",
	classifiers=classifiers,
	keywords="tts",
	packages=find_packages(),
	install_requires=['']
)