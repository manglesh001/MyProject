import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
from IPython.display import HTML

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose

# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils 


def detectPose(image, pose, display=True):
   
    
    # Create a copy of the input image.
    output_image = image.copy()
    
    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform the Pose Detection.
    results = pose.process(imageRGB)
    
    # Retrieve the height and width of the input image.
    height, width, _ = image.shape
    
    # Initialize a list to store the detected landmarks.
    landmarks = []
    
    # Check if any landmarks are detected.
    if results.pose_landmarks:
    
        # Draw Pose landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        
        # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:
            
            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    
    # Check if the original input image and the resultant image are specified to be displayed.
    if display:
    
        # Display the original input image and the resultant image.
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
        # Also Plot the Pose landmarks in 3D.
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
        
    # Otherwise
    else:
        
        # Return the output image and the found landmarks.
        return output_image, landmarks





def calculateAngle(landmark1, landmark2, landmark3):
  

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle


# Calculate the angle between the three landmarks.
angle = calculateAngle((558, 326, 0), (642, 333, 0), (718, 321, 0))

# Display the calculated angle.
# print(f'The calculated angle is {angle}')

title="Yoga Pose"
def classifyPose(landmarks, output_image, display=False):
 
    
    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)
    
    # Calculate the required angles.
    #----------------------------------------------------------------------------------------------------------------
    
    # Get the angle between the left shoulder, elbow and wrist points. 
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
    # Get the angle between the right shoulder, elbow and wrist points. 
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    
    # Get the angle between the left elbow, shoulder and hip points. 
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points. 
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points. 
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points 
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    hip_angle_right = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])

    hip_angle_left = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    
    #----------------------------------------------------------------------------------------------------------------
    
    # Check if it is the warrior II pose or the T pose.
    # As for both of them, both arms should be straight and shoulders should be at the specific angle.
    #----------------------------------------------------------------------------------------------------------------
    if left_elbow_angle > 160 and left_elbow_angle < 200 or right_elbow_angle > 160 and right_elbow_angle < 200:

    #     # Check if shoulders are at the required angle.
        if left_shoulder_angle > 160 and left_shoulder_angle < 200 or right_shoulder_angle > 160 and right_shoulder_angle < 200:

    # #----------------------------------------------------------------------------------------------------------------
                # Check if the other leg is bended at the required angle.
            if left_knee_angle > 160 and left_knee_angle < 200 or right_knee_angle > 160 and right_knee_angle < 200:
                title=label = "Mountain Pose"
                
               
    #
    #--------------------------------
    if left_elbow_angle > 160 and left_elbow_angle < 200 or right_elbow_angle > 160 and right_elbow_angle < 200:

    #     # Check if shoulders are at the required angle.
        if left_shoulder_angle > 160 and left_shoulder_angle < 200 or right_shoulder_angle > 160 and right_shoulder_angle < 200:

    # #----------------------------------------------------------------------------------------------------------------
                # Check if the other leg is bended at the required angle.
            if left_knee_angle > 160 and left_knee_angle < 200 or right_knee_angle > 160 and right_knee_angle < 200:
               
                if hip_angle_right >60 and hip_angle_right <110 or hip_angle_left >60 and hip_angle_left <110:
                    
                    title=label = "Staff Pose"
    
    #-----------------------------
    if left_elbow_angle > 160 and left_elbow_angle < 200 or right_elbow_angle > 160 and right_elbow_angle < 200:

    #     # Check if shoulders are at the required angle.
        if left_shoulder_angle > 0 and left_shoulder_angle < 30 or right_shoulder_angle > 0 and right_shoulder_angle < 30:

    # #----------------------------------------------------------------------------------------------------------------
                # Check if the other leg is bended at the required angle.
            if left_knee_angle > 0 and left_knee_angle < 20 or right_knee_angle > 0 and right_knee_angle < 20:
                title=label = "Butterfly Pose"
                
    #-----------
    #-------------
    #-------------mountain pose
    if left_elbow_angle > 160 and left_elbow_angle < 200 or right_elbow_angle > 160 and right_elbow_angle < 200:

    #     # Check if shoulders are at the required angle.
        if left_shoulder_angle > 0 and left_shoulder_angle < 30 or right_shoulder_angle > 0 and right_shoulder_angle < 30:

    # #----------------------------------------------------------------------------------------------------------------
                # Check if the other leg is bended at the required angle.
            if left_knee_angle > 160 and left_knee_angle < 200 or right_knee_angle > 160 and right_knee_angle < 200:
                
                if hip_angle_right >160 and hip_angle_right <200 or hip_angle_left >160 and hip_angle_left <200:
                    label = "Standing Pose"
                    title="Standing Pose"
               
    #-----------
    #----------------

    #-----------for squat
    if left_elbow_angle > 160 and left_elbow_angle < 200 or right_elbow_angle > 160 and right_elbow_angle < 200:

    #     # Check if shoulders are at the required angle.
        if left_shoulder_angle > 80 and left_shoulder_angle < 130 or right_shoulder_angle > 80 and right_shoulder_angle < 130:

    # #----------------------------------------------------------------------------------------------------------------
                # Check if the other leg is bended at the required angle.
            if left_knee_angle > 40 and left_knee_angle < 100 or right_knee_angle > 40 and right_knee_angle < 100:
                title=label = "Squat"
                
    #-----------
    
    
    # Check if the both arms are straight.
    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:

        # Check if shoulders are at the required angle.
        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:

    # Check if it is the warrior II pose.
    #----------------------------------------------------------------------------------------------------------------

            # Check if one leg is straight.
            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

                # Check if the other leg is bended at the required angle.
                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:

                    # Specify the label of the pose that is Warrior II pose.
                    title=label = 'Warrior II Pose' 
                   
                    
                     
    #----------------------------------------------------------------------------------------------------------------
    
    # Check if it is the T pose.
    #----------------------------------------------------------------------------------------------------------------
    
            # Check if both legs are straight
            if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:

                # Specify the label of the pose that is tree pose.
                title=label = 'T Pose'
                

    #----------------------------------------------------------------------------------------------------------------
    
    # Check if it is the tree pose.
    #----------------------------------------------------------------------------------------------------------------
    
    # Check if one leg is straight
    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

        # Check if the other leg is bended at the required angle.
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:

            # Specify the label of the pose that is tree pose.
            title=label = 'Tree Pose'
            
    if label == 'Unknown Pose':
        
        poses_ranges = {
        'Butterfly Pose': [(160, 200), (160, 200), (0, 30), (0, 30), (0, 20), (0, 20)],
        'Standing Pose': [(160, 200), (160, 200), (0, 30), (0, 30), (160, 200), (160, 200)],
        'Staff Pose': [(160, 200), (160, 200), (160, 200), (160, 200), (160, 200), (160, 200)],
        'Mountain Pose': [(160, 200), (160, 200), (160, 200), (160, 200), (160, 200), (160, 200)],
        'Squat': [(160, 200), (160, 200), (80, 130), (80, 130), (40, 80), (40, 80)],
        'Warrior II Pose': [(165, 195), (165, 195), (80, 110), (80, 110), (165, 195), (90, 120)],
        'T Pose': [(165, 195), (165, 195), (80, 110), (80, 110), (160, 195), (160, 195)],
        'Tree Pose': [(165, 195), (165, 195), (80, 110), (80, 110), (165, 195), (25, 45)],
    }

        def calculate_distance(angles1, ranges):
            # Calculate the distance between two sets of angles considering the ranges
            distances = []
            for angle1, (a1, b1) in zip(angles1, ranges):
                angle_diff = min(abs(angle1 - b1), abs(angle1 - a1))
                distances.append(angle_diff)
            
            return np.linalg.norm(distances)

        def find_nearest_pose(input_angles):
            # Initialize variables to store the nearest pose and minimum distance
            nearest_pose = None
            min_distance = float('inf')

            # Initialize a variable to store the differences in angles
            angle_differences = []

            # Iterate over each pose and calculate the distance
            for pose_name, pose_ranges in poses_ranges.items():
                distance = calculate_distance(input_angles, pose_ranges)

                # Update the nearest pose if the current distance is smaller
                if distance < min_distance:
                    min_distance = distance
                    nearest_pose = pose_name
                    # Calculate the differences in angles
                    angle_differences = [min(abs(angle - range[1]), abs(angle - range[0])) for angle, range in zip(input_angles, pose_ranges)]

            return nearest_pose, angle_differences

        # Example usage:
        input_angles = [left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle, left_knee_angle, right_knee_angle]
        nearest_pose, angle_differences = find_nearest_pose(input_angles)

        title="Similar to " + nearest_pose
        label = "Angle differences from  " + nearest_pose + " in order of(Left Elbow, Right Elbow, Left Shoulder, Right Shoulder, Left Knee, Right, Knee)"
        for a in angle_differences:
            label=label + " " + str(round(a, 3)) 


    return label, title
    # Check if the pose is classified successfully
    if label != 'Unknown Pose':
        
        # Update the color (to green) with which the label will be written on the image.
        color = (0,0,255)  
    
    # Write the label on the output image. 
    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 5)
    
    # Check if the resultant image is specified to be displayed.
    if display:
    
        # Display the resultant image.
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    else:
        
        # Return the output image and the classified label.
        return output_image, label



def OutputPose(path):
    image = cv2.imread(path)
    output_image, landmarks = detectPose(image, pose, display=False)
    image_bytes = cv2.imencode('.jpg', output_image)[1].tobytes()
    # posing = "Yoga Pose"
   
    if landmarks:
        label, title=classifyPose(landmarks, output_image, display=True)
  
    return image_bytes, label, title
