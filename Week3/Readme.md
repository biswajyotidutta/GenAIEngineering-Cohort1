# Setting Up Your Development Environment

## Clone the GitHub Repository

First, clone the repository using Git:

```bash
# Clone the repository
git clone https://github.com/outskill-git/GenAIEngineering-Cohort1

# Navigate into the repository folder
cd GenAIEngineering-Cohort1
```

## Navigate to the Week 1 Directory

Move into the Week_3 directory:

```bash
# Navigate to the Week3 directory
cd Week3
```

## Create and Configure Environment Variables

Create a `.env` file to store your Hugging Face API token:

```bash
# Create a .env file
touch .env

# For Windows, use:
# type nul > .env
```

Open the `.env` file in your preferred text editor and add your Hugging Face API token:

```
GROQ_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Make sure to replace `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your actual Hugging Face API token.

## Create a Virtual Environment

Create and activate a Python virtual environment:

### For Windows:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

### For macOS/Linux:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

## Install Requirements

Install the packages listed in requirements.txt:

```bash
# Install required packages
pip install -r requirements.txt
```

## Verify Installation

Verify that everything is set up correctly:

```bash
# Check installed packages
pip list
```
