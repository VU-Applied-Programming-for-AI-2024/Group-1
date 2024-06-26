import sys
import os

# Get the absolute path of the backend directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
print(f"Backend path: {backend_path}")  # Print for debugging

# Add the backend directory to the Python path
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Now you can import genre_x
try:
    import genre_x
    print("Successfully imported genre_x")
except ImportError as e:
    print(f"Error importing genre_x: {e}")

# Use functions or classes from genre_x as needed
# For example:
# genre_x.some_function()
