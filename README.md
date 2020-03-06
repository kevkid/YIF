# Yale Image Finder
![alt text](https://raw.githubusercontent.com/kevkid/YIF/master/YIF.png)
Redesign of the Yale Image finder using the Django framework.

The Yale Image Finder is a document retrieval system that allows the user to input a keyword and will return results associated with the keyword. This also includes finding documents that are nearest to the key word and documents that have similar images to any document that is currently being viewed. Currently deep learning has been integrated into YIF in order to classify images more accurately thus giving us a more precise set of results given a keyword. We are using Convolutional Neural Networks to accomplish this task. We are using the keras framework with the theano backend to perform all of the image classification tasks. We have updated the model to classify based on images and text and can be found: https://github.com/kevkid/Reducing_Burden
![alt text](https://raw.githubusercontent.com/kevkid/YIF/master/Screenshot%20from%202020-03-06%2015-11-44.png)
### Confusion Matrix:
|           | bar | gel | histology | line | molecular | network | plot | sequence |
|-----------|-----|-----|-----------|------|-----------|---------|------|----------|
| bar       | 23  | 2   | 0         | 0    | 0         | 0       | 0    | 1        |
| gel       | 0   | 23  | 0         | 0    | 0         | 1       | 1    | 3        |
| histology | 0   | 0   | 23        | 0    | 4         | 1       | 0    | 3        |
| line      | 1   | 0   | 0         | 23   | 2         | 4       | 4    | 0        |
| molecular | 1   | 0   | 2         | 0    | 17        | 1       | 0    | 0        |
| network   | 1   | 0   | 0         | 1    | 2         | 15      | 0    | 0        |
| plot      | 0   | 0   | 0         | 2    | 0         | 0       | 21   | 0        |
| sequence  | 0   | 1   | 1         | 0    | 1         | 4       | 0    | 19       |
