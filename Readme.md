# Time Table Management System

This is a Flask-based web application for managing teachers, courses, classrooms, and generating/viewing timetables.

## Features

- Add and view teachers, courses, and classrooms
- Generate and view timetables
- Simple web interface using Bootstrap

## Requirements

- Python 3.x
- Flask
- SQLite (included with Python)

## Installation

1. **Clone or download this repository.**

2. **(Optional but recommended) Create and activate a virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Ensure you have a SQLite database file named `timetable.db` in the project folder.**
   - If not, the app will create it automatically when you add data.

## Running the App

1. **Start the Flask server:**
   ```
   flask run
   ```
   or
   ```
   python app.py
   ```

2. **Open your browser and go to:**  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure

```
time_table/
│
├── app.py
├── database.py
├── requirements.txt
├── timetable.db
└── templates/
    ├── homepage.html
    ├── create_teacher.html
    ├── create_course.html
    ├── create_classroom.html
    ├── view_teachers.html
    ├── view_courses.html
    ├── view_classrooms.html
    ├── view_timetable.html
    └── generate_timetable.html
```

## Database

- Uses SQLite (`timetable.db`)
- You can view or edit the database using [DB Browser for SQLite](https://sqlitebrowser.org/).

## Notes

- Make sure all required templates exist in the `templates` folder.
- For any issues, check the Flask debug output in your terminal.

---

**Enjoy using the Time Table Management System!**