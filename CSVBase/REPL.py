from .language import execute
from .database import Database
import os
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory


class WiredReplClient:
    def __init__(self, db):
        self.db = db
        self.hist = FileHistory(os.path.expanduser("~/.csvbase.history"))
        self.buffer = ""
        self.linecount = 0

    def __call__(self):
        while True:
            prompttext = "CSV>  "
            if self.linecount > 0:
                prompttext = "{0}    ".format(self.linecount)
            resp = prompt(prompttext, history=self.hist).strip()
            if resp == "quit":
                break
            if resp[-1] == ";":
                resp = self.buffer + " " + resp
                execute(self, self.db, resp)
                self.buffer = ""
                self.linecount = 0
            else:
                self.buffer += " " + resp
                self.linecount += 1

    def notify(self, result):
        print(result)

    def fail(self, exception):
        print(exception)

def main():
    db = Database()
    client = WiredReplClient(db)
    client()

if __name__ == "__main__":
    main()