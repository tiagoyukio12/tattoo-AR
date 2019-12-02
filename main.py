import cv2 as cv2

import FingersNumberDetector
import TemplateDetector


def main():
    window_cam = "Tattoo AR"
    cv2.namedWindow(window_cam)
    cap = cv2.VideoCapture(0)
    template_detector = TemplateDetector.TemplateDetector("template.png", "tattoo.png")
    finger_detector = FingersNumberDetector.FingersNumberDetector(cap)

    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    # Loop while webcam is active
    while ret:
        ret, frame = cap.read()

        template_detector.detect_template(frame)
        frame = template_detector.draw_tattoo(frame)

        # Detect hand
        frame = cv2.LUT(frame, finger_detector.lookUpTable)
        cv2.rectangle(frame, (finger_detector.x0, finger_detector.y0),
                      (finger_detector.x0 + finger_detector.width - 1, finger_detector.y0 + finger_detector.height - 1),
                      (255, 0, 0), 2)

        k = cv2.waitKeyEx(1)
        if k == ord("z"):
            finger_detector.isHandHistCreated = True
            handHist = finger_detector.createHandHistogram(frame)
        elif k == ord('b'):
            finger_detector.bgSubtractor = cv2.createBackgroundSubtractorMOG2(10, finger_detector.bgSubThreshold)
            finger_detector.isBgCaptured = True
        elif k == ord("r"):
            finger_detector.bgSubtractor = None
            finger_detector.isBgCaptured = False
        elif k == ord("q"):
            break

        if finger_detector.isHandHistCreated and finger_detector.isBgCaptured:
            finger_detector.detectHand(frame, handHist)
        elif not finger_detector.isHandHistCreated:
            finger_detector.drawRect(frame)

        # Move tattoo offset
        if k == 2424832:
            template_detector.x_offset -= 10
        elif k == 2490368:
            template_detector.y_offset -= 10
        elif k == 2555904:
            template_detector.x_offset += 10
        elif k == 2621440:
            template_detector.y_offset += 10

        # Move hand ROI
        if k == ord("q"):
            break
        elif k == ord("j"):
            finger_detector.y0 = min(finger_detector.y0 + 20, finger_detector.frame_height - finger_detector.height)
        elif k == ord("k"):
            finger_detector.y0 = max(finger_detector.y0 - 20, 0)
        elif k == ord("h"):
            finger_detector.x0 = max(finger_detector.x0 - 20, 0)
        elif k == ord("l"):
            finger_detector.x0 = min(finger_detector.x0 + 20, finger_detector.frame_width - finger_detector.width)

        # Update window
        cv2.imshow(window_cam, frame)

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()
