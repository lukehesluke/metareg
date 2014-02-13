metareg
=======

Finds a short regex to match strings from one list and none from another, inspired by [Peter Norvig's](http://nbviewer.ipython.org/url/norvig.com/ipython/xkcd1313.ipynb)

Running
-------

From the root directory, run, with python 3:

    python main.py

Strings to match and to not match can be found in, respectively:

    good_strings.txt
    bad_strings.txt

Settings like probability distributions and time spent on searching can be found in:

    metareg/settings.py
