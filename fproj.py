import json

all_city_data = []
f = open("city_data.json","r")
lines = f.readlines()
for line in lines:
    data = json.loads(line)
    all_city_data.append(data)
f.close()

class city_letter_node:
    def __init__(self, letter):
        self.letter = letter
        self.children = []
        self.info = None

    def insert_city(self,city_name,city_info):
        if city_name == "":
            self.info = city_info
            return
        for child in self.children:
            if child.letter == city_name[0]:
                child.insert_city(city_name[1:],city_info)
                return
        new_child = city_letter_node(city_name[0])
        print("inserting",city_name[0])
        self.children.append(new_child)
        new_child.insert_city(city_name[1:],city_info)

    def get_city_info(self,city_name):
        if city_name == "":
            return self.info
        for child in self.children:
            if child.letter == city_name[0]:
                return child.get_city_info(city_name[1:])
        return None

    def show(self,level=0):
        print(" "*level + self.letter)
        for child in self.children:
            child.show(level+1)