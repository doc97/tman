# TMan
This is a database project for a [course](https://materiaalit.github.io/tsoha-18/) at The University of Helsinki.

**Note**: This project is **not** under active development but if you have any problems or find any
bugs, please create a Github [issue](https://github.com/doc97/tman/issues)!

## Description
TMan is an application that can help you manage your time you spend during your day. It offers 
easy-to-use features to manage your day. But it is more than just a simple todo-list. You can categorize 
and prioritize your tasks. This way you can declutter your day and focus on taking one 
step at the time.

## Features
- [x] Registration and login
- [x] Remember Me for login
- [x] Add tasks
- [x] Delete tasks
- [x] Complete tasks
- [x] Edit task description
- [x] Undo completion of tasks
- [x] View Today, Tomorrow and Weekly task lists
- [x] Assign/remove tags to/from tasks
- [x] Order tasks
- [x] Search tasks by description
- [x] Search tasks by tags
- [x] Create, edit, delete tags
- [ ] Account settings

## Installation

The app is running on Heroku so there is no need to install it to use it. If you however want to
run the app on your local machine here are some instructions on how to do it. If you are using python 3
by default you can leave out the '3' in `python3` and `pip3`.

Clone the repository:
```bash
git clone https://github.com/doc97/tman.git
cd tman/
```

Install and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install requirements in the virtual environment:
```bash
pip3 install -r requirements.txt
```

Run the local webserver:
```bash
python3 run.py
```

Open up the browser and go to the URL `localhost:5000`

## Manual
Check the [manual](docs/manual.md) for instructions on how to use all of the available features.

## Known issues

- When logging out and trying to log back in, you have to log in twice. It has to do with CSRF form protection.
- There is currently no way to delete your account or reset a forgotten password. If you wish to do so, please
contact me at daniel.riissanen[at]helsinki.fi.

For any other issue, create a Github [issue](https://github.com/doc97/tman/issues).

## Feature requests

I accept feature request but do not promise to implement them. Please use Github's issue system to submit a
feature request.

## Links
[Heroku app](https://tsoha-tman.herokuapp.com)  
[User stories](docs/user-stories.md)  
[Database schema](docs/db-schema.md)  

## Contact

daniel.riissanen[at]helsinki.fi
