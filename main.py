from gtts import gTTS
import os
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'


cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "image.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        
        
        
        img = cv2.imread(img_name)

        # Adding custom options
        custom_config = r'--oem 3 --psm 4'
        output = pytesseract.image_to_string(img, config=custom_config)

        print(output)
        language = 'en'
        myobj = gTTS(text=output, lang=language, slow=False)
        myobj.save("output2.mp3")
        os.system("mpg123 output2.mp3")


cam.release()

cv2.destroyAllWindows()
