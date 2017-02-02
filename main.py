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

# extract the names and classes from the .csv file
data        = extractData('names.csv')
classes     = set([f[1] for f in data])
n           = int(len(data) / 5) * 4

# divide the data into 4/5 into training set, 1/5 into test set
trainingSet = data[:n]
testSet     = data[n:]

# flatten the features into a list
trainingFeatureList = [(name[1], i) for name in trainingSet for i in extractFeatures(name[0])]

# set the frequencies of each feature by class
model = dict()
for c in classes: model[c] = dict()
for feature in trainingFeatureList:
    featureClass = feature[0]
    if feature[1] in model[featureClass]: model[featureClass][feature[1]] += 1
    else: model[featureClass][feature[1]] = 0

# Classify the extracted features from the name
def classifyFeatureList(nameFeatureList):
    scores = []
    featureSet = set(trainingFeatureList)
    vocabularyCount = len(list(featureSet))
    for c in classes:
        score = len([x for x in trainingSet if x[1] == c]) / len(trainingSet)
        countOfFeaturesInTheClass = len([x for x in trainingFeatureList if x[0] == c])
        for nf in nameFeatureList:
           featFrequencyPerClass = 0
           if nf in model[c]: featFrequencyPerClass = model[c][nf]

           score *= (featFrequencyPerClass + 1) / (countOfFeaturesInTheClass + vocabularyCount + 1)
        scores.append((c, score))
    return max(scores, key=itemgetter(1))[0]

# Use for the UI
def classify(name):
    print(classifyFeatureList(extractFeatures(name)))

def test():
    evaluationResult = dict()
    for c1 in classes:
        evaluationResult[c1] = dict([(x, 0) for x in classes])

    for name in testSet:
        assignedClass = classifyFeatureList(extractFeatures(name[0]))
        trueClass = name[1]
        evaluationResult[trueClass][assignedClass] += 1

    for c1 in classes:
        numerator = evaluationResult[c1][c1];
        precisionDenominator = 0;
        recallDenominator = 0;
        for c2 in classes:
            precisionDenominator += evaluationResult[c2][c1]
            recallDenominator += evaluationResult[c1][c2]
        precision = (numerator / precisionDenominator)
        recall = (numerator / recallDenominator)
        f = (2 * precision * recall) / (precision + recall)
        print('Precision(' + c1 + ') => ' + str(precision))
        print('Recall(' + c1 + ')    => ' + str(recall))
        print('F(' + c1 + ')         => ' + str(f))
