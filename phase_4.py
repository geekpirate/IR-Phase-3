
import os
import sys
import time
from heapq import nlargest


def checkQueryWeights(args):
    if args[1] in ["wt", "Wt", "wt", "WT"]:
        if len(args) < 4:
            print("Invalid input. please check and try again")
            return None
        else:
            return True
    return False


def getQeuryTerms(inputWeights, input):
    queryWeightsDict = {}
    if inputWeights:
        for i in range(2, len(input)-1, 2):
            try:
                key = input[i].lower()
                value = input[i + 1]
                value = float(value)
                queryWeightsDict[key] = value
            except ValueError:
                print("Invalid input. please check and try again")
                exit()
    else:
        for i in range(1, len(input)):
            queryWeightsDict[input[i].lower()] = 1
    queryTerms = list(queryWeightsDict.keys())
    return queryTerms, queryWeightsDict


def getDictionaryPostingList(dictFileName, postingFileName):
    dictionaryFile = open(dictFileName, "r")
    dictionaryList = dictionaryFile.read().rstrip("\n").split("\n")
    dictionaryFile.close()
    postingsFile = open(postingFileName, "r")
    postingsFileList = postingsFile.read().rstrip("\n").split("\n")
    postingsFile.close()
    return dictionaryList, postingsFileList


def getTermWeightDict(dictionaryList, postingsFileList, queryWeightsDict):
    termWeightsDict = {}
    for i in range(0, len(dictionaryList), 3):
        word = dictionaryList[i]
        step = int(dictionaryList[i+1])
        index = int(dictionaryList[i+2])
        if word in queryWeightsDict:
            inputWeight = queryWeightsDict[word]
            temp_postings_list = postingsFileList[index-1:index+step-1]
            for each in temp_postings_list:
                each = each.split(",")
                fileName = each[0]
                wieght = float(each[1].strip())
                termWeightsDict[fileName] = termWeightsDict.get(
                    fileName, wieght*inputWeight)+(wieght*inputWeight)
    return termWeightsDict


def getTopRanks(termWeightsDict):
    print("Files with highest ranks")
    top10Files = []
    n = 10
    topN = nlargest(n, termWeightsDict, key=termWeightsDict.get)
    for each in topN:
        top10Files.append(each)
        print(each + ".html", ":", termWeightsDict.get(each))
    return top10Files


def getTop10TFIDF(dictionaryList):
    out = {}
    top = 10
    for i in range(0, len(dictionaryList), 3):
        term = dictionaryList[i]
        step = int(dictionaryList[i + 1])
        index = int(dictionaryList[i + 2])
        posting = postingsFileList[index - 1:index + step - 1]
        termDict = {}
        for each in posting:
            each = each.split(",")
            fileName = each[0]
            weight = float(each[1].strip())
            termDict[fileName] = weight
        out[term] = termDict
    termWeightsKey = {}
    for word, token in out.items():
        for fileName, wgt in token.items():
            termWeightsKey.setdefault(fileName, {})[word] = wgt
    for each, token in termWeightsKey.items():
        if each in top10Files:
            highWeightTerms = nlargest(top, token, key=token.get)
            print("top 10 tf*idf terms in ", each + ".html")
            for each in highWeightTerms:
                print(each, token[each])


dictFileName = "outdictionaryFile.txt"
outFileName = "outpostingsFile.txt"
input = sys.argv
inputWeights = False

inputWeights = checkQueryWeights(input)
if inputWeights is None:
    exit()

queryTerms, queryWeightsDict = getQeuryTerms(inputWeights, input)
print("Query Output", queryTerms)

dictionaryList, postingsFileList = getDictionaryPostingList(dictFileName, outFileName)

termWeightsDict = getTermWeightDict(dictionaryList, postingsFileList, queryWeightsDict)

top10Files = getTopRanks(termWeightsDict)

getTop10TFIDF(dictionaryList)
