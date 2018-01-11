import math
import os
from numpy import *

def readImages(filename):
    images = []
    with open(os.getcwd() + os.sep + filename, "r") as f:
        finish = False
        lines = f.readlines()
        count = 0
        image = []
        for line in lines:
            if (not line) or line == '\n':
                continue
            image.append(line)
            count += 1
            if count == 25:
                images.append(image)
                image = []
                count = 0
    return images

def audio_classification():
    no_train = readImages('no_train.txt')
    yes_train = readImages('yes_train.txt')
    no_test = readImages('no_test.txt')
    yes_test = readImages('yes_test.txt')


    yes_prior =  (float)(len(yes_train)) / (len(no_train) + len(yes_train))
    no_prior = 1 - yes_prior

    new_yes_train = []
    new_no_train = []
    new_yes_test = []
    new_no_test = []

    refactor(yes_train, new_yes_train)
    refactor(no_train, new_no_train)
    refactor(yes_test, new_yes_test)
    refactor(no_test, new_no_test)

    #calcualte the average vectors
    yes_train_mui = [0 for i in range(25)]
    no_train_mui = [0 for i in range(25)]
    mui(new_yes_train, yes_train_mui)
    mui(new_no_train, no_train_mui)

    #calculate the covariance matrix for class yes
    yes_train_mat = mat(new_yes_train)
    yes_train_conv = cov(yes_train_mat.T)

    #calculate the covariance matrix for class no
    no_train_mat = mat(new_no_train)
    no_train_conv = cov(no_train_mat.T)


    yes_train_size = len(new_yes_train)
    no_train_size = len(new_no_train)
    conv = mat((yes_train_size * yes_train_conv + no_train_size * no_train_conv) / (no_train_size + yes_train_size))

    #calculate the linear coefficients
    beta = dot(conv.I, (mat(yes_train_mui) - mat(no_train_mui)).T)

    #test
    no_success = test(yes_train_mui, no_train_mui, beta, no_prior, yes_prior, new_no_test, 1)
    yes_success = test(yes_train_mui, no_train_mui, beta, no_prior, yes_prior, new_yes_test, 0)

    # print  "no_test: ", len(no_test), " yes_test: ", len(yes_test)
    print "no_success: ", no_success, " yes_success: ", yes_success
    correct_rate = (float)(no_success + yes_success) / 100
    print "total correst rate :", correct_rate

def test( yes_train_mui, no_train_mui, beta, no_prior, yes_prior, dataset, flag):

    success = 0
    for i in range(len(dataset)):
        testsample = mat(dataset[i])
        new_mui = (mat(yes_train_mui) + mat(no_train_mui)) / 2
        value = dot(beta.T, (testsample - new_mui).T)
        if flag == 1:
            if value < math.log(yes_prior / no_prior):
                success += 1
        else:
            if value > math.log(yes_prior / no_prior):
                success += 1
    return success


def mui(dataset, mui):
    size = len(dataset)
    for i in range(len(dataset)):
        for x in range(25):
            mui[x] += dataset[i][x]
    for i in range(25):
        mui[i] = (float)(mui[i] / size)

def refactor(dataset, new_dataset):
    size = len(dataset)
    for i in range(len(dataset)):
        feature = []
        for x in range(25):
            count = 0
            for y in range(10):
                if dataset[i][x][y] == '%':
                    count += 1
            feature.append(count/10.0)
        new_dataset.append(feature)


if __name__ == '__main__':
    audio_classification()

