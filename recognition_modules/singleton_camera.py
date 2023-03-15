import cv2

class SingletonCamera:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonCamera, cls).__new__(cls)
            cls._instance.activateCamera()
        return cls._instance

    def activateCamera(self):
        self._camera_capture = cv2.VideoCapture(0)

    def getCurrentFrame(self):
        "Returns the return code: int and frame: numpy arr -> (ret, frame)"
        self._return, self._frame = self._camera_capture.read()
        return self._return, self._frame

    def closeCamera(self):
        self._camera_capture.release()
