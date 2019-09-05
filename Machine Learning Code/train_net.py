'''
24662 Gesture
training of NN
'''

import tensorflow as tf
import numpy as np
import numpy.matlib as mat
import matplotlib.pyplot as plt


# ------------ define hyperparameters ------------
nodes1 = 100
nodes2 = 100
nodes3 = 100
nodes4 = 100

input_dim = 30
output_dim= 11
num_people = 12
# Name: stop, keep forward, keep backward, keep left, keep rigth, forward and left45, forward and right45, pointing
# Lable:  0          1             2            3           4              5                   6              7
# Name: pointup ccw,  pointdown cw, kick
# Lable:    8               9        10

# misrecognize: 7 -> 10; 7 -> 9; 8 -> 0

lr=0.0001
epochs=50
batch_size=32



# ------------ functions ------------
def extract_data():
    path = "./gestureRecogniton/data_collection/static_data/"
    datalist = []
    for i in range(output_dim):
        for j in range(num_people):
            filepath = path + "data_" + str(i) + "_" + str(j) + ".txt"
            file = open(filepath)
            data = file.readlines()

            for line in data:
                splitdata = line.split(" ")
                temp = [float(instance_pure) for instance_pure in splitdata[:-1]]
                datalist.append(temp)

    return datalist


def preprocess_data(datalist):
    num_data = len(datalist)
    print(num_data)
    trainnum = int(num_data * 0.8)

    datalist_ = np.matrix(datalist)
    print(datalist_.shape)
    np.random.shuffle(datalist_)

    training_data = datalist_[0:trainnum, :-1]
    training_data_label = datalist_[0:trainnum, -1]

    validation_data = datalist_[trainnum:num_data, :-1]
    validation_data_label = datalist_[trainnum:num_data, -1]

    training_data_labeloh = np.zeros((len(training_data_label), output_dim))
    for i in range(len(training_data_label)):
        training_data_labeloh[i, int(training_data_label[i, 0])] = 1

    validation_data_labeloh = np.zeros((len(validation_data_label), output_dim))
    for i in range(len(validation_data_label)):
        validation_data_labeloh[i, int(validation_data_label[i, 0])] = 1

    print(training_data.shape)
    print(training_data_labeloh.shape)
    print(validation_data.shape)
    print(validation_data_labeloh)

    # training data
    substract = mat.repmat(training_data[:,0:3],1,int(training_data.shape[1]/3))
    training_data = training_data - substract
    training_data_label = training_data_label.astype(int)
    print(training_data.shape)

    # validation data
    substract = mat.repmat(validation_data[:,0:3],1,int(validation_data.shape[1]/3))
    validation_data = validation_data - substract
    validation_data_label = validation_data_label.astype(int)

    return training_data, training_data_labeloh, validation_data, validation_data_labeloh

def plot_figure(x, y, xlabel, ylabel):
        plt.figure()
        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()



#------------------- extract data -------------------
datalist = extract_data()
training_data, training_data_label, validation_data, validation_data_label = preprocess_data(datalist)



#------------------- build neural network -------------------
with tf.variable_scope('nn'):
    inputdata = tf.placeholder(tf.float32, [None, input_dim], name = 'input')
    groundtruth = tf.placeholder(tf.int64, [None, output_dim], name = 'groundtruth')

    layer1 = tf.layers.dense(inputdata, nodes1, 
                            kernel_initializer = tf.truncated_normal_initializer(stddev=0.1), 
                            activation = tf.nn.relu,
                            name = 'layer1')
    layer2 = tf.layers.dense(layer1, nodes2, 
                            kernel_initializer = tf.truncated_normal_initializer(stddev=0.1), 
                            activation = tf.nn.relu,
                            name = 'layer2')
    layer3 = tf.layers.dense(layer2, nodes3, 
                            kernel_initializer = tf.truncated_normal_initializer(stddev=0.1), 
                            activation = tf.nn.relu,
                            name = 'layer3')
    layer4 = tf.layers.dense(layer3, nodes4, 
                            kernel_initializer = tf.truncated_normal_initializer(stddev=0.1), 
                            activation = tf.nn.relu,
                            name = 'layer4')
    output = tf.layers.dense(layer4, output_dim, 
                            kernel_initializer = tf.truncated_normal_initializer(stddev=0.1),
                            name = 'output')
    pred = tf.argmax(tf.nn.softmax(output), axis = 1, name = 'prediction')

with tf.name_scope("loss"):
    loss_softmax = tf.nn.softmax_cross_entropy_with_logits(labels = groundtruth, logits = output, name = 'loss_softmax')
    loss = tf.reduce_mean(loss_softmax , name='loss')

with tf.name_scope("train"):
    optimizer = tf.train.AdamOptimizer(lr)
    train_op=optimizer.minimize(loss)

# the accuracy computation
with tf.variable_scope('accuracy'):
    correct_mask = tf.equal(tf.argmax(tf.nn.softmax(output), axis = 1), tf.argmax(groundtruth, axis = 1))
    accuracy = tf.reduce_mean(tf.cast(correct_mask, tf.float32), name = 'acc')


sess = tf.Session()
sess.run(tf.global_variables_initializer())

steps = training_data.shape[0] // batch_size + 1 # calculate the steps in each epochs
print(steps)
losses = np.zeros(epochs * steps)
counter = 0

for i in range(epochs):
    # feed all the minibatch
    for j in range(steps):
        # obtain the data and label of the minibatch
        if j == (steps - 1):
            minibatch_data = training_data[(batch_size * j):-1, :]
            minibatch_label = training_data_label[(batch_size * j):-1, :]
        else:
            minibatch_data = training_data[(batch_size * j):(batch_size * (j+1)), :]
            minibatch_label = training_data_label[(batch_size * j):(batch_size * (j+1)), :]


        # train the model
        _, lossvalue = sess.run([train_op, loss], 
                                feed_dict = {inputdata: minibatch_data, groundtruth: minibatch_label})
        # record the loss
        print(lossvalue)
        losses[counter] = lossvalue
        counter += 1


plot_figure(range(len(losses)), losses, 'iterations', 'loss')

accuracy_training = sess.run(accuracy, 
                                feed_dict = {inputdata: training_data, groundtruth: training_data_label})

accuracy_validation = sess.run(accuracy, 
                                feed_dict = {inputdata: validation_data, groundtruth: validation_data_label})

print('Trainning accuracy:', accuracy_training*100, '%')
print('Validation accuracy', accuracy_validation*100, '%')


#save the model
saver=tf.train.Saver()
saver.save(sess,"./model/564/model.ckpt") ### save model