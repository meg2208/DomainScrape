"""
A script that scrapes for optimal, available, domains
@author Matt Garbis
dependencies:
word frequency list ('rank\tword\tcount')
list of tlds
"""

import heapq
import time
from datetime import timedelta, datetime
from urllib2 import urlopen
import urllib2
import sys
import socket

def run(FreqFile = '10000mostfreqwords.txt', tldFile = 'tld.txt'):
    word_by_freq = createFreqHeap(FreqFile)
    tlds = createTLDdict(tldFile)
    domainlist = getDomains(word_by_freq, tlds)
    finaldomains = getUnusedDomains(domainlist, 1) # 1 minute limit
    print finaldomains

def createFreqHeap(FreqFile = '10000mostfreqwords.txt'):
    word_by_freq = [] 
    with open(FreqFile) as freq:
        for line in freq:
            word = line[line.index('\t')+1:].split('\t')[0]
            rank = line[:line.index('\t')]
            heapq.heappush(word_by_freq, (rank, word))
    return word_by_freq

def createTLDdict(tldFile = 'tld.txt'):
    tlds = dict()
    with open(tldFile) as tld:
        for line in tld:
            line = line.split('\n')[0].lower()
            tlds[line] = True
    return tlds

def getDomains(word_by_freq, tlds):
    done = False
    domainlist = []
    while not done:
        try:
            word = heapq.heappop(word_by_freq)
            lasttwo, lastthree = word[1][-2:], word[1][-3:]
        except IndexError:
            done = True
        try:
            if tlds[lasttwo] == True and len(word[1]) >= 5:
                domainlist.append(word[1][:-2]+'.'+lasttwo)
            if tlds[lastthree] == True and len(word[1]) >= 6:
                domainlist.append(word[1][:-3]+'.'+lastthree)
        except KeyError:
            continue
    return domainlist

def getUnusedDomains(domainlist, minlimit = 1):
    domainlist.reverse()
    done, finaldomains = False, []
    minlim = datetime.now() + timedelta(minutes = minlimit)
    while not done and not tooLong(minlim, minlimit):
        if len(domainlist) <= 1:
            done = True
        else:
            domain = domainlist.pop()
            print domain
            req = urllib2.Request('http://'+domain)
        try:        
            socket.setdefaulttimeout(8)
            urlopen(req)
        except Exception, e:
            print e.reason
            if e.reason[0] == 61 and not tooLong(minlim, minlimit):
                finaldomains.append(domain)
    return finaldomains

def tooLong(minlim, mins):
    percent = (1-(minlim - datetime.now()).total_seconds()/(60*mins))*100
    sys.stdout.write("%3d%%\r" % percent)
    sys.stdout.flush()
    return datetime.now() > minlim

if __name__ == '__main__':
    run()
