
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import numpy as np
import cv2
from pyzbar.pyzbar import decode

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if img: 
            for barcode in decode(img):
                data = barcode.data.decode('utf-8')
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (255,0,255), 5)
                pts2 = barcode.rect
                cv2.putText(img, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.9, (255, 0, 255), 2)
        # img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

        return img


webrtc_streamer(key="example", video_processor_factory=VideoTransformer)
