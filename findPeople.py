import urllib2
import urllib
import csv
import json
import time
import random
# from fake_useragent import UserAgent

def getgoogleurl(search,siteurl=False):
    if siteurl==False:
        return 'http://www.google.com/search?q='+urllib2.quote(search)
    else:
        return 'http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)

def getgooglelinks(search,siteurl=False):
    #google returns 403 without user agent
    time.sleep(random.randint(15,40))
    users = ['Mozilla/11.0',
             'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
             'Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
             ]
    randomUser = users[random.randint(0,2)]
    headers = {'User-agent':randomUser}
    #user = ua.random
    #userstr = user.encode('ascii','ignore')
    #headers = {'User-agent':users[1]}    
    req = urllib2.Request(getgoogleurl(search,siteurl),None,headers)
    site = urllib2.urlopen(req)
    data = site.read()
    site.close()
    
    #no beatifulsoup because google html is generated with javascript
    start = data.find('<div id="res">')
    end = data.find('<div id="foot">')
    if data[start:end]=='':
      #error, no links to find
        return False
    else:
        links =[]
        data = data[start:end]
        start = 0
        end = 0        
        while start>-1 and end>-1:
            #get only results of the provided site
            if siteurl==False:
                start = data.find('<a href="/url?q=')
            else:
                start = data.find('<a href="/url?q='+str(siteurl))
                data = data[start+len('<a href="/url?q='):]
                end = data.find('&amp;sa=U&amp;ei=')
            if start>-1 and end>-1: 
                link =  urllib2.unquote(data[0:end])
                data = data[end:len(data)]
                if link.find('http')==0:
                    links.append(link)
    return links

def getBio(url):
    response = urllib2.urlopen(url)
    page = response.read()
    start = page.find('itemprop="description">')
    end = page.find('</span><div style="margin-top:8px;">')
    if start>-1 and end>-1: 
        bio = page[start+23:end]
        bio = bio.replace('<span id="dots"> ...</span><span id="hidden" style="display:none">','')
        bio = bio.replace('\t','')
        bio = bio.replace('\r\n','')
    else:
        bio = 'wrong page'
    return bio

def getAccFirm(bio):
    results = ''
    for auditor in auditors:
        if bio.find(auditor)>-1:
            results = results + auditor + ';'
    if len(results)==0:
        results = 'none'
    return results

def runSearch(skip):
    ctr=skip
    ceoNamePre = ''
    cfoNamePre = ''
    ceoBio = ''
    cfoBio = ''
    firmHeader = firmReader.next()
    if skip > 0:
        outputWriter.writerow('\n')
        for i in range(skip-1):
            line = firmReader.next()
    else:
        outputWriter.writerow(firmHeader)
    for row in firmReader:
        print ctr
        corpName = row[1]    
        ceoName = row[4]+' '+row[6]+' '+row[5]
        cfoName = row[8]+' '+row[10]+' '+row[9]
        
        # CEO
        if ceoName != ceoNamePre:
            links = getgooglelinks(ceoName+' '+corpName, 'http://www.bloomberg.com/')
            for link in links:
                ceoBio = 'not found'
                if link.find('personId')>-1: 
                    ceoBio = getBio(link)
                    print link
                    break
            ceoNamePre = ceoName
            
        # CFO
        if cfoName != cfoNamePre:
            links = getgooglelinks(cfoName+' '+corpName, 'http://www.bloomberg.com/')
            for link in links:
                cfoBio = 'not found'
                if link.find('personId')>-1: 
                    cfoBio = getBio(link)
                    print link
                    break
            cfoNamePre = cfoName
    
        row[13] = cfoBio
        row[14] = getAccFirm(cfoBio)

        if cfoName.find('CPA')>-1: 
            row[15]='Y' 
        else: 
            row[15]='N'

        row[16] = ceoBio
        row[17] = row[7]
        row[18] = getAccFirm(ceoBio)

        if ceoName.find('CPA')>-1: 
            row[19]='Y' 
        else: 
            row[19]='N'

        outputWriter.writerow(row)

        ctr = ctr + 1
 
        # testing
        #if ctr >= 100:
        #    break

firmFile = open('firms.csv','r')
firmReader = csv.reader(firmFile)
auditorFile = open('auditors_shortlist.csv','r')
auditorReader = csv.reader(auditorFile)

outputFile = open('output.csv','a')
outputWriter = csv.writer(outputFile)

# load auditor
auditors = []
auditorHeader = auditorReader.next()
for row in auditorReader:
    auditors.append(row[1])

# initial user agent
# ua = UserAgent()

# main
runSearch(1108)

# test getAccFrim
# tmpbio = 'I have been working at Ernst & Young LLP for 10 years. Currently, I am working at KPMG LLP.'
# print getAccFirm(tmpbio)

# test getBio()

# print getBio('http://www.bloomberg.com/research/stocks/private/person.asp?personId=12003574&privcapId=248655&previousCapId=319534&previousTitle=PVH%20B.V.')

# test getgooglelink
#links = getgooglelinks('Gregory F. Milzcik', 'http://www.bloomberg.com/')
#print links

firmFile.close()
outputFile.close()
auditorFile.close()


