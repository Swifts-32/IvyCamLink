import cv2
from ivycamlink import IvyCamCapture

def on_focus_changed(val, cap_instance):
    # Callback trigger when trackbar moves
    cap_instance.set_focus(val)

def main():
    cap = IvyCamCapture(port=5001)
    
    if not cap.open():
        print("Failed to launch IvyCam link pipeline.")
        return

    window_name = "IvyCam Stream Processing"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    cv2.createTrackbar("Focus", window_name, 0, 100, lambda val: on_focus_changed(val, cap))

    print("Pipeline running. Move the 'Focus' slider bar to adjust camera lens...")
    while True:
        success, frame = cap.read()
        
        if not success:
            print("Dropped stream sync.")
            break

        # Display the frame matrix inside the window
        cv2.imshow(window_name, frame)

        # Handle keyboard exits safely
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Safely release the background stream resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()