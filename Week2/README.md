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

Move into the Week_2 directory:

```bash
# Navigate to the Week2 directory
cd Week2
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
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Make sure to replace `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your actual Hugging Face API token.

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

## Load Environment Variables in Your Code

Add the following code at the beginning of your Python scripts to load the API token:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API token
hf_token = os.getenv("HF_TOKEN")
```

## Deactivate Virtual Environment

When you're done working, you can deactivate the virtual environment:

```bash
# Deactivate the virtual environment
deactivate
```

## Important Security Notes

1. Never commit your `.env` file to version control
2. Add `.env` to your `.gitignore` file
3. Keep your API tokens secure and never share them publicly

## Setup tools error

1. Setup tools issue is because of python version 3.13 and above. In this case requirements.txt fails
2. If the version is 3.12 or less, you should not be getting set up tools issue. Hence requirements.txt should work. if you downgrade python 3. requirements.txt should work

## Numpy Conflict

1. Latest numpy installation causes conflict with tabpfn because the tabpfn library expects numpy version less than 2. requirements.txt is altered to meet this requirement
2. If the version is 3.12 or less, you should not be getting set up tools issue. Hence requirements.txt should work. if you downgrade python 3. requirements.txt should work

## Alternative Option - create separate virtual environments and use appropriately

1. if still it does not work, If you install the libraries in the following order, you should be execute the code seamlessly

```bash
# Create tabpfn environment by installing the following in order
pip install hyperopt tabpfn-extensions tabpfn
pip install ipykernel pandas matplotlib dotenv  seaborn numpy
```

```bash
# Create chronos environment by installing the following in order
pip install git+https://github.com/amazon-science/chronos-forecasting.git
pip install ipykernel pandas matplotlib dotenv  seaborn numpy
```

```bash
# Create week2 environment by installing the following in order
pip install ipykernel pandas matplotlib dotenv  seaborn numpy
pip install sentence_transformers streamlit
pip install fastapi uvicorn faiss-cpu pypdf2
```

---

Now you have a fully set up development environment with all the required dependencies installed in an isolated virtual environment and your Hugging Face API token securely stored.
