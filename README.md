DomainScrape
============

The algorithm is simple:
Takes a text list of the 10,000 [most frequently used english
words in American movie scripts](http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists#English) and compares the
last two/three letters to [each tld](tld.txt).  If there is a
match, it joins the word and tld to form a domain, places the 
domain in a priority queue, then iterates through the queue and
places it in a final list if a 404 error is returned.