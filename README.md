metareg
=======

Finds a short regex to match strings from one list and none from another, inspired by [Peter Norvig's](http://nbviewer.ipython.org/url/norvig.com/ipython/xkcd1313.ipynb).

This Meta-Regex Golf solution differs from Norvig's in a number of ways:

* Randomness element when generating regex components, allowing components to be of any size
* Based on the weighted set cover problem rather than vanilla set cover
* Uses simulated annealing to improve upon greedy solution

Running
-------

From the root directory, run, with python 3:

    python main.py

Strings to match and to not match can be found in, respectively:

    good_strings.txt
    bad_strings.txt

Settings like probability distributions and time spent on searching can be found in:

    metareg/settings.py

Examples
--------

Matching US presidential winners against losers:

    ay.|po|r.e$|bu|a.a|ed|i.l|di|i.*o|oo|j|a.t|ma|e.a

Matching IMDB's [top 100 films](http://www.imdb.com/chart/top) against it's [bottom 100 films](http://www.imdb.com/chart/bottom):

    yc|D.+g|Ve|A.a|R.i|do|ot$|M$|g$|·|df|aut|Ev|a.h|mu|a.c|7|L.+f+|ble|Ci|lie|^h|Mat|Dep|po|ist| D.*i|ile|gb|av|oy|or*k|ode|or |Fu|p ?.i|F.g|r. M|su|G.a|es?t|Mem
