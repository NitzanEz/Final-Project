import os
import tensorflow as tf
from tensorflow.keras.layers import Dense, MaxPooling2D, Flatten, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

from inception_v4 import create_model  # Make sure this script is correctly formatted and located

# Directory setup
train_dir = 'C:/Users/liorb/git/Final-Project/Data/train'
validation_dir = 'C:/Users/liorb/git/Final-Project/Data/validation'
test_dir = 'C:/Users/liorb/git/Final-Project/Data/test'

# Model parameters
img_width, img_height = 299, 299
batch_size = 32
epochs = 50

# Load the pre-trained Inception V4 model without the top layer (for transfer learning)
model = create_model(num_classes=1, dropout_prob=0.2, weights='imagenet', include_top=False)

# Adding custom Layers
x = model.output
# Apply MaxPooling2D as global max pooling (pool_size should be adjusted based on the actual output size of the last conv layer)
x = MaxPooling2D(pool_size=(8, 8))(x)
x = Flatten()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)
model = Model(inputs=model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

# Use image_dataset_from_directory to load images
train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(img_width, img_height),
    batch_size=batch_size,
    label_mode='binary')

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    validation_dir,
    image_size=(img_width, img_height),
    batch_size=batch_size,
    label_mode='binary')


# Train the model
model.fit(
    train_dataset,
    epochs=epochs,
    validation_data=validation_dataset
)

# Evaluate the model on the validation set
val_loss, val_acc = model.evaluate(validation_dataset)
print(f'Validation Loss: {val_loss}, Validation Accuracy: {val_acc}')
