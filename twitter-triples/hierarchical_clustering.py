import sys

from smith_waterman import String_Comparer

SIMILARITY_THRESHOLD = 0.8

def computeSimilarity(cluster1, cluster2):
    similarity = 0
    comparer=String_Comparer(0.5,1.0)
    for string1 in cluster1:
        for string2 in cluster2:
            similarity += comparer.getSimilarity(string1.lower(), string2.lower())
    return float(similarity / (len(cluster1) * len(cluster2)))

def createClusters(strings):
    clusters = []
    for string in strings:
        cluster = []
        cluster.append(string)
        clusters.append(cluster)
    return clusters

def buildClusters (strings):
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
                for k in range(0, len(clusters[maxMatchIndex])):
                    clusters[i].append(clusters[maxMatchIndex][k])
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
    for cluster in clusters:
        print(cluster)

