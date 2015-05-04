library(class)
library(e1071)
args <- commandArgs(trailingOnly = TRUE)
features = read.csv(args[1])

nb_model <- naiveBayes(features[,colnames(features)!="sentiment"], features[,colnames(features)=="sentiment"])
nb_result <- predict(nb_model, features[,colnames(features)!="sentiment"])
table(nb_result, features[,colnames(features)=="sentiment"])

svm_model <- svm(features[,colnames(features)!="sentiment"], features[,colnames(features)=="sentiment"])
svm_result <- predict(svm_model, features[,colnames(features)!="sentiment"])
table(svm_result, features[,colnames(features)=="sentiment"])
