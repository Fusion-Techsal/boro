import sys
import cv2
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class Mrr_Animation(QMainWindow):
    play_video_signal = pyqtSignal(str)

    def __init__(self):
        super(Mrr_Animation, self).__init__()

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        # self.btn_sad = QPushButton("Play Sad", self)
        # self.btn_sad.clicked.connect(lambda: self.play_emotion("sad.mp4"))

        # self.btn_angry = QPushButton("Play Angry", self)
        # self.btn_angry.clicked.connect(lambda: self.play_emotion("angry.mp4"))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_label)
        # self.layout.addWidget(self.btn_sad)
        # self.layout.addWidget(self.btn_angry)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.continuous_play = True
        self.current_state = "normal"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.play_video_signal.connect(self.play_video, Qt.QueuedConnection)

        self.play_normal_loop()  # Start playing the normal video continuously

        self.setWindowTitle("MRR-C1")

    @pyqtSlot(str)
    def play_video(self, video_file):
        if self.current_state != video_file.split(".")[0]:
            self.continuous_play = False

        cap = cv2.VideoCapture(video_file)
        if not cap.isOpened():
            print("Error opening video file")
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.video_label.setFixedSize(640, 480)

        self.cap = cap
        self.timer.start(30)

    @pyqtSlot()
    def update_frame(self):
        ret, frame = self.cap.read()

        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame = cv2.resize(rgb_frame, (640, 480))

            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w

            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            self.video_label.setPixmap(pixmap)
        else:
            self.cap.release()
            self.timer.stop()

            if self.continuous_play:
                self.play_normal_loop()
            else:
                # The emotion video has ended, restart normal.mp4 loop
                self.play_normal_loop()

    def play_normal(self):
        self.play_video_signal.emit("animations/normal.mp4")

    def play_normal_loop(self):
        self.continuous_play = True
        self.play_normal()

    def play_emotion(self, emotion_file):
        self.continuous_play = True
        self.play_video_signal.emit(emotion_file)

    def closeEvent(self, event):
        self.continuous_play = False
        self.timer.stop()
        self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mrr_Animation()
    window.show()
    sys.exit(app.exec_())
