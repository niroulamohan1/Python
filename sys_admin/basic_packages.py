import os

#print("Current user ID:", os.getuid())
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