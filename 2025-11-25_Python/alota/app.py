import helpers.module1 as module1
from icecream import ic
import json

if __name__ == '__main__':
    
    # ic(module1.stringCounter('hello world'))

    # x = '{ "name":"John", "age":30, "city":"New York" }'

    # y = json.loads(x)

    # ic(y["age"])

    # # a Python object (dict):
    # x = {
    #     "name": "John",
    #     "age": 30,
    #     "city": "New York"
    # }

    # # convert into JSON:
    # y = json.dumps(x)

    # # the result is a JSON string:
    # ic(y)

    # f = open("../Readme.md")
    # print(f.read())

    with open("demofile.txt", "a") as f:
        f.write("Now the file has more content!")
    #open and read the file after the appending:
    with open("demofile.txt") as f:
        print(f.read())