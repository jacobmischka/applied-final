import json, csv, os, sys
from nltk.corpus import stopwords
from datetime import datetime

stopWords = stopwords.words("english")

features = {"sentiment": 0}
with open("positive-words.txt") as file:
    for line in file:
        line = line.strip()
        if line != "" and not line.startswith(";"):
            features[line] = 0

with open("negative-words.txt") as file:
    for line in file:
        line = line.strip()
        if line != "" and not line.startswith(";"):
            features[line] = 0

count = 0
featureCount = features.copy()
featureCount["sentiment"] = 10000

if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    sys.exit()

if len(sys.argv) > 2:
    iterations = int(sys.argv[2])
else:
    iterations = 1000

if len(sys.argv) > 3:
    hitRequirement = int(sys.argv[3])
else:
    hitRequirement = 1
now = datetime.now()
outfilename = directory.split("/")[-2] + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute)

with open(outfilename+".csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(list(features.keys()))

    for filename in os.listdir(directory):
        if(count >= iterations):
            break
        with open(directory+filename) as file:
            archive = json.load(file)
            for review in archive["Reviews"]:
                content = review["Content"]
                rating = review["Overall"]
                if content and rating:
                    rating = float(rating)
                    usefulWords = [w for w in content.split() if not w in stopWords]

                    for feature in features:
                        if feature in usefulWords:
                            features[feature] = 1
                            featureCount[feature] += 1

                    if 1 <= rating and rating <= 2:
                        features["sentiment"] = "negative"
                    elif 4 <= rating and rating <= 5:
                        features["sentiment"] = "positive"
                    else:
                        features["sentiment"] = 0

                    if features["sentiment"] != 0:
                        writer.writerow(list(features.values()))

                    count += 1
                    for feature in features:
                        features[feature] = 0

featureNames = list(features.keys())
with open(outfilename+".csv", newline="") as infile, open(outfilename+"-cleaned.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    reader = csv.reader(infile)
    for row in reader:
        outlist = []
        names = featureNames.copy()
        while len(row) > 0:
            val = row.pop()
            if(featureCount[names.pop()] >= hitRequirement):
                outlist.append(val)

        writer.writerow(outlist)
