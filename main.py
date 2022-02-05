
import tkinter
import math
from model import pose
import time

mark_detector = pose.MarkDetector()
cap = pose.cv2.VideoCapture(0)
ret, img = cap.read()
size = img.shape
font = pose.cv2.FONT_HERSHEY_SIMPLEX
# 3D model points.
model_points = pose.np.array([
    (0.0, 0.0, 0.0),  # Nose tip
    (0.0, -330.0, -65.0),  # Chin
    (-225.0, 170.0, -135.0),  # Left eye left corner
    (225.0, 170.0, -135.0),  # Right eye right corne
    (-150.0, -150.0, -125.0),  # Left Mouth corner
    (150.0, -150.0, -125.0)  # Right mouth corner
])

# Camera internals
focal_length = size[1]
center = (size[1] / 2, size[0] / 2)
camera_matrix = pose.np.array(
    [[focal_length, 0, center[0]],
     [0, focal_length, center[1]],
     [0, 0, 1]], dtype="double"
)
# while True:

def detect():
    submission = 0
    ret, img = cap.read()
    faceboxes = mark_detector.extract_cnn_facebox(img)
    for facebox in faceboxes:
        face_img = img[facebox[1]: facebox[3],
                   facebox[0]: facebox[2]]
        face_img = pose.cv2.resize(face_img, (128, 128))
        face_img = pose.cv2.cvtColor(face_img, pose.cv2.COLOR_BGR2RGB)
        marks = mark_detector.detect_marks([face_img])
        marks *= (facebox[2] - facebox[0])
        marks[:, 0] += facebox[0]
        marks[:, 1] += facebox[1]
        shape = marks.astype(pose.np.uint)
        # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
        image_points = pose.np.array([
            shape[30],  # Nose tip
            shape[8],  # Chin
            shape[36],  # Left eye left corner
            shape[45],  # Right eye right corne
            shape[48],  # Left Mouth corner
            shape[54]  # Right mouth corner
        ], dtype="double")
        dist_coeffs = pose.np.zeros((4, 1))  # Assuming no lens distortion
        (success, rotation_vector, translation_vector) = pose.cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                      dist_coeffs, flags=pose.cv2.SOLVEPNP_UPNP)
        # Project a 3D point (0, 0, 1000.0) onto the image plane.
        # We use this to draw a line sticking out of the nose

        (nose_end_point2D, jacobian) = pose.cv2.projectPoints(pose.np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                         translation_vector, camera_matrix, dist_coeffs)

        for p in image_points:
            pose.cv2.circle(img, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        x1, x2 = pose.draw_annotation_box(img, rotation_vector, translation_vector, camera_matrix)

        pose.cv2.line(img, p1, p2, (0, 255, 255), 2)
        pose.cv2.line(img, tuple(x1), tuple(x2), (255, 255, 0), 2)
        # for (x, y) in shape:
        #     pose.cv2.circle(img, (x, y), 4, (255, 255, 0), -1)
        # pose.cv2.putText(img, str(p1), p1, font, 1, (0, 255, 255), 1)
        try:
            m = (p2[1] - p1[1]) / (p2[0] - p1[0])
            ang1 = int(math.degrees(math.atan(m)))
        except:
            ang1 = 90

        try:
            m = (x2[1] - x1[1]) / (x2[0] - x1[0])
            ang2 = int(math.degrees(math.atan(-1 / m)))
        except:
            ang2 = 90

            # print('div by zero error')
        pose.cv2.putText(img, str(ang1), tuple(p1), font, 2, (128, 255, 255), 3)
        pose.cv2.putText(img, str(ang2), tuple(x1), font, 2, (255, 255, 128), 3)
        submission = rotation_vector[2]
    pose.cv2.imshow('img', img)
    # if pose.cv2.waitKey(1) & 0xFF == ord('q'):
    #    return
    return submission


if __name__ == "__main__":
    for i in range(1000):
        angle = detect()
        print(angle)
        if angle > 0.8 or angle < -0.8:
            print("looked away")
        elif angle is None or angle == 0:
            print("no face detected")
        else:
            print("looking forward")

    pose.cv2.destroyAllWindows()
    cap.release()
