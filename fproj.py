import json
from flask import Flask, render_template, request


class city_letter_node:
    def __init__(self, letter):
        self.letter = letter
        self.children = {}
        self.info = None

    def insert_city(self, city_name, city_info):
        if city_name=='':
            self.info = city_info
            return
        letter = city_name[0]
        if letter not in self.children:
            self.children[letter] = city_letter_node(letter)
        self.children[letter].insert_city(city_name[1:], city_info)

    def get_city_info(self, city_name):
        if city_name=='':
            return self.info
        letter = city_name[0]
        if letter not in self.children:
            return None
        return self.children[letter].get_city_info(city_name[1:])

    def get_city_info_by_prefix(self, prefix):
        if prefix=='':
            return self.get_all_city_info()
        letter = prefix[0]
        if letter not in self.children:
            return []
        return self.children[letter].get_city_info_by_prefix(prefix[1:])

    def get_all_city_info(self):
        if self.info is not None:
            return [self.info]
        res = []
        for child in self.children.values():
            res.extend(child.get_all_city_info())
        return res

    def show(self,level=0):
        print("-"*level + self.letter)
        for child in self.children.values():
            child.show(level+1)

all_city_data = []
f = open("city_data.json","r")
lines = f.readlines()
for line in lines:
    data = json.loads(line)
    all_city_data.append(data)
f.close()

top_node = city_letter_node("")

for city in all_city_data:
    try:
        city_name = city['businesses'][0]['location']['city']
        city_name = city_name.lower()
        city_name = city_name.replace(" ","")
        top_node.insert_city(city_name, city)
    except:
        pass

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST','GET'])
def search():
    try:
        old_city_name = request.form['city']
        city_name = old_city_name.lower()
        city_name = city_name.replace(" ","")
        city_info = top_node.get_city_info(city_name)
    except:
        return render_template('form.html',search = True)
    if city_info is None:
        return render_template('form.html', message='Restaurant not found')
    else:
        display_address = ''
        for address in city_info['businesses'][0]['location']['display_address']:
            display_address += (address + ' ')
        res_name = city_info['businesses'][0]['name']
        res_url = city_info['businesses'][0]['url']
        res_phone = city_info['businesses'][0]['display_phone']
        
        return render_template('form.html', message="Most hot restaurant in "+old_city_name,city_info=city_info,address=display_address \
            ,name=res_name, url=res_url,phone = res_phone,search=True)

@app.route('/recommend')
def recommend():
    all = top_node.get_all_city_info()
    all_res = [{'name':ele['businesses'][0]['name'],'city':ele['businesses'][0]['location']['city']}for ele in all[0:5]]
    return render_template('rec.html',restaurants=all_res)

@app.route('/detail/<city>')
def detail(city):
    city_info = top_node.get_city_info(city.lower().replace(" ",""))
    display_address = ''
    for address in city_info['businesses'][0]['location']['display_address']:
        display_address += (address + ' ')
    res_name = city_info['businesses'][0]['name']
    res_url = city_info['businesses'][0]['url']
    res_phone = city_info['businesses'][0]['display_phone']
    return render_template('form.html',city_info=city_info,address=display_address \
        ,name=res_name, url=res_url,phone = res_phone,search=False)

@app.route('/cities')
def cities():
    all = top_node.get_all_city_info()
    all_city = [{'name':ele['businesses'][0]['location']['city']}for ele in all]
    return render_template('cities.html',cities=all_city)

@app.route('/search_by_prefix', methods=['POST','GET'])
def search_by_prefix():
    try:
        old_city_name = request.form['city']
        city_name = old_city_name.lower()
        city_name = city_name.replace(" ","")
        city_info = top_node.get_city_info_by_prefix(city_name)
    except:
        return render_template('form.html',search = True)
    if city_info is None:
        return render_template('form.html', message='Restaurant not found')
    else:
        all_city = [{'name':ele['businesses'][0]['location']['city']}for ele in city_info]
        return render_template('cities.html',cities=all_city)

app.run(debug=True)




# city_name = input("Enter a city name that you want to search for a restaurant: ")
# restaurant_info = top_node.get_city_info(city_name.lower().replace(" ",""))
# if restaurant_info is None:
#     print("Sorry, we don't have any restaurant information for this city.")
# else:
#     print("Here are the most hot restaurant for this city:")
#     display_address = ''
#     for address in restaurant_info['businesses'][0]['location']['display_address']:
#         display_address += (address + ' ')
#     print("Location: " + display_address)