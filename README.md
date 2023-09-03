# Amharic **Text-to-Speech (TTS)**

![Repo size](https://img.shields.io/github/repo-size/moanbekele/Text-to-Speech-Amharic)
![Pep8 style](https://img.shields.io/badge/PEP8-style%20guide-purple?style=round-square)
![Latest commit](https://img.shields.io/github/last-commit/moanbekele/Text-to-Speech-Amharic/main?style=round-square)


Welcome to the ATRONS GitHub repository! ATRONS is an online resource sharing and learning platform designed to provide users with a seamless experience for accessing and sharing educational resources. This repository contains the source code and development history of the ATRONS platform.

## Structure

The repository is structured as follows:

- `backend/`: <a href="https://github.com/moanbekele/Text-to-Speech-Amharic/tree/main/main">Link for the Backend</a>
> - `frontend/`: <a href="https://github.com/moanbekele/Text-to-Speech-Amharic/tree/main/templates">Here</a>, you will find the frontend code, implemented using JavaScript, and Flask. This directory also includes the HTML, CSS, and JavaScript files for the user interface.
- `models/`: This directory contains the trained Generative AI models used by ATRONS to enhance the platform's capabilities. The models are implemented using Python-based AI/ML libraries, and they play a crucial role in solving specific problems such as visual question answering (VQA).

## Purpose

The purpose of this repository is to provide a collaborative space for development and improvement of the ATRONS  platform. By making the repository publicly accessible, we aim to foster community engagement, allowing developers, contributors, and users to explore the codebase, report issues, and suggest enhancements.

## How Generative AI Models are Solving the Problem

ATRONS leverages Generative AI models to enhance the platform's functionality, particularly in the domain of visual question answering (VQA). The chosen Generative AI models, such as the `dandelin/vilt-b32-finetuned-vqa` model, have been fine-tuned to process and interpret images containing questions from users. These models utilize cutting-edge techniques in computer vision and natural language processing to generate accurate and meaningful responses to user queries.

By incorporating Generative AI models into ATRONS, we enable users to ask questions about visual content, such as diagrams, images, or screenshots, and receive relevant answers. This significantly enhances the learning experience, as users can obtain detailed explanations, insights, or clarifications about the resources they are interacting with. It opens up new possibilities for interactive and dynamic learning, making ATRONS a powerful platform for knowledge sharing and acquisition.


## Installation
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
