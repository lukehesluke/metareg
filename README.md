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

    python main.py <STRINGS TO MATCH> <STRINGS TO NOT MATCH>

e.g.

    python main.py examples/aristotle_quotes.txt examples/gold_digger_lyrics.txt

Settings like probability distributions and time spent on searching can be found in:

    metareg/settings.py

Examples
--------

Matching US presidential winners against losers:

    ay.|po|r.e$|bu|a.a|ed|i.l|di|i.*o|oo|j|a.t|ma|e.a

Matching IMDB's [top 100 films](http://www.imdb.com/chart/top) against it's [bottom 100 films](http://www.imdb.com/chart/bottom):

    yc|D.+g|Ve|A.a|R.i|do|ot$|M$|g$|·|df|aut|Ev|a.h|mu|a.c|7|L.+f+|ble|Ci|lie|^h|Mat|Dep|po|ist| D.*i|ile|gb|av|oy|or*k|ode|or |Fu|p ?.i|F.g|r. M|su|G.a|es?t|Mem

Matching [Shakespeare quotes](http://pastebin.com/2AwJ9CTq) against [Aristotle quotes](http://pastebin.com/2AwJ9CTq):

    ad b|Be| .ew|h as|â|Mai|av.n| .ge|rg|ou. d|Br|Lo.e |hs|ch*,|^I |doo|-l|w n*o| da|u |m s|, I|Le|bon| pr.ve|y;|ar.$| .tr|rue|T.ey|, T|fat|gu|^To|n.le|!|eart|w\.|ull|e wor|my|oy|bor|f no*t|foo|ub|^U| ste|cky|a.fu|fal|gel|Sc|th b|e.pt|I c|nt.y

And, of course, Shakespeare quotes against [Golddigger lyrics](http://www.azlyrics.com/lyrics/kanyewest/golddigger.html):

    !$| re|\.| de
