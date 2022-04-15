import collections
import math
import os
import re
import datetime
import sys
import time
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


start_time = datetime.datetime.now()
cpu_start_time = time.process_time()

# h = html2text.HTML2Text()
# h.ignore_links = True
word_counts = []
allTokens = []
cpuElapsedTime = []
elapsedTimeList = []
dictOut = {}
postOut = {}
fileCount = os.listdir('files')
fileNames = []

# inputFile = "files"
# outputFile = "out"


inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])
sw = open(r"stopwords.txt", "r")
stop_words = sw.read().split()
outAll = []
allFiles = os.listdir(inputFile)
for each in allFiles:
    fileNames.append(each.split(".")[0])
    # print(each.split(".")[0])
    # exit()
    startTimeIndiv = datetime.datetime.now()
    cpustartTime = time.process_time()
    path_in = os.path.join(inputFile, each)
    with open(path_in, 'r', encoding='utf-8', errors='ignore') as HTMLFile:
        index = HTMLFile.read()
        S = BeautifulSoup(index, 'html.parser')
        rawText = S.get_text().lower()
        # removes all punctuations
        rawText = re.sub(r'[^\w\s]', '', rawText)

        # removes all numbers
        out = [each for each in rawText.split() if each.isalpha()]

        # allTokens += out
        word_counts.append(len(out))
    elapsedEndTime = datetime.datetime.now() - startTimeIndiv
    cpuEndTime = time.process_time() - cpustartTime
    elapsedTimeList.append(elapsedEndTime.total_seconds())
    cpuElapsedTime.append(cpuEndTime)

# calculates count frequency of tokens
    outCount = collections.Counter(out).most_common()
    outAll.append(outCount)

outAllList = []
# print(len(fileNames))
for each in outAll:
    outAlldict = {}
    for k, j in each:
        if j > 1 and len(k) > 1:
            outAlldict[k] = j
    outAllList.append(outAlldict)


# print(len(outAllList))
time_elapsed_v1 = []
cput_time_v1 = []

idf = dict()
for i in outAllList:
    start_t = time.time()
    cpu_start = time.process_time()
    for j in i.keys():
        if j in idf:
            idf[j] += 1
        else:
            idf[j] = 1
    time_elapsed_v1.append(time.time()-start_t)
    cput_time_v1.append(time.process_time()-cpu_start)

# print(idf.items())
cnt = 0

cpu_time_v2 = []
time_elapsed_v2 = []
for i in outAllList:
    start_t = time.time()
    cpu_start = time.process_time()
    tf = dict()
    for j in i.keys():
        tf[j] = i[j]/word_counts[cnt]*math.log(len(fileCount)/idf[j])
        postOut[j] = [fileNames[cnt], tf[j]]
    time_elapsed_v2.append(time.time()-start_t)
    cpu_time_v2.append(time.process_time() - cpu_start)
    prev = "prev_results"
    if not os.path.exists(prev):
        os.makedirs(prev)
    # outPath = os.path.join(outputFile, each + '.txt')

    f1 = open(r"" + prev + "/" + fileNames[cnt] + ".wts", "w+")  # write tokens to file
    for key, value in tf.items():
        f1.write(str([key, value]))
    f1.close()

    cnt += 1

# exec_t = []
# t_each = []
# for i in range(len(elapsedTimeList)):
#     t_each.append(elapsedTimeList[i] + time_elapsed_v1[i] + time_elapsed_v2[i])
# exec_t.append(t_each[0])
#
#
# for i in range(1, len(time_elapsed_v1)):
#     t_each[i] = t_each[i - 1] + t_each[i]
#     exec_t.append(t_each[i])

cputm = []
elpsmtm = []

cpu_time_v3 = []
time_elapsed_v3 = []

postOut = dict(sorted(postOut.items()))

count = 0
for k in idf.keys():
    st = time.time()
    cpu_st = time.process_time()
    count = 0
    for word in postOut.keys():
        count += 1
        if k == word:
            pos = count
            break
    dictOut[k] = [idf[k], pos]
    elapsedET = time.time() - st
    cpu_et = time.process_time() - cpu_st
    cpu_time_v3.append(cpu_et)
    time_elapsed_v3.append(elapsedET)

dictOut = dict(sorted(dictOut.items()))

if not os.path.exists(outputFile):
    os.makedirs(outputFile)

with open(outputFile + '/' + 'dictionaryFile.txt', 'w') as f:
    for k in dictOut.keys():
        f.write('{}\n'.format(k))
        f.write('{}\n'.format(dictOut[k][0]))
        f.write('{}\n'.format(dictOut[k][1]))

with open(outputFile + '/' + 'postingsFile.txt', 'w') as ff:
    for key in postOut.keys():
        ff.write('{},{}\n'.format(postOut[key][0], postOut[key][1]))
    f.close()
    ff.close()


filec1 = [i for i in range(503)]

cputm = [i+j+k+m for i, j, k, m in zip(cpuElapsedTime, cput_time_v1, cpu_time_v2, cpu_time_v3)]

elpsmtm = [i+j+k for i, j, k in zip(elapsedTimeList, time_elapsed_v1, time_elapsed_v2)]
# print(exect1)
# print(cputm)
#
# print("-------------------------------------------------------------------------------------------------")
#
# print(elpsmtm)
exec_t_elapsed = []
exec_t_cpu = []
exec_t_elapsed.append(elpsmtm[0])
exec_t_cpu.append(cputm[0])
for i in range(1, len(time_elapsed_v1)):
    elpsmtm[i] = elpsmtm[i - 1] + elpsmtm[i]
    cputm[i] = cputm[i - 1] + cputm[i]
    exec_t_elapsed.append(cputm[i])
    exec_t_cpu.append(elpsmtm[i])

plt.plot(filec1, exec_t_cpu)

plt.xlabel("Number of documents")
plt.ylabel("CPU Time")
plt.show()

plt.plot(filec1, exec_t_elapsed)
plt.xlabel("Number of documents")
plt.ylabel("Elapsed Time")
plt.show()