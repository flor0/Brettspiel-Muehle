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


def makemove(board, hand_human, hand_ai, board_human, board_ai):
    # generate input vector for the neural network
    ai_input = []
    for i in range(3):
        for j in range(8):
            ai_input.append(board[i][j])  # Turn the board into something we can use
    ai_input.append(hand_ai)
    ai_input.append(hand_human)
    ai_input.append(board_ai)
    ai_input.append(board_human)
    ai_input = ai_input
    print("AI INPUT: ", ai_input)

    predictions = model(tf.convert_to_tensor(ai_input))

    try:
        for i, logits in enumerate(predictions):
            class_idx = tf.argmax(logits).numpy()
            p = tf.nn.softmax(logits)[class_idx]
            output_move = datahandler.get_position(class_idx)
            print("Move Position: {}".format(output_move))
            return output_move
    except:
        with i as predictions[0]:
            with logits as predictions[1]:
                class_idx = tf.argmax(logits).numpy()
                p = tf.nn.softmax(logits)[class_idx]
                output_move = datahandler.get_position(class_idx)
                print("Move Position: {}".format(output_move))
                return output_move




print("TensorFlow version: {}".format(tf.__version__))
print("Eager execution: {}".format(tf.executing_eagerly()))

#######################################################################################################################
# Model stuff
model = tf.keras.Sequential([
  tf.keras.layers.Dense(5000, activation=tf.nn.relu, input_shape=(1, 28)),  # input shape required
  tf.keras.layers.Dense(5000, activation=tf.nn.relu),
  tf.keras.layers.Dense(5000, activation=tf.nn.relu),
  tf.keras.layers.Dense(12719)
])
model.load_weights("weights.tf")

print("####################### NEURAL NETWORK INITIALIZED #######################")




