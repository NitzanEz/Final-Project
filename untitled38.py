import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import sys

import sys
sys.path.append('/content/Final-Project')
#sys.path.append('/content/Final-Project/athena.exp')
sys.path.append('/content/Final-Project/athena.exp')


from imagenet_inceptionv4 import inception_v4, train_inception_v4

# הגדרת נתיבים
train_dir = 'C:/Users/liorb/git/Final-Project/Data/train'
validation_dir = 'C:/Users/liorb/git/Final-Project/Data/validation'
test_dir = 'C:/Users/liorb/git/Final-Project/Data/test'

# פרמטרים של התמונות
IMG_HEIGHT = 299
IMG_WIDTH = 299
BATCH_SIZE = 32

# פונקציה לטעינת הנתונים
def load_asd_data(train_dir, validation_dir, test_dir, img_height=299, img_width=299, batch_size=32):
    train_datagen = ImageDataGenerator(

    )

    val_datagen = ImageDataGenerator(rescale=1.0/255)
    test_datagen = ImageDataGenerator(rescale=1.0/255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary'
    )

    validation_generator = val_datagen.flow_from_directory(
        validation_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary'
    )

    return train_generator, validation_generator, test_generator

# פונקציה להצגת גרף ביצועים
def plot_training_history(train_loss, val_loss):
    plt.figure(figsize=(12, 6))
    plt.plot(train_loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend()
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.show()

# הקוד הראשי
if __name__ == "__main__":
    # טעינת הנתונים
    train_gen, val_gen, test_gen = load_asd_data(train_dir, validation_dir, test_dir)

    # אימון המודל
    train_loss, val_loss = train_inception_v4(train_gen, val_gen, epochs=10)

    # גרף ביצועים
    plot_training_history(train_loss, val_loss)
