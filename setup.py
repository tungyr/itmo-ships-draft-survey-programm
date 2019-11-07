from cx_Freeze import setup, Executable
setup(
    name = "intro",
    version = "1.0",
    description = "Download Blog",
    executables = [Executable("intro.py")]
)