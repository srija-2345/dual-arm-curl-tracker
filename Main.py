import cv2
import time
import numpy as np
import PoseEstimationModule as ptm
def update_counter(angle, count, direction):
    per = np.interp(angle, (210, 320), (0, 100))
    if per >= 95 and direction == 0:
        count += 0.5
        direction = 1
    if per <= 5 and direction == 1:
        count += 0.5
        direction = 0
    return count, direction, per

def draw_bar(img, per, x_start, x_end, h):
    bar = np.interp(per, (0, 100), (int(h * 0.85), int(h * 0.25)))
    cv2.rectangle(img,(x_start, int(h * 0.25)),(x_end, int(h * 0.85)),(0, 255, 0), 3)
    cv2.rectangle(img,(x_start, int(bar)),(x_end, int(h * 0.85)),(0, 255, 0), cv2.FILLED)
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access camera")
        return
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cap.set(cv2.CAP_PROP_ZOOM, 0)
    detector = ptm.Detector()
    countR, countL = 0, 0
    dirR, dirL = 0, 0
    ptime = 0
    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        h, w = img.shape[:2]

        img = detector.findpos(img, False)
        lmlist = detector.getposition(img, draw=False)

        if len(lmlist) != 0:

            # For the Right Arm --------
            angleR = detector.findangle(img, 12, 14, 16, True)
            countR, dirR, perR = update_counter(angleR, countR, dirR)

        # For the Left Arm
            angleL = detector.findangle(img, 11, 13, 15, True)
            countL, dirL, perL = update_counter(angleL, countL, dirL)
            draw_bar(img, perR, int(w * 0.92), int(w * 0.96), h)
            draw_bar(img, perL, int(w * 0.04), int(w * 0.08), h)
            cv2.rectangle(img,
                          (0, int(h * 0.88)),
                          (w, h),
                          (50, 50, 50), cv2.FILLED)
            cv2.putText(img, f'Right: {int(countR)}',
                        (int(w * 0.65), int(h * 0.95)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.putText(img, f'Left: {int(countL)}',
                        (int(w * 0.05), int(h * 0.95)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        ctime = time.time()
        fps = 1 / (ctime - ptime) if ctime != ptime else 0
        ptime = ctime
        cv2.putText(img, f'FPS: {int(fps)}',
                    (int(w * 0.03), int(h * 0.1)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        cv2.imshow("AI Fitness - Both Arm Counter", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('r'):
            countR, countL = 0, 0
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
