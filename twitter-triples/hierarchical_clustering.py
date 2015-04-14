import sys

import smith_waterman

SIMILARITY_THRESHOLD = 0.8
SIMILARITY_THRESHOLD_WITH_WEIGHTS = 0.5

def computeSimilarity(cluster1, cluster2):
    similarity = 0
    for string1 in cluster1[0]:
        for string2 in cluster2[0]:
            similarity += smith_waterman.getSimilarity(string1.lower(), string2.lower())
    overallSimilarity = float((similarity) / (len(cluster1[0]) * len(cluster2[0])))
    return overallSimilarity

def createClusters(strings):
    clusters = []
    for string in strings:
        cluster = []
        cluster.append(string[0])
        clusters.append((cluster, string[1]))
    return clusters

def buildClusters (strings, applyWeights = False):
    #print(strings)
    clusters = createClusters(strings)
    searchForClusters = True
    while searchForClusters == True and len(clusters) != 1:
        searchForClusters = False
        for i in range(0, len(clusters)):
            maxatchIndex = -1
            maxSimilarity = 0
            for j in range(i+1, len(clusters)):
                similarity = computeSimilarity(clusters[i], clusters[j])
                if similarity > maxSimilarity:
                    maxMatchIndex = j
                    maxSimilarity = similarity
            if maxSimilarity > SIMILARITY_THRESHOLD:
                weight = float(clusters[i][1]/clusters[maxMatchIndex][1])
                if clusters[i][1] > clusters[maxMatchIndex][1]:
                    weight = float(clusters[maxMatchIndex][1]/clusters[i][1])
                if applyWeights == False or float(maxSimilarity * weight) > SIMILARITY_THRESHOLD_WITH_WEIGHTS:
                    clusters[i][0].extend(clusters[maxMatchIndex][0])
                    clusters[i] = (clusters[i][0], clusters[i][1] + clusters[maxMatchIndex][1])
                    clusters.pop(maxMatchIndex)
                    searchForClusters = True
    return clusters

if __name__ == "__main__":
    inputFile = open(sys.argv[1])
    strings = []
    for line in inputFile:
        line = line.rstrip(" \t\n\r")
        parts = line.split(" ")
        prev = False
        previous = ""
        for i in range(0, len(parts)):
            if parts[i].endswith(("/^", "/Z")):
                if parts[i].endswith("/Z"):
                    parts[i] = parts[i].replace("'s", "")
                parts[i] = parts[i][:-2]
                if parts[i] not in strings:
                    strings.append(parts[i])
                if prev == True:
                    previous = previous + " " + parts[i]
                else:
                    prev = True
                    previous = parts[i]
            else:
                if prev == True:
                    if previous not in strings:
                        strings.append(previous)
                prev = False
    inputFile.close()
    clusters = buildClusters(strings)
    #for cluster in clusters:
        #print(cluster)

