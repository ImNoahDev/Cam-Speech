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
         
        
        try:
            img = cv2.imread(img_name)

            # Adding custom options
            custom_config = r'--oem 3 --psm 4'
            output = pytesseract.image_to_string(img, config=custom_config)

            print(output)
            language = 'en'
            myobj = gTTS(text=output, lang=language, slow=False)
            myobj.save("output.mp3")
            os.system("mpg123 output.mp3")
        except:
            print("failiure")
            
    elif k%256 == 118:
        # v pressed
        img_name = "image2.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        
        output_label = ""
        """Detects labels in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient()
    
        with io.open("image2.png", 'rb') as image_file:
            content = image_file.read()
    
        image = vision.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels:')

        for label in labels:
            if "description" in label:
                output_label += str(label).split('"')[-2]+", "

        if response.error.message:
                print('{}\nFor more info on error messages, check: ')
                print("https://cloud.google.com/apis/design/errors")
                    
        try:
            print(output_label)
            language = 'en'
            myobj = gTTS(text=output_label, lang=language, slow=False)
            myobj.save("output2.mp3")
            os.system("mpg123 output2.mp3")
        except:
            print("failiure on Label")
                    

cam.release()

cv2.destroyAllWindows()
