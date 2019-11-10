import os
import matplotlib.pyplot as plt
import tensorflow as tf
import datahandler
import time

tf.debugging.set_log_device_placement(True)

def pack_features_vector(features, labels):
    """Pack the features into a single array."""
    features = tf.stack(list(features.values()), axis=1)
    return features, labels


def loss(model, x, y):
    y_ = model(x)
    return loss_object(y_true=y, y_pred=y_)


def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        _loss_value = loss(model, inputs, targets)
    return _loss_value, tape.gradient(_loss_value, model.trainable_variables)


print("TensorFlow version: {}".format(tf.__version__))
print("Eager execution: {}".format(tf.executing_eagerly()))

#######################################################################################################################
#######################################################################################################################
########################################################    FIRST NETWORK (TO)  #######################################
#######################################################################################################################
#######################################################################################################################
# Data stuff
batch_size = 64
_column_names = ['b00','b01','b02','b03','b04','b05','b06','b07','b10','b11','b12','b13','b14','b15','b16','b17','b20','b21','b22','b23','b24','b25','b26','b27','hand_me','hand_enemy','board_me','board_enemy','to']
_label_name = 'to'
print("Making dataset...")

train_dataset = tf.data.experimental.make_csv_dataset(
    'mydata_to.txt',
    batch_size,
    column_names=_column_names,
    label_name=_label_name,
    header=True,
    shuffle=True,
    num_epochs=1)

train_dataset = train_dataset.map(pack_features_vector)

#######################################################################################################################
# Model stuff
model = tf.keras.Sequential([
  tf.keras.layers.Dense(2000, activation=tf.nn.relu, input_shape=(1, 28)),  # input shape required
  tf.keras.layers.Dense(2000, activation=tf.nn.relu),
  tf.keras.layers.Dense(2000, activation=tf.nn.relu),
  tf.keras.layers.Dense(24)
])


loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

num_epochs = 10

#model.load_weights("weights_to.tf")
print("####################### START TRAINING #######################")

for epoch in range(num_epochs):
    t = time.time()
    epoch_loss_avg = tf.keras.metrics.Mean()
    epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

    for x, y in train_dataset:
        # Model optimization
        loss_value, gradients = grad(model, x, y)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        epoch_accuracy(y, model(x)) # Compare prediction to actual label

    print("Epoch {:03d}: Accuracy: {:.3%}".format(epoch, epoch_accuracy.result()))
    secs = (num_epochs - epoch) * (time.time() - t)
    mins = secs // 60
    hrs = mins / 60
    mins = mins - hrs*60
    secs = secs - mins*60 - hrs*60*60

    print("Completed epoch after: {} mins and {} secs".format(mins, secs))
    print("Estimated time remaining: {} hrs {} min {} sec".format(hrs, mins, secs))
    print("------------------------------------------------------")
    model.save_weights("weights_to.tf")
