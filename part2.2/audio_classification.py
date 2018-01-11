import math
import numpy as np

r = 30  # Time Frames
c = 13  # Cepstrums
num = 5  # Size of data set: [1,2,3,4,5]


def readData(txt):
	images = []
	with open(txt, "r") as data:
		lines = data.readlines()
		count = 0
		image = []
		for line in lines:
			if (not line) or line == '\n':
				continue
			image.append(line)
			count += 1
			if count == 30:
				images.append(image)
				image = []
				count = 0
	return images


def readLabel(txt):
	all_data = []
	with open(txt, "r") as data:
		labels = data.readlines()
		for label in labels:
			all_data.append(int(label))
	return all_data


def process(data):
	processed = []
	for i in range(0, len(data)):
		recording = []
		for j in range(0, len(data[i])):
			temp = np.array(list(data[i][j]))
			new_line = []
			for k in range(0, len(temp)):
				if temp[k] == ' ':
					new_line.append(0)
				if temp[k] == '%':
					new_line.append(1)
			recording.append(new_line)
		processed.append(recording)
	return processed


def audio_classification():
	testing_data = readData('testing_data.txt')
	testing_labels = readLabel('testing_labels.txt')
	training_data = readData('training_data.txt')
	training_labels = readLabel('training_labels.txt')

	p_testing = process(testing_data)
	p_training = process(training_data)

	trained = training(p_training, training_labels)
	testing(trained, p_testing, testing_labels)


def training(data, label):
	prob = [[[0 for x in range(c)] for y in range(r)] for z in range(num)]

	for i in range(len(data)):
		for j in range(0, r):
			for k in range(0, c):
				prob[label[i] - 1][j][k] += data[i][j][k]

	# Laplace smoothing
	k = 0.1

	for o in range(0, num):
		for p in range(0, r):
			for q in range(0, c):
				prob[o][p][q] = (prob[o][p][q] + k) / (12 + k * num)

	return prob


def testing(prob_table, test_data, test_label):

	prior = [1.0 / num for x in range(num)]
	result = [[] for x in range(num)]
	correct = 0

	for i in range(len(test_data)):
		likelihood = [0 for x in range(num)]
		for j in range(r):
			for k in range(c):
				if test_data[i][j][k] == 1:

					for l in range(num):
						likelihood[l] += math.log(prob_table[l][j][k])
		for m in range(num):
			likelihood[m] = math.log(prior[m])+likelihood[m]
		predict = likelihood.index(max(likelihood))+1
		result[predict-1].append(test_label[i])

		if predict == test_label[i]:
			correct += 1
	'''
	for i in range(num):
		print(result[i])
	'''

	print "Overall accuracy is: ", correct/float(40)

	matrix = [[0 for x in range(num)] for x in range(num)]

	for x in range(num):
		all_num = 0
		for y in range(len(result)):
			for z in range(len(result[y])):
				if result[y][z] == x+1:
					all_num += 1
					matrix[x][y] += 1
		for zz in range(num):
			matrix[x][zz] = round(matrix[x][zz] / float(all_num) , 3)

	print("Confusion matrix is: ")
	for i in range(num):
		print(matrix[i])

	return


if __name__ == '__main__':
	audio_classification()
