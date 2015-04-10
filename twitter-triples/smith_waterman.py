import sys

gapCost = 0.5

maxCost = 1.0

def getCost(str1, str1Indx, str2, str2Indx):
    if len(str1) <= str1Indx or str1Indx < 0:
        return 0
    if len(str2) <= str2Indx or str2Indx < 0:
        return 0
    if str1[str1Indx] == str2[str2Indx]:
        return 1.0
    else:
        return -2.0

def getUnNormalisedSimilarity(string1, string2):
    n = len(string1)
    m = len(string2)
    if n == 0:
        return m
    if m == 0:
        return n
    d = [[0 for x in range(m)] for x in range(n)]
    maxSoFar = 0.0
    for i in range(0, n):
        cost = getCost(string1, i, string2, 0)
        if i == 0:
            d[0][0] = max(0, -gapCost, cost)
        else:
            d[i][0] = max(0, d[i-1][0] - gapCost, cost)
        if d[i][0] > maxSoFar:
            maxSoFar = d[i][0]
    for j in range(0, m):
        cost = getCost(string1, 0, string2, j)
        if j == 0:
            d[0][0] = max(0, -gapCost, cost)
        else:
            d[0][j] = max(0, d[0][j-1] - gapCost, cost)
        if d[0][j] > maxSoFar:
            maxSoFar = d[0][j]
    for i in range(1, n):
        for j in range(1, m):
            cost = getCost(string1, i, string2, j)
            d[i][j] = max(0, d[i-1][j] - gapCost, d[i][j-1] - gapCost, d[i-1][j-1] + cost)
            if d[i][j] > maxSoFar:
                maxSoFar = d[i][j]
    return maxSoFar

def getSimilarity (string1, string2):
    unNormalizedSimilarity = getUnNormalisedSimilarity(string1, string2)
    maxValue = min(len(string1), len(string2))
    if maxCost > (-gapCost):
        maxValue = maxValue * maxCost;
    else:
        maxValue = maxValue * -gapCost
    if maxValue == 0:
        return float(maxCost)
    else:
        return float(unNormalizedSimilarity/maxValue)

if __name__ == "__main__":
    print(getSimilarity("Miliman", "Milliman"))
    print(getSimilarity("Nischal", "Nishal"))
    print(getSimilarity("Nischal", "Nikhil"))
    print(getSimilarity("Nischal", "Bharath"))
    print(getSimilarity("Cameron", "David Cameron"))
