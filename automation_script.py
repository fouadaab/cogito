import os
from helper import data_source

cwd = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":

    data_object = data_source.Data(cwd)
    df = data_object.read_data()

    print("Successfully Completed Automation Script")
