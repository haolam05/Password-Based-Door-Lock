import cv2
import numpy as np
import os
import LCD as LCD


# For using face recognition:
# First, you need to run gather_data.py to gather the face data.
# Then, you need to run train_model.py to train the model.
# Then, you can run main.py to activate the face recognition.
def greet_if_saw_members():

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # iniciate id counter
    id = 0

    # names related to ids: None = 0;
    names = ['None', 'Quan', 'Gang']

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    is_recognized = False
    loop = True

    while (loop):
        ret, img = cam.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
            )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            print(id)

            # Check if confidence is less than 40 ==> "0" is perfect match
            if (confidence < 40):
                name = str(names[id])
                print("Name: ", name)
                LCD.print_custom_msg("Hi " + name + "!")
                print("confidence", confidence)
                is_recognized = True
                loop = False
                break

            else:
                name = "unknown"
                print("unknown, confidence", confidence)
                LCD.print_custom_msg("You can't enter")
                continue

            is_recognized = False
            LCD.print_custom_msg("calling 911 !")

            cv2.putText(img, name, (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(1000) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    return is_recognized
