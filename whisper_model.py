import whisper
import ctypes
import ctypes.util
import platform




# Function to load whisper model
def load_model(model_name: str = "base"):
    model = whisper.load_model(model_name)
    return model

# Platform-specific libc handling
libc = None
if platform.system() == "Windows":
    libc = ctypes.CDLL(ctypes.util.find_library("msvcrt"))
else:
    libc = ctypes.CDLL(ctypes.util.find_library('c'))

if not libc:
    raise ImportError("Unable to find required C library.")

# Optional: Check if specific functions are available in libc
try:
    # Example: check for specific function
    fallocate = libc.fallocate
except AttributeError:
    fallocate = None


