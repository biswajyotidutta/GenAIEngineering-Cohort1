# Running FastAPI and Streamlit Services

This guide provides commands to start a FastAPI service and run a Streamlit application.

## Starting a FastAPI Service

FastAPI is a modern, high-performance web framework for building APIs. It's typically run with Uvicorn:

```bash
# Make sure you are in your activated virtual environment

# Basic run command
uvicorn main:app --reload

# With custom host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# If your FastAPI app is in a different file or uses a different variable
uvicorn your_file:your_app_variable --reload

# Running in production mode (without reload)
uvicorn main:app --workers 4
```

## Running a Streamlit Application

Streamlit is an open-source Python library that makes it easy to create web apps:

```bash
# Make sure you are in your activated virtual environment

# Basic command to run a Streamlit app
streamlit run app.py

# With custom server port
streamlit run app.py --server.port 8501

# With custom server address
streamlit run app.py --server.address 0.0.0.0

# Running with custom theme
streamlit run app.py --theme.primaryColor "#F63366"

# Running without opening browser automatically
streamlit run app.py --server.headless true
```

## Running Both Services Together

You may need to run both the FastAPI and Streamlit app concurrently. Here are some options:

### Using Multiple Terminal Windows

The simplest approach is to use separate terminal windows:

1. Terminal 1: Start your FastAPI service
2. Terminal 2: Start your Streamlit app

### Running Services in Background

#### Linux/macOS

You can run processes in the background using the `&` operator:

```bash
# Start FastAPI in the background
uvicorn main:app --reload &
# Note the process ID (PID) that is displayed

# Start Streamlit in the background
streamlit run app.py &
# Note the process ID (PID) that is displayed
```

To bring a background process to the foreground:

```bash
# Replace 1234 with the actual PID
fg %1234
```

#### Windows

You can use the `start` command to run processes in a new window:

```bash
# Start FastAPI in a new window
start cmd /k "uvicorn main:app --reload"

# Start Streamlit in a new window
start cmd /k "streamlit run app.py"
```

### Using nohup (Linux/macOS)

For keeping processes running even after closing the terminal:

```bash
# Run FastAPI with nohup
nohup uvicorn main:app --reload > fastapi.log 2>&1 &

# Run Streamlit with nohup
nohup streamlit run app.py > streamlit.log 2>&1 &
```

## Checking if Services are Running

### Checking Process Status

#### Linux/macOS

```bash
# List all Python processes
ps aux | grep python

# Find specific processes
ps aux | grep uvicorn
ps aux | grep streamlit

# Get the status of a specific process by PID
ps -p 1234 # Replace 1234 with the actual PID
```

#### Windows

```bash
# List all running processes
tasklist | findstr python

# Find specific processes
tasklist | findstr uvicorn
tasklist | findstr streamlit
```

### Checking Network Services

Check if services are listening on their expected ports:

```bash
# Linux/macOS
netstat -tuln | grep 8000  # For FastAPI default port
netstat -tuln | grep 8501  # For Streamlit default port

# Windows
netstat -an | findstr 8000  # For FastAPI default port
netstat -an | findstr 8501  # For Streamlit default port
```

### Testing Service Availability

```bash
# Test FastAPI (Linux/macOS/Windows)
curl http://localhost:8000

# Open in browser
# FastAPI: http://localhost:8000
# FastAPI Docs: http://localhost:8000/docs
# Streamlit: http://localhost:8501
```

## Accessing Your Services

Once running, you can access your services at:

- API service: http://localhost:5000 (Flask) or http://localhost:8000 (FastAPI)
- Streamlit app: http://localhost:8501

## Stopping the Services

### Stopping Foreground Processes

- For terminal processes running in the foreground: Press `Ctrl+C` in the respective terminal

### Stopping Background Processes

#### Linux/macOS

```bash
# Kill process by PID
kill 1234  # Replace 1234 with the actual PID

# Kill process more forcefully if needed
kill -9 1234  # Replace 1234 with the actual PID

# Kill all uvicorn processes
pkill -f uvicorn

# Kill all streamlit processes
pkill -f streamlit
```

#### Windows

```bash
# Kill process by PID
taskkill /PID 1234  # Replace 1234 with the actual PID

# Kill process forcefully
taskkill /F /PID 1234  # Replace 1234 with the actual PID

# Kill by process name
taskkill /IM uvicorn.exe
taskkill /IM streamlit.exe
```

### Verifying Services Are Stopped

After stopping a service, you can verify it's no longer running using the same commands from the "Checking if Services are Running" section:

```bash
# Linux/macOS
ps aux | grep uvicorn
ps aux | grep streamlit

# Windows
tasklist | findstr uvicorn
tasklist | findstr streamlit
```

## Git Commands

Git is a distributed version control system for tracking changes in source code during software development.

### Setting Up Git

```bash
# Configure user information
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize a new Git repository
git init

# Clone an existing repository
git clone https://github.com/username/repository.git

# Clone a specific branch
git clone -b branch-name https://github.com/username/repository.git
```

### Basic Git Workflow

```bash
# Check status of the repository
git status

# Add files to staging area
git add filename.py          # Add a specific file
git add .                    # Add all files in the current directory
git add -A                   # Add all files in the repository

# Commit changes
git commit -m "Commit message"

# Commit with both add and commit for tracked files
git commit -am "Commit message"
```

### Working with Branches

```bash
# List all branches
git branch                   # Local branches
git branch -r                # Remote branches
git branch -a                # All branches (local and remote)

# Create a new branch
git branch branch-name

# Switch to a branch
git checkout branch-name

# Create and switch to a new branch
git checkout -b branch-name

# Rename a branch
git branch -m old-name new-name

# Delete a branch
git branch -d branch-name    # Safe delete (prevents deletion of unmerged branches)
git branch -D branch-name    # Force delete

# Merge a branch into the current branch
git merge branch-name
```

### Working with Remotes

```bash
# List remote repositories
git remote -v

# Add a remote repository
git remote add origin https://github.com/username/repository.git

# Change remote URL
git remote set-url origin https://github.com/username/new-repository.git

# Remove a remote
git remote remove origin

# Fetch changes from remote
git fetch origin
git fetch --all              # Fetch from all remotes

# Pull changes (fetch + merge)
git pull origin branch-name
git pull                     # Pull from current branch tracking remote

# Push changes to remote
git push origin branch-name
git push -u origin branch-name   # Push and set upstream
git push                     # Push to current branch tracking remote
git push --force             # Force push (use with caution)
```

### Viewing History & Changes

```bash
# View commit history
git log
git log --oneline            # Compact view
git log --graph              # Show branching graph
git log -n 5                 # Show only last 5 commits
git log --author="username"  # Filter by author

# View changes
git diff                     # Unstaged changes
git diff --staged            # Staged changes
git diff branch1 branch2     # Differences between branches
git diff commit1 commit2     # Differences between commits

# Show changes in a commit
git show commit-hash
```

### Stashing Changes

```bash
# Save changes temporarily
git stash

# Save with a message
git stash save "Work in progress"

# List stashes
git stash list

# Apply and keep the most recent stash
git stash apply

# Apply and drop the most recent stash
git stash pop

# Apply a specific stash
git stash apply stash@{n}

# Remove all stashed changes
git stash clear
```

### Undoing Changes

```bash
# Discard changes in working directory
git checkout -- filename
git restore filename          # Git 2.23+

# Unstage files
git reset filename
git restore --staged filename # Git 2.23+

# Reset to a previous commit
git reset commit-hash         # Keeps changes in working directory
git reset --soft commit-hash  # Keeps changes staged
git reset --hard commit-hash  # Discards all changes (use with caution)

# Revert a commit (creates a new commit that undoes changes)
git revert commit-hash
```

### Advanced Git Commands

```bash
# Interactive rebase for editing commit history
git rebase -i HEAD~3          # Rebase last 3 commits

# Cherry-pick commits from another branch
git cherry-pick commit-hash

# Create and apply patches
git format-patch -1 commit-hash
git apply patch-file.patch

# Clean untracked files
git clean -n                  # Dry run (show what would be removed)
git clean -f                  # Force removal
git clean -fd                 # Remove directories too

# Blame (see who changed each line)
git blame filename

# Find which commit introduced a line/pattern
git log -S "search pattern" filename
git log -p -S "search pattern" # Show patches too

# Create a tag
git tag tag-name
git tag -a tag-name -m "Tag message"  # Annotated tag

# Push tags to remote
git push origin tag-name
git push --tags                # Push all tags
```

### Git Workflows with Remote Repositories

```bash
# Fetch and rebase (alternative to pull)
git fetch origin
git rebase origin/main

# Force push with lease (safer than force push)
git push --force-with-lease

# Sync a fork with original repository
git remote add upstream https://github.com/original/repository.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```
