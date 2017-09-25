from cx_Freeze import setup, Executable

base = None


executables = [Executable("GUI.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "SerialSnooper",
    options = options,
    version = "1.0",
    description = 'Program that reads the data from an arduino and converts it to keypresses.',
    executables=[Executable("GUI.py"), Executable("SerialSnooper.py")]
)