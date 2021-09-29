# Classification Of Persian Tweets Using Neural Networks

This project was done as a part of my B.Sc. Thesis under supervision of Dr. Mehdi Rahmati, Computer Engineering Department, Tehran Polytechnic. The aim was to implement a LSTM and CNN neural netwoks to classify short Persian tweets to determine tweet's subject. I've done the project as follow:

# Step 1

The first step was to collect data from twitter. As we used supervised algorithms so we need labeled data. therefore we used hashtags to get tweets from twitter api and, then we labeled tweets considering the hashtags and, we removed hashtags from tweets content. 15315 tweets were retrieved.

# Step 2

The second step was the most important step, data preprocessing! Stages such as removing unrelated contents, normalization, tokenization, lemmatization, stemming, removing stop words and making a dictionary was done in this step.

# Step 3

Tensorflow library is used to train an LSTM and a CNN model. Then model's accuracy and confusion matrix was claculated to evaluate the model. CNN reached 80.05 percent accuracy and, LSTM reached 94.81.
Hyperparameters were obtained as follow:

LSTM:
1. input sequence length = 40
2. output sequence length = 45
3. learning rate=0.0001
4. epochs = 20
5. batch size = 16
![Untitled1](https://user-images.githubusercontent.com/25254019/135328836-477ee62f-26f9-43ae-b4e5-f8d5d8d98340.png)

CNN:
1. input sequence length = 40
2. CNN window size = 3
3. CNN layer1 neuron = 64
4. CNN layer2 neuron = 128
5.  CNN layer3 neuron = 256
6. learning rate=0.0007
7. epochs = 30
8. batch size = 64
![Untitled2](https://user-images.githubusercontent.com/25254019/135332384-deb81d2a-f920-44cc-a57b-a3dff7f1e990.png)

 
# Step 4

IN the fourh step an user interface was designed using django framework.
