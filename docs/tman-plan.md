# Planning

## Keywords

- User: A user of the app
- Task: A user-defined task
- Task list: A list of tasks, a category
- Preferences: Preferences for a user

## DB Schema

- User 
    - ID : Integer
    - Username : String
    - Password : String
- Task
    - ID : Integer
    - User ID : Integer
    - List ID : Integer
    - Description : String
    - IsCompleted : Boolean
    - Time completed: Date
- TaskList
    - ID : Integer
    - Name : String
- Category
    - ID : Integer
    - Name : String
- CategoryTask
    - Category ID : Integer
    - Task ID : Integer

## Functionality

- CRUD (Create Read Update Delete)
- Add task
- Delete task
- Complete task
- Undo completed task
- Move task to another list
- Reorder task within the list
- Assign tags/category

## UI

### Main view

- Current task
- Tasks remaining today

### Planning view

- Today: Tasks that should be done by today
- Tomorrow: Tasks that should be done by tomorrow
- This week: Tasks that should be done by this week

### Settings

- Preferences
- Account
    - Change username
    - Change password
