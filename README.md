# Pepper Potts - Task Management Project

## Overview

Pepper Potts is a project aimed at showcasing task management functionality, including authentication, authorization.

## Setup

To set up the project locally, follow these steps:

1. **Clone the repository**:

   ```
   git clone https://github.com/vfiliplima/Pepper-Potts.git
   ```

2. **Navigate to the project folder**:

   ```
   cd Pepper-Potts
   ```

3. **Build the Docker containers**:

   ```
   docker-compose build
   ```

4. **Run the containers**:

   ```
   docker-compose up
   ```

5. **Create DB Tables**:

   ```
   docker-compose web run python manage.py migrate
   ```

6. **Run tests**:

   ```
   docker-compose web run pytest
   ```

## Usage

Once the project is set up, and you server is running, here are some steps to get started:

1. **Registration & Login**: On your home page (task listing) you'll be able to see all existing tasks. On the top right corner you'll see a "Login" "Sign Up" link. Click "Sign Up" to create a new user (provide username and password). You'll be redirected to login page. enter your credentials and you should be looking at the task listing page with your username logged in (top right corner).

2. **Create Tasks**: Hit the "Create New Task" button to create new tasks. These should be automatically added to the updated list of tasks once created.

3. **Seeing, Editing and Deleting**: Once created and added to task list, you can click the 'card' of the task you have created to be taken to task detail page. On the task detail page, you can edit and delete your tasks.

4. **Filtering tasks by priority**: Create several tasks with different "priorities". You can now use the filter to only see the desired "priority" tasks.

## Notes

- You'll only be able to click a task and navigate to task detail page if you are the "creator" of that task.
- You only have access to "edit" and "delete" buttons on task detail page.
- Additional features include:
  - Search bar: allow searching for task title.
  - Pagination: display limited amount of tasks per page.
  - Task completion fucntionality: easy and intuitive way to mark tasks as "completed".
  - Task List Filter: Add option to only see tasks associated with logged user on task list.
