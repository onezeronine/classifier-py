import random
from operator import itemgetter

# Extract data from the csv file and transform it into a feature
def extractData(fileName):
    csvFile = open(fileName, "r")
    r = csvFile.read().split("\n")
    random.shuffle(r)
    li = []
    for kvp in set(filter(None, r)):
        pair = kvp.lower().split(",")
        li.append((pair[0], pair[1]))
    return li

# Build the feature set: firstLetter, lastLetter, has and count
def extractFeatures(fi):
    features = []
    features.append("firstLetter=" + fi[0])
    features.append("lastLetter=" + fi[-1:])
    for c in "abcdefghijklmnopqrstuvwxyz":
        features.append("has("+c+")=" + str(c in fi))
        features.append("count("+c+")=" + str(fi.count(c)))
    return features

def classify(classes, model, length, featureList):
    scores = []
    for c in classes:
        score = 1
        for feature in featureList:
            n = 0
            if feature in model[c]:
                n = model[c][feature]
            score *= n + 1 / length + 1
        scores.append((c, score))

    return max(scores, key=itemgetter(1))[0]

###########################################

data = extractData('names.csv')
classes = set([f[1] for f in data])

# extract the features
featureList = [(name[1], i) for name in data for i in extractFeatures(name[0])]
n = int(len(featureList) / 5) * 4

# divide the training and test sets
trainingSet = featureList[:n]
testSet = featureList[n:]

# set the frequencies of each feature by class
model = dict()
totalCount = len(trainingSet)
for c in classes:
    model[c] = dict()
for feature in featureList:
    clss = feature[0]
    if feature[1] in model[clss]:
        model[clss][feature[1]] += 1
    else:
        model[clss][feature[1]] = 0

names = ['john', 'vanessa', 'carrie', 'phillip', 'kenneth', 'patricia', 'antonio', 'precious']
for name in names:
    print(name, classify(classes, model, totalCount, extractFeatures(name)))
