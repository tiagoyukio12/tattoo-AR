import cv2
import imutils
import numpy as np


class TemplateDetector:
    def __init__(self, template_filename, tattoo_filename):
        template1 = cv2.imread(template_filename)
        template1 = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
        template1 = cv2.Canny(template1, 50, 200)
        self.template = imutils.resize(template1, width=60)
        (self.tH, self.tW) = self.template.shape[:2]

        self.tattoo = cv2.imread(tattoo_filename)
        self.tattoo = imutils.resize(self.tattoo, width=60)

        self.found = None
        self.x_offset = 0
        self.y_offset = 0

    def detect_template(self, frame):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found = None

        # Loop over the scales of the image
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # Resize the image according to the scale
            resized = cv2.resize(gray, None, fx=scale, fy=scale)
            r = gray.shape[1] / float(resized.shape[1])

            if resized.shape[0] < self.tH or resized.shape[1] < self.tW:
                print("frame is smaller than the template")
                break

            # Detect edges in the resized grayscale image
            edged = cv2.Canny(resized, 50, 100)
            # Template match to find the template in the image
            result = cv2.matchTemplate(edged, self.template, cv2.TM_CCOEFF)
            (minVal, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # Update if found greater correlation value
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)
        self.found = found

    def draw_tattoo(self, frame):
        if self.found[0] < 8e5:
            # Correlation too low
            print("Nao foi encontrado o target")
        else:
            # Show bounding box and tattoo
            (_, maxLoc, r) = self.found
            (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            (endX, endY) = (int((maxLoc[0] + self.tW) * r), int((maxLoc[1] + self.tH) * r))

            # Remove template
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            sub_canny = edged[startY:endY, startX:endX]
            sub_frame = frame[startY:endY, startX:endX]
            cv2.imshow("Sub-Frame", sub_frame)
            # Dilate canny edges
            kernel = np.ones((3, 3), np.uint8)
            dilate = cv2.dilate(sub_canny, kernel, iterations=5)
            dilate = cv2.bitwise_not(dilate)
            cv2.imshow("Sub-Contour", dilate)
            cv2.moveWindow("Sub-Contour", 120, -10)
            # Remove template from sub-frame
            sub_frame = cv2.bitwise_or(sub_frame, sub_frame, mask=dilate)
            # Inpaint sub-frame
            dilate = cv2.bitwise_not(dilate)
            inpaint = cv2.inpaint(sub_frame, dilate, 3, cv2.INPAINT_TELEA)

            frame[startY:endY, startX:endX] = inpaint

            # Draw tattoo around detected result
            resized_tattoo = cv2.resize(self.tattoo, None, fx=r, fy=r)
            y1 = startY + self.y_offset
            y1 = 0 if y1 < 0 else y1
            y2 = y1 + resized_tattoo.shape[0]

            x1 = startX + self.x_offset
            x1 = 0 if x1 < 0 else x1
            x2 = x1 + resized_tattoo.shape[1]

            if y2 < frame.shape[0] and x2 < frame.shape[1]:
                # Tattoo fits frame
                for c in range(0, 3):
                    # Apply tattoo with transparency to image
                    alpha = resized_tattoo[:, :, 2] / 255.0
                    color = resized_tattoo[:, :, c] * (1.0 - alpha)
                    beta = frame[y1:y2, x1:x2, c] * alpha
                    frame[y1:y2, x1:x2, c] = color + beta

            # Draw a bounding box around the detected result and display the image
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
        return frame
