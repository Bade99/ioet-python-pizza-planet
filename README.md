<h1 align="center"> Python Pizza Planet </h1>

![python-badge](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)

This is an example software for a pizzeria that takes customizable orders.

## Table of Contents
- [Getting started](#getting-started)
- [Running the backend project](#running-the-backend-project)
- [Testing the backend](#testing-the-backend)
- [Running the frontend](#running-the-frontend)
- [Tickets board](#tickets-board)

## Getting started

You will need the following general tools:

- A Python interpreter installed. [3.8.x](https://www.python.org/downloads/release/python-3810/) is preffered.

- A text editor: preferably [Visual Studio Code](https://code.visualstudio.com/download)

- Extensions such as [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

## Running the backend project

- Create a virtual environment in the root folder

```bash
python3 -m venv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate 
```

- Install all necessary dependencies:

```bash
pip3 install -r requirements.txt
```

- Start the database:

```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

- Run the project with:

```bash
python3 manage.py run
```

### Testing the backend

- Make sure that you have `pytest` installed

- Run the test command

```bash
python3 manage.py test
```

## Running the frontend

- Clone git UI submodule

```bash
git submodule update --init
```

- Install Live Server extension from [here](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) on VSCode Quick Open (`Ctrl + P`)

```bash
ext install ritwickdey.LiveServer
```

- To run the frontend, start `ui/index.html` file with Live Server (Right click `Open with Live Server`)

## Tickets board

TBD
