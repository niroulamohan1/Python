import os

print("Current user ID:", os.getuid())
print("Process ID:", os.getpid())

# Get environment variable
aws_key = os.getenv('AWS_ACCESS_KEY_ID', 'default_key')

# Set environment variable (temporary for current process)
os.environ['DEPLOY_ENV'] = 'production'
value = os.environ.get('DEPLOY_ENV')
try:
  print(f"DEPLOY_ENV = {value}")
  print(f"CI_ENV = {os.environ['CI_ENV']}") #Raises error
except KeyError:
  pass

print("test")

import shutil

try:
    # Example 1: Copy a file
    shutil.copy("example.txt", "backup_example.txt")

    # Example 2: Move a file
    shutil.move("backup_example.txt", "archive/backup_example.txt")

    # Example 3: Copy an entire directory
    shutil.copytree("project_folder", "project_backup")

    # Example 4: Remove a directory tree
    shutil.rmtree("project_backup")

    # Example 5: Create a compressed archive (zip/tar)
    shutil.make_archive("project_archive", "zip", "project_folder")

    print("Shutil operations completed successfully!")
except:
    print("shutil operations failed")

import subprocess

# Example 1: Run a simple command
subprocess.run(["echo", "Hello from subprocess!"])

# Example 2: Capture output of a command
result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
print("Command output:\n", result.stdout)

# Example 3: Run a command with error handling
try:
    subprocess.run(["false"], check=True)
except subprocess.CalledProcessError:
    print("The command failed!")

# Example 4: Open another program (e.g., Notepad on Windows)
# subprocess.run(["notepad.exe"])   # Uncomment if on Windows

try:
    result = subprocess.run(
        ["/usr/local/bin/myapp_start.sh"],
        check=True,
        capture_output=True,
        text=True
    )
    print("✅ Script ran successfully")
    print("Output:", result.stdout)
except subprocess.CalledProcessError as e:
    print("Script failed with exit code", e.returncode)
    print("Error output:", e.stderr)
