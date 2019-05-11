# -*- coding: utf-8 -*-
"""second_question.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13doPx4dAhkeRRUpxdfH_CvO2AkWa_WTI
"""

from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf
import os,cv2
import numpy as np
from sklearn.model_selection import train_test_split
train=[]
train_labels=[]
for path, dirs, files in os.walk("drive/My Drive/HumanActionClassification"):
  for name in dirs:
    l=[0,0,0,0,0,0,0]
    l[int(name)-1]=1
    for x,y,z in os.walk("drive/My Drive/HumanActionClassification/"+name):
      for file in z:
        image=cv2.resize(cv2.imread("drive/My Drive/HumanActionClassification/"+name+'/'+file),dsize=(224,224),interpolation=cv2.INTER_CUBIC)
        train.append(image)
        train_labels.append(l)
train=np.array(train)
train_labels=np.array(train_labels)
X_train, X_test, y_train, y_test = train_test_split(train, train_labels, test_size=0.25)

learning_rate = 0.0001
epochs = 12
batch_size = 30

x = tf.placeholder(tf.float32, [None, 224,224,3])                            #   training data placeholders
y = tf.placeholder(tf.float32, [None, 7])

    #///////////////////////////////////////////        layer1            ////////////////////////////////////////////////
conv_filt_shape1 = [5, 5, 3, 32]                                             #   num_filters, input_data,  num_input_channels

weights1 = tf.Variable(tf.truncated_normal(conv_filt_shape1, stddev=0.03), name='layer1'+'_W')
bias1 = tf.Variable(tf.truncated_normal([32]), name='layer1'+'_b')
out_layer1 = tf.nn.conv2d(x, weights1, [1, 1, 1, 1], padding='SAME')
out_layer1 += bias1 
out_layer1 = tf.nn.relu(out_layer1)                                        # ReLU activation  
ksize1 = [1, 3, 3, 1]                                                      # filter_shape, pool_shape for max pool
out_layer1 = tf.nn.max_pool(out_layer1, ksize=ksize1, strides=[1,2,2,1], padding='SAME')
   
    #///////////////////////////////////////////         layer2         ////////////////////////////////////////////////
    
conv_filt_shape2 = [5, 5, 32, 64]
weights2 = tf.Variable(tf.truncated_normal(conv_filt_shape2, stddev=0.03), name='layer2'+'_W')
bias2 = tf.Variable(tf.truncated_normal([64]), name='layer2'+'_b')
out_layer2 = tf.nn.conv2d(out_layer1, weights2, [1, 1, 1, 1], padding='SAME')
out_layer2 += bias2
out_layer2 = tf.nn.relu(out_layer2)                                   # ReLU activation
ksize2 = [1, 3, 3, 1]
out_layer2 = tf.nn.max_pool(out_layer2, ksize=ksize2, strides=[1,2,2,1], padding='SAME')
    
    #///////////////////////////////////////////          layer3        ////////////////////////////////////////////////
    
conv_filt_shape3 = [9, 9, 64, 128]
weights3 = tf.Variable(tf.truncated_normal(conv_filt_shape3, stddev=0.03), name='layer3'+'_W')
bias3 = tf.Variable(tf.truncated_normal([128]), name='layer3'+'_b')
out_layer3 = tf.nn.conv2d(out_layer2, weights3, [1, 1, 1, 1], padding='SAME')
out_layer3 += bias3 
out_layer3 = tf.nn.relu(out_layer3)                                 # ReLU activation
ksize3 = [1, 9, 9, 1]  
out_layer3 = tf.nn.max_pool(out_layer3, ksize=ksize3, strides=[1,8,8,1], padding='SAME')
    
flat_output = tf.reshape(out_layer3, [-1, 7 * 7 * 128])             # Flatten the output

wd = tf.Variable(tf.truncated_normal([7*7*128, 7], stddev=0.03), name='wd')
bd = tf.Variable(tf.truncated_normal([7], stddev=0.01), name='bd')
dense_layer = tf.matmul(flat_output, wd) + bd
y_ = tf.nn.softmax(dense_layer)                                  #  softmax layer

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=dense_layer, labels=y))

optimiser = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

initialize_operator = tf.global_variables_initializer()
  
with tf.Session() as sess:
  sess.run(initialize_operator)
  total_batch = int( X_train.shape[0]/ batch_size)                    
  for epoch in range(epochs):
    avg_cost = 0
    for i in range(total_batch):
      batch_x = X_train[i*batch_size:(i+1)*batch_size]
      batch_y = y_train[i*batch_size:(i+1)*batch_size]

      _, c = sess.run([optimiser, cross_entropy], feed_dict={x: batch_x, y: batch_y})
      avg_cost += c / total_batch
    test_acc = sess.run(accuracy, feed_dict={x: X_test, y: y_test})
    print("Epoch number:", (epoch + 1)," test accuracy: {:.3f}".format(test_acc))
  print("\nTraining complete!\n Accuracy :",)
  print(sess.run(accuracy, feed_dict={x: X_test, y: y_test}))

