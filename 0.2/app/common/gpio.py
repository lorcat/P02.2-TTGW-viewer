__author__ = 'Konstantin Glazyrin'

try:
    import RPi.GPIO
    from app.common.RPI import GPIOreal as gpio
except RuntimeError:
    print("Error importing the GPIO; make sure you run under root priveleges.")
except ImportError:
    from app.common.RPI import GPIOdummy as gpio

