# Image Disease Detection System

An end-to-end Python project for detecting diseases from images using a trained deep learning model.  
The project supports local image prediction as well as an API interface for integration with other applications.

---

## Overview

This system loads a pretrained PyTorch model and performs image classification to predict diseases from input images.  
It is designed to be simple, modular, and reusable for academic, demo, or prototype use cases.

---

## Repository Structure

├── folder/ # Supporting files / dataset / utilities
├── .gitignore # Git ignored files
├── best.pt # Trained PyTorch model
├── disease.py # Core disease prediction logic
├── main.py # Run prediction locally
├── main_api.py # API server for predictions
├── test.jpg # Sample image for testing
├── README.md # Project documentation


---

## Features

- Image-based disease detection
- Pretrained deep learning model
- Modular prediction pipeline
- REST API support
- Easy local testing
- Ready for extension or deployment

---

## Tech Stack

- Python
- PyTorch
- OpenCV
- NumPy
- Flask (API)

---

## Requirements

- Python 3.8 or above
- pip package manager

### Install Dependencies

```bash
pip install torch torchvision opencv-python numpy flask
