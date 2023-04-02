from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

class DogClassifier:
    def __init__(self) -> None:
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model and labels
        self.model = load_model("model\keras_model.h5", compile=False)
        self.class_names = open("model\labels.txt", "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


    def classifier(self, image):            
        img = image.convert("RGB")

        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(img)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        self.data[0] = normalized_image_array

        # Predicts the model
        prediction = self.model.predict(self.data)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        return class_name[2:], confidence_score

    

