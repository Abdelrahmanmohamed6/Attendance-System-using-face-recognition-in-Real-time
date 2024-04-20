# Attendance-System-using-face-recognition-in-Real-time
# Face Attendance System

This repository contains a Python-based face attendance system. The system leverages face recognition technology to mark attendance of students using live camera feed. It also integrates with Firebase Realtime Database for storing student information and attendance records.

## Features

- **Live Camera Attendance**: Real-time attendance marking using face recognition.
- **Firebase Integration**: Store student information and attendance records in Firebase Realtime Database.
- **Add/Delete Students**: Add and delete student information from the system.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/face-attendance-system.git

2. Install the required dependencies:
   ```bash
    pip install -r requirements.txt

3. Set up Firebase:
    - Create a Firebase project and obtain the service account key JSON file.
    - Replace "serviceAccountKey.json" with your actual service account key file.
    - Set the database URL and storage URL in dbconn_ref_bucket() function in db.py.
## Usage
1. Run the main script main.py:
   ```bash
   python main.py
    
2. The system will open a live camera feed. Recognize faces to mark attendance.
Use keyboard shortcuts:
    - Press q to quit the system.
    - Press a to add a new student.
    - Press d to delete a student.
## Contributing
Contributions are welcome! Please follow these steps:

  - Fork the repository.
  - Create a new branch (git checkout -b feature/new-feature).
  - Make your changes.
  - Commit your changes (git commit -am 'Add new feature').
  - Push to the branch (git push origin feature/new-feature).
  - Create a new Pull Request.
## License
This project is licensed under the MIT License - see the LICENSE file for details.


