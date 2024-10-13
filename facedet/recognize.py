import cv2
import numpy as np
import os

# Define the size of images
size = 4

# Path to the Haar Cascade file for face detection
haar_file = 'haarcascade_frontalface_default.xml'

# Path to the datasets directory
datasets = "C:\\Users\\attar\\OneDrive\\Documents\\datasets"

print('Training...')

# Initialize lists for images, labels, and a dictionary for names
(images, labels, names, id) = ([], [], {}, 0)

# Load images and labels from the datasets directory
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1

# Convert the lists into numpy arrays
(images, labels) = [np.array(lst) for lst in [images, labels]]

# Create an LBPH face recognizer
model = cv2.face.LBPHFaceRecognizer_create()

# Train the model with the images and labels
model.train(images, labels)

# Initialize the face cascade
face_cascade = cv2.CascadeClassifier(haar_file)

# Open the webcam
cam = cv2.VideoCapture(0)
cnt = 0

while True:
    # Read the current frame from the webcam
    _, im = cam.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (130, 100))

        # Predict the identity of the face
        prediction = model.predict(face_resize)

        # If the prediction is confident (low distance value)
        if prediction[1] < 800:
            cv2.putText(im, '%s - %.0f' % (names[prediction[0]], prediction[1]), 
                        (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                        (255, 0, 0), 2, cv2.LINE_AA)
            print(names[prediction[0]])
            cnt = 0
        else:
            cnt += 1
            if cnt > 100:
                print("Unknown Person")
                cv2.imwrite("input.jpg", im)
                cnt = 0

    # Display the frame with annotations
    cv2.imshow('OpenCV', im)

    # Break the loop if the 'Esc' key is pressed
    key = cv2.waitKey(10)
    if key == 27:
        break

# Release the webcam and close windows
cam.release()
cv2.destroyAllWindows()
