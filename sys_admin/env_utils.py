import os
import logging

# Optional: configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def get_env(var_name, default=None, log=True):
    value = os.getenv(var_name, default)
    if log:
        logging.info(f"GET: {var_name} = {value}")
    return value

def set_env(var_name, value, log=True):
    os.environ[var_name] = value
    if log:
        logging.info(f"SET: {var_name} = {value}")

def delete_env(var_name, log=True):
    removed = os.environ.pop(var_name, None)
    if log:
        if removed is not None:
            logging.info(f"DEL: {var_name} removed")
        else:
            logging.warning(f"DEL: {var_name} not found")
    return removed is not None

def exists_env(var_name):
    return var_name in os.environ

def main():
    set_env("MY_VAR", "value")
    get_env("MY_VAR")
    delete_env("MY_VAR")

if __name__ == "__main__":
    main()