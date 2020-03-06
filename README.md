# Yale Image Finder
![alt text](https://raw.githubusercontent.com/kevkid/YIF/master/YIF.png)
Redesign of the Yale Image finder using the Django framework.

The Yale Image Finder is a document retrieval system that allows the user to input a keyword and will return results associated with the keyword. This also includes finding documents that are nearest to the key word and documents that have similar images to any document that is currently being viewed. Currently deep learning has been integrated into YIF in order to classify images more accurately thus giving us a more precise set of results given a keyword. We are using Convolutional Neural Networks to accomplish this task. We are using the keras framework with the theano backend to perform all of the image classification tasks. The current deep learning model has been moved to: https://github.com/kevkid/Reducing_Burden
![alt text](https://github.com/kevkid/YIF/blob/master/Model%20Fusion%20DenseNet121%20Lite.jpg)
