AI Fitness - Both Arm Counter

A real-time arm exercise counter using OpenCV and Pose Estimation. This project detects the angles of your arms and counts repetitions automatically for both the right and left arms.

Features

Real-time detection using a webcam

Counts repetitions for both arms independently

Displays progress bars for each arm

Shows current FPS for performance monitoring

Reset counter functionality with a single key press

Requirements

Python 3.7+

OpenCV

NumPy

PoseEstimationModule (custom module, include PoseEstimationModule.py in the repo)

Install dependencies via pip:

pip install opencv-python numpy

Usage

Clone the repository:

git clone https://github.com/yourusername/AI-Fitness-Arm-Counter.git
cd AI-Fitness-Arm-Counter


Ensure PoseEstimationModule.py is in the same folder.

Run the application:

python main.py


Controls:

Press q to quit

Press r to reset the counters

How It Works

Pose Detection: Uses PoseEstimationModule to detect key points of the arms

Angle Calculation: Computes the angle of the elbows to track movement

Repetition Counting: Updates counters based on specific angle thresholds

Visualization: Displays bars for each arm, repetition counts, and FPS on the screen

File Structure
AI-Fitness-Arm-Counter/
│
├─ main.py                  # Main application
├─ PoseEstimationModule.py  # Pose estimation helper
├─ README.md                # Project documentation