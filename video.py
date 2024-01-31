import cv2
cap = cv2.VideoCapture(0)
def capture_image():
    # Open the video capture object for the camera
    cap = cv2.VideoCapture(0)

    # Read a frame from the camera
    ret, frame = cap.read()

    # Save the frame as an image
    cv2.imwrite('captured_image.png', frame)

    # Release the video capture object and close all windows
    # cap.release()
    # cv2.destroyAllWindows()

def display_live_video():
    # Open the video capture object for the camera
    

    # Create a while loop to continuously read and display the frames
    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        cv2.imshow('Live Video', frame)  # Display the frame

        # Check for the 'q' key to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Check for the 'c' key to capture an image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            capture_image()

    # Release the video capture object and close all windows
    # cap.release()
    # cv2.destroyAllWindows()


# Call the function to display the live video
display_live_video()