# PythonMaster - Interactive Learning Platform

PythonMaster is an interactive learning platform designed to help users master Python programming and Linux commands through gamified lessons, achievements, and badges.

## Features

- Interactive Python and Linux command lessons
- Progress tracking and XP system
- Achievement badges
- User profiles
- Modern, responsive UI
- Real-time progress tracking

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pythonmaster
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
pythonmaster/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   ├── css/          # CSS stylesheets
│   ├── js/           # JavaScript files
│   └── images/       # Image assets
└── templates/        # HTML templates
    ├── base.html     # Base template
    ├── index.html    # Landing page
    ├── profile.html  # User profile
    └── ...          # Other templates
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)
