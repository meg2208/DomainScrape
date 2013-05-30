"""
A script that scrapes for optimal, available, domains
@author Matt Garbis
dependencies:
word frequency list ('rank\tword\tcount')
list of tlds
"""

import heapq
# http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists#English

if __name__ == '__main__':
    word_by_freq = [] 
    with open('1000mostfreqwords.txt') as freq:
        for line in freq:
            word = line[line.index('\t')+1:].split('\t')[0]
            rank = line[:line.index('\t')]
            heapq.heappush(word_by_freq, (rank, word))
    
    tlds = dict()
    with open('tld.txt') as tld:
        for line in tld:
            tlds[line[:line.index('\n')].lower()] = True
    print tlds['com']

    done = False
    domainlist = []
    while not done:
        try:
            word = heapq.heappop(word_by_freq)
        except IndexError:
           # print domainlist
            done = True
        lasttwo, lastthree = word[1][-2:], word[1][-3:]
        try:
            if tlds[lasttwo] == True and len(word[1]) >= 5:
                domainlist.append(word[1][:-2]+'.'+lasttwo)
            if tlds[lastthree] == True and len(word[1]) >= 6:
                domainlist.append(word[1][:-3]+'.'+lastthree)
        except KeyError:
            continue

   # import whois
    import urllib2

    domainlist.reverse()
    print 'REVERSED'
    done1 = False
    finaldomains = []
    while not done1:
        print finaldomains
        print len(domainlist)
        if len(domainlist) <= 1:
            done1 = True
        try:        
            domain = domainlist.pop()
            urllib2.urlopen('http://'+domain)
            print domain
            continue
        except Exception:
            print 'happened'
            finaldomains.append(domain)
            continue
    print 'BOOYAAAHHHHH!!!'
    print finaldomains

