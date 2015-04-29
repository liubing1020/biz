import csv

def getAccFirm(bio):
    results = ''
    for auditor in auditors:
        if bio.find(auditor)>-1:
            results = results + auditor + ';'
    if len(results)==0:
        results = 'none'
    return results

def runClean():
    firmHeader = firmReader.next()
    outputWriter.writerow(firmHeader)
    for row in firmReader:
        cfoBio = row[13]
        row[14] = getAccFirm(cfoBio)
        ceoBio = row[16]
        row[18] = getAccFirm(ceoBio)
        outputWriter.writerow(row)

firmFile = open('results.csv','r')
firmReader = csv.reader(firmFile,dialect='excel')
auditorFile = open('auditors_1000.csv','r')
auditorReader = csv.reader(auditorFile)

outputFile = open('firm_results.csv','w')
outputWriter = csv.writer(outputFile)

# load auditor
auditors = []
auditorHeader = auditorReader.next()
for row in auditorReader:
    auditors.append(row[1])


# main
runClean()

# test getAccFrim
# tmpbio = 'I have been working at Ernst & Young LLP for 10 years. Currently, I am working at KPMG LLP.'
# print getAccFirm(tmpbio)

firmFile.close()
outputFile.close()
auditorFile.close()


