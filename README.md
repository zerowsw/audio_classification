# audio_classification
Apply Naive Bayes classifiers to solve basic binary classification problems in the area of audio signal processing.<br> 
In this problem, the feature we used to classify spectrograms are 250 binary variables W(1,1), ... , W(25, 10), <br>
and W(i, j) = 1, if the ij-th block of the spectrogram has high energy and and 0 otherwise. Each binary variable <br>
is conditionally independent of the others given audio class. According to the model description provided by the <br>
problem, we estimate the likelihoods P(W(i, j) = 1 | class) as the proportion of the training data from that class <br>
that has high energy at the corresponding block. And it is the same when we estimate the likelihoods 
P(W(i, j) = 0 | class). Besides we use the laplace smoothing to avoid calculation problems when low or high energy <br>
appears zero time. We also  compute the log-likelihood to avoid underflow.
In training procedure, we first read binary text images from yes_train.txt and no_train.txt and store them into arrays. <br>
Then, we compute the P(W(i, j) = 1 | class) through dividing the number of high energy in position ij of the binary <br>
image plus the smoothing_factor by the total number of images plus the smoothing_factor * 2.  Here, the smoothing_factor<br> 
is the Laplace smoothing constant. After several experiments, we set the smoothing_factor to be 0.1. After the training <br>
procedure, we get all the model parameters stored in four two-dimensional arrays: likelyhood_yes_low, likelyhood_yes_high,<br>
likelyhood_no_low, likelyhood_no_high. <br>
In test procedure, we first read all the test data from yes_train.txt and no_test.txt. Then we use MAP classification, <br>
that’s to say, we assign the images to the class with the highest posterior. <br>
The formula we used here is:<br>
![image](https://github.com/zerowsw/audio_classification/blob/master/formula2.png) <br>


