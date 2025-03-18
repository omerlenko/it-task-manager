# IT Task Manager

## Overview
This portfolio project is a comprehensive task manager for an IT company, built with Django. It addresses real-world challenges in team task management and includes a variety of features to facilitate efficient workflow and collaboration. The application allows team members to create, assign, and complete tasks, while also providing a dynamic dashboard for managers to view key metrics, filter tasks, and assess team workloads.

## Key Features

### Custom User & Role Management
- Custom Worker model (extending `AbstractUser`) with a Position model to categorize roles (e.g., Developer, Designer, QA Specialist).

### Task Management
- Creation, assignment, and completion of tasks.
- Task model with fields for name, description, deadline, priority (Urgent, High, Medium, Low), task type, and tags.
- Inline tag creation using a comma-separated text input (Many-to-Many relationship with Tag).

### Filtering, Sorting, and Searching
- Advanced filtering on the task list by status, priority, and assignees.
- Sorting options by priority, status, and deadline with custom logic for proper ordering.
- A search bar to search tasks by title and description.

### Dashboard with Dynamic Widgets
- A card-based dashboard providing an overview of:
  - **Task Overview:** Total, pending, and completed tasks.
  - **Upcoming Deadlines:** A list of tasks nearing their deadlines.
  - **Tasks by Priority:** Displayed with color-coded badges and clickable counts for quick filtering.
  - **Weekly Progress:** A progress bar summarizing weekly task completion.
  - **Active Projects:** A card listing the user’s active projects with brief descriptions.
  - **Teams:** A card displaying the teams the user belongs to, including a summary of members.
- Dual dropdown filters at the top allow switching between workers and projects for a focused view.

### Teams & Projects Integration
- **Team model:** Contains team names and a Many-to-Many relationship with workers.
- **Project model:** Associated with teams and tasks, with dedicated list and detail views.
- Consistent, card-based design across Teams and Projects pages.

### UI/UX Enhancements
- Responsive, card-based layouts using Bootstrap.
- Consistent spacing, equal card heights, and neat alignment for a professional appearance.
- Pagination that preserves filtering, sorting, and search parameters.

## Installation

### Prerequisites
- Python 3.x
- Django
- A virtual environment tool (e.g., `venv` or `virtualenv`)

### Steps to Set Up the Project

1. **Clone the repository:**
   ```sh
   git clone https://github.com/omerlenko/it-task-manager.git
   cd it-task-manager
   
2. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the project root and add:
     ```sh
     SECRET_KEY='your-secret-key-here'
     ```

5. **Apply Migrations:**
   ```sh
   python manage.py migrate
   ```

6. **Create a Superuser:**
   ```sh
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```sh
   python manage.py runserver
   ```
   Access the project at `http://127.0.0.1:8000/`.

## Dependencies
All required dependencies are listed in the `requirements.txt` file. Install them with:
```sh
pip install -r requirements.txt
```

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** Bootstrap (HTML, CSS)
- **Database:** SQLite (default), with options to switch to PostgreSQL or MySQL
