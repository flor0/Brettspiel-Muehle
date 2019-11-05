import os
import matplotlib.pyplot as plt
import tensorflow as tf
import datahandler
import time


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
# Data stuff
batch_size = 30
_column_names = ['b00','b01','b02','b03','b04','b05','b06','b07','b10','b11','b12','b13','b14','b15','b16','b17','b20','b21','b22','b23','b24','b25','b26','b27','hand_me','hand_enemy','board_me','board_enemy','solution']
_label_name = 'solution'
print("Making dataset...")

train_dataset = tf.data.experimental.make_csv_dataset(
    'mydata.txt',
    batch_size,
    column_names=_column_names,
    label_name=_label_name,
    header=True,
    shuffle=True,
    num_epochs=1)
print("Dataset finished!")

train_dataset = train_dataset.map(pack_features_vector)

features, labels = next(iter(train_dataset))

print(features)
print(labels)

#######################################################################################################################
# Model stuff
model = tf.keras.Sequential([
  tf.keras.layers.Dense(100, activation=tf.nn.relu, input_shape=(1, 28)),  # input shape required
  tf.keras.layers.Dense(100, activation=tf.nn.relu),
  tf.keras.layers.Dense(100, activation=tf.nn.relu),
  tf.keras.layers.Dense(12719)
])

predictions = model(features)
tf.nn.softmax(predictions[:5])

print("Prediction: {}".format(tf.argmax(predictions, axis=1)))
print("    Labels: {}".format(labels))

loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)


loss_value, grads = grad(model, features, labels)
print("Step: {}, Initial Loss: {}".format(optimizer.iterations.numpy(),
                                          loss_value.numpy()))
optimizer.apply_gradients(zip(grads, model.trainable_variables))
print("Step: {},         Loss: {}".format(optimizer.iterations.numpy(),
                                          loss(model, features, labels).numpy()))

########################################################################################################################
# Training loop
print("####################### START TRAINING #######################")
train_loss_results = []
train_accuracy_results = []
num_epochs = 1500

#model.load_weights("weights.tf")


for epoch in range(num_epochs):
    t = time.time()
    epoch_loss_avg = tf.keras.metrics.Mean()
    epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

    # training loop
    for x, y in train_dataset:
        # Model optimization
        loss_value, gradients = grad(model, x, y)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        # track progress
        epoch_loss_avg(loss_value)  # Add current batch's loss
        epoch_accuracy(y, model(x)) # Compare prediction to actual label
    # End epoch
    train_loss_results.append(epoch_loss_avg.result())
    train_accuracy_results.append(epoch_accuracy.result())

    print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch, epoch_loss_avg.result(),
                                                                epoch_accuracy.result()))
    secs = (num_epochs - epoch) * (time.time() - t)
    mins = secs // 60
    hrs = mins / 60
    print("Estimated time remaining: {} hrs {} min {} sec".format(hrs, mins, secs))
    model.save_weights("weights.tf")


# visualize

fig, axes = plt.subplots(2, figsize=(12, 8))
fig.suptitle('Training Metrics')

axes[0].set_ylabel("Loss", fontsize=14)
axes[0].plot(train_loss_results)

axes[1].set_ylabel("Accuracy", fontsize=14)
axes[1].set_xlabel("Epoch", fontsize=14)
axes[1].plot(train_accuracy_results)
plt.show()

