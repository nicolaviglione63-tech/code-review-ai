# code-review-ai
AI-powered code review tool built with FastAPI and OpenAI.

## Overview

This project demonstrates how to build a simple AI-based code review system in under 100 lines of Python.

It analyzes code and returns:
- Issues
- Suggestions
- Score

## Tech Stack

- Python
- FastAPI
- OpenAI API

## How it works

The application sends user code to an AI model which returns structured feedback in JSON format.

## Run locally

```bash
pip install fastapi uvicorn openai
uvicorn main:app --reload
