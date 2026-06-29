class FileWriter:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.f = open(self.path, "w")
        return self.f
    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
        return False

with FileWriter("no_file") as fw:
    raise ValueError("No file detected")

