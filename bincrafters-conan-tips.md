Bincrafter's Conan Tips
=======================

*Practical day to day conan usage. This guide is always a work in progress.*

Introduction
============

Conan is a very powerful tool that greatly diminishes project setup time. When used exclusively, it also shortens configuration files considerably, automating builds and improving maintainability at the same time. Bincrafters members are software developers who use conan during their day-to-day work. We are not professional "packagers" but, since we package open source libraries for our own use, we have come together to create a common pool of high quality packages for ourselvesand the rest of the conan community, and also to learn from each other and increase our efficiency and quality of work by establishing a set of good common practices.

This guide is not a replacement for the [conan documentation](http://docs.conan.io/en/latest/). As a matter of fact, it often references it. Its purpose is help you navigate learning conan and advance quickly without getting lost in the details. It is based on our experience of doing so ourselves and the insights we have developed while packaging, testing and using various libraries in our own projects. It is probably a good idea to read it sequentially if you have just started out with conan. On the other hand, if you are a more experienced user, it is probably best to just skim through the titles to go directly to the next tip that catches your attention.

Tip 1: Set up conan with virtualenv
===================================
One of the first things you will do when starting out with conan is of course installing it. On the [download page](https://www.conan.io/downloads) you will notice that there are various ways to do that: installation programs, from source code, from pypi or even from homebrew on MacOS. We suggest setting up conan under virtualenv, using pip. It may seem simpler to just run a setup wizard, but this method will make updating to the latest conan version a breeze, and that is something that is needed quite often. Once you have installed python and virtualenv on your system, do the following:

	virtualenv vconan --no-site-packages
	
You have created your virtual environment. Every time you need to activate it, you need to do the following on Linux and MacOS. Do that now:

	source vconan/bin/activate
	
Note that, on Windows, things are a little different:

	.\vconan\scripts\activate
	
Your virtual environment is now activated. Notice that its name appears in parenthesis in front of your command prompt.

Make sure you have the latest version of pip installed in your virtual environment:

	pip install --upgrade pip
	
We can then install conan:

	pip install conan
	
That's all! Let's run a conan command:

	conan --version
	
In order to deactivate the virtual environment (thus no longer being able to run conan), do the following:

	deactivate
	
Conan has now been set up with virtualenv. And since virtualenv makes it so easy, it is a good idea to always make sure you have the latest version of pip and conan every time you activate it:

	source/vconan/bin/activate or .\vconan\scripts\activate
	pip install --upgrade pip
	pip install --upgrade conan

*You may have noticed that we have made no reference to brew. You can certainly use brew as the conan download page suggests if you have a Mac, but we wanted to make the point that you do not have to. MacOS comes with Python preinstalled and you can install virtualenv directly there with easy_install and sudo*: `sudo pip easy_install virtualenv`
