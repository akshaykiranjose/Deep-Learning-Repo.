import tensorflow as tf
import os
import csv
from tensorflow.keras.preprocessing.image import ImageDataGenerator

emotions = {0:'angry',
            1:'disgust',
            2:'fear',
            3:'happy',
            4:'neutral',
            5:'sad',
            6:'surprise'}

path = os.getcwd();

datagen = ImageDataGenerator(rescale=1/255.)

pred_generator = datagen.flow_from_directory(path,
                              classes=['EMOTOR_TEST'],
                              class_mode=None,
                              shuffle=False,
                              target_size=(64, 64))
                            
model = tf.keras.models.load_model('fer2013.h5')
preds = model.predict(pred_generator)
preds = tf.argmax(preds, axis=1).numpy()

images = os.listdir(os.path.join(path, 'EMOTOR_TEST'))
pred_dict = [{'img_name':img, 'label':emotions[pred]} for img, pred in zip(images, preds)]

if __name__ == "__main__":
    with open('predictions.csv', 'w', newline='') as f:
        fieldnames=['img_name', 'label']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pred_dict)
