import math
import os

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

    #smooth factor
    smooth_factor = 0.1

    yes_prior =  (float)(len(yes_train)) / (len(no_train) + len(yes_train))
    no_prior = 1 - yes_prior

    likelyhood_yes = [[0 for i in range(11)] for i in range(25)]
    likelyhood_no = [[0 for i in range(11)] for i in range(25)]

    #after training likelyhood_yes_low, we can easily get likelyhood_yes_high
    train(likelyhood_yes, yes_train, smooth_factor)
    train(likelyhood_no, no_train, smooth_factor)

    #test

    total_test_count = len(no_test) + len(yes_test)

    #classification for no_test dataset
    no_success = test(likelyhood_no, likelyhood_yes, no_prior, no_test, yes_prior, 1)
    yes_success = test(likelyhood_no, likelyhood_yes, no_prior, yes_test, yes_prior, 0)

    print  "no_test: ", len(no_test), " yes_test: ", len(yes_test)
    print "no_success: ", no_success, " yes_success: ", yes_success
    correct_rate = (float)(no_success + yes_success) / total_test_count
    print "total correst rate :", correct_rate

def test(likelyhood_no, likelyhood_yes, no_prior, dataset, yes_prior, flag):
    successful_count = 0;
    for i in range(len(dataset)):
        no_posterior = math.log(no_prior)
        yes_posterior = math.log(yes_prior)
        no_posterior_factor = 0
        yes_posterior_factor = 0

        for x in range(25):
            count = 0
            for y in range(10):
                if dataset[i][x][y] == '%':
                    count += 1
            no_posterior += math.log(likelyhood_no[x][count])
            yes_posterior += math.log(likelyhood_yes[x][count])
        if flag == 1:
            if no_posterior > yes_posterior:
               successful_count += 1
        else:
            if yes_posterior > no_posterior:
                successful_count += 1
    return successful_count


def train(likelyhood, dataset, smooth_factor):
    size = len(dataset)
    for i in range(len(dataset)):
        for x in range(25):
            count = 0
            for y in range(10):
                if dataset[i][x][y] == '%':
                    count += 1
            likelyhood[x][count] += 1

    #laplacian smoothing
    denominator = size + smooth_factor * 11
    for i in range(25):
        for j in range(11):
            likelyhood[i][j] = (likelyhood[i][j] + smooth_factor) / denominator


if __name__ == '__main__':
    audio_classification()

