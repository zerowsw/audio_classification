import math
import os


def readImages(dirPath):
    images = []
    fileList = os.listdir(os.getcwd() + os.sep + dirPath)
    for f in fileList:
        f = dirPath + '/' + f
        with open(f, "r") as f:
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

def readTraingImages(dirPath, no_train, yes_train):
        fileList = os.listdir(os.getcwd() + os.sep + dirPath)
        for f in fileList:
            type = []
            for i in range(0, 15, 2):
                type.append(f[i])
            print f
            f = dirPath+'/'+f

            with open(f, "r") as filepath:
                lines = filepath.readlines()
                images = []
                # for i in range(8):
                #     images.append([])
                for line in lines:
                    if (not line) or line == '\n':
                        continue
                    # for i in range(8):
                    #     str = line[i * 10 : i * 10 + 10]
                       # str = str + '\n'
                    images.append(line)

                index = []
                i = 0
                while i < len(images[0]):
                    count = 0
                    for j in range(25):
                        if images[j][i] == ' ':
                            count += 1
                    if count >= 3:
                        index.append(i)
                        i = i + 10
                    else:
                        i = i + 1

                for i in range(8):
                    tempImage = []
                    for j in range(25):
                        tempImage.append(images[j][index[i] : index[i] + 10])
                    if type[i] == '0':
                        no_train.append(tempImage)
                    else :
                        yes_train.append(tempImage)


def audio_classification():
    no_train = []
    yes_train = []
    readTraingImages('txt_yesno/training', no_train, yes_train)

    no_test = readImages('txt_yesno/no_test')
    yes_test = readImages('txt_yesno/yes_test')

    #smooth factor
    smooth_factor = 0.6

    yes_prior =  (float)(len(yes_train)) / (len(no_train) + len(yes_train))
    no_prior = 1 - yes_prior

    likelyhood_yes_low = [[0 for i in range(10)] for i in range(25)]
    likelyhood_yes_high = [[0 for i in range(10)] for i in range(25)]
    likelyhood_no_low = [[0 for i in range(10)] for i in range(25)]
    likelyhood_no_high = [[0 for i in range(10)] for i in range(25)]

    #after training likelyhood_yes_low, we can easily get likelyhood_yes_high
    train(likelyhood_no_low, likelyhood_no_high, no_train, smooth_factor)
    train(likelyhood_yes_low, likelyhood_yes_high, yes_train, smooth_factor)

    #test

    total_test_count = len(no_test) + len(yes_test)

    #classification for no_test dataset
    no_success = test(likelyhood_no_high, likelyhood_no_low, likelyhood_yes_high, likelyhood_yes_low, no_prior, no_test, yes_prior, 1)
    yes_success = test(likelyhood_no_high, likelyhood_no_low, likelyhood_yes_high, likelyhood_yes_low, no_prior, yes_test, yes_prior, 0)

    print  "no_test: ", len(no_test), " yes_test: ", len(yes_test)
    print "no_success: ", no_success, " yes_success: ", yes_success
    correct_rate = (float)(no_success + yes_success) / total_test_count
    print "total correst rate :", correct_rate

def test(likelyhood_no_high, likelyhood_no_low, likelyhood_yes_high, likelyhood_yes_low, no_prior, dataset,
          yes_prior, flag):
    successful_count = 0;
    for i in range(len(dataset)):
        no_posterior = math.log(no_prior)
        yes_posterior = math.log(yes_prior)
        no_posterior_factor = 0
        yes_posterior_factor = 0

        for x in range(25):
            for y in range(10):
                if dataset[i][x][y] == '%':
                    no_posterior_factor = likelyhood_no_low[x][y]
                    yes_posterior_factor = likelyhood_yes_low[x][y]
                else:
                    no_posterior_factor = likelyhood_no_high[x][y]
                    yes_posterior_factor = likelyhood_yes_high[x][y]
                no_posterior += math.log(no_posterior_factor)
                yes_posterior += math.log(yes_posterior_factor)
        if flag == 1:
            if no_posterior > yes_posterior:
               successful_count += 1
        else:
            if yes_posterior > no_posterior:
                successful_count += 1
    return successful_count


def train(likelyhood_low, likelyhood_high, dataset, smooth_factor):
    size = len(dataset)
    for i in range(len(dataset)):
        for x in range(25):
            for y in range(10):
                if dataset[i][x][y] == '%':
                    likelyhood_low[x][y] += 1
                else :
                    likelyhood_high[x][y] += 1
    #laplacian smoothing
    denominator = size + smooth_factor * 2
    for i in range(25):
        for j in range(10):
            likelyhood_low[i][j] = (likelyhood_low[i][j] + smooth_factor) / denominator
            likelyhood_high[i][j] = (likelyhood_high[i][j] + smooth_factor) / denominator

if __name__ == '__main__':
    #audio_classification()
    audio_classification()



