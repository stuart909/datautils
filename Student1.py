'''
Written by: Stuart Anderson
Copyright: Tobu Pengin, LLC, 2021
'''
data = {'chips': {'price': 1.75}, 'drink': {'price': 2.50}, 'cookie': {'price': 0.65}, 'hotdog': {'price': 3.50}}

'''
def printer(string,args=None):
    if not args:
        if type(args) is list:
            for i in args:
                print(i+'\n')
            else:
                print(string)
    else:
        print(string)
'''
data = {'chips': {'price': 1.75}, 'drink': {'price': 2.50}, 'cookie': {'price': 0.65}, 'hotdog': {'price': 3.50}}

class Data:
    def __init__(self, data):
        self.keys = [i for i in data] if type(data) is dict else None
        self.length = 1 if type(data) is not dict or type(data) is not list else len(data)
        if type(data) is list:
            self.data = [Data(i) for i in data]
        elif type(data) is dict:
            self.data = [Data(data[i]) for i in self.keys]
        else:
            self.data = data


    def index(self, value):
        return [i for i, v in enumerate(self.data) if v == value]

    def __next__(self):
        next(self.data)

    def __iter__(self):
        self.data

    def __call__(self):
        pass


def total(d):
    total = 0
    for i in d.keys():
        total += d[i]['price']*d[i]['qty']
    total += round(total*.0625, 2)
    return total


def get_qty(item):
    def get(item):
        try:
            msg = input('\nHow many %s do you want?' % item)
            if msg == 'q' or msg == 'Q':
                quit()
            else:
                return int(msg)
        except:
            get(item)

    return {'qty': get(item)}


for i in data.keys():
    data[i].update(get_qty(i))

print('Total: '+str(total(data)))
'''
print("**")
print("Hot Dog Stand Sale Bill")

# Output for chips

print(f"Bags of chips @ {chips} each")
print(f"Number={chips1} ")
total_chips = (chipschips1)
print(f"Total Cost ={total_chips}")

# Output for drinks
print(f"Bottles of drink @ {drink} each")
print(f"Number={drinks1} ")
total_drinks = (drinkdrinks1)
print(f"Total Cost ={total_drinks}")

# Output for cookie
print(f"Cookies @ {cookie} each")
print(f"Number={cookie1} ")
total_cookies = (cookiecookie1)
print(f"Total Cost ={total_cookies}")

# Output for hotdog
print(f"Bottles of drink @ {hot_dog} each")
print(f"Number={hot_dog} ")
total_hotdogs = (hot_dog * hot_dog1)
print(f"Total Cost ={total_hotdogs}")

total_cost = (total_chips+total_drinks+total_cookies+total_hotdogs)
print(f"Total = {total_cost}")

total_tax = (total_cost*tax)
print(f"Tax@ {total_tax}")


ammount = int(input("How much do you want to pay?"))

if (ammount > total_tax):
    change = (ammount - total_tax)
    print(f"Your change is {change}")

else:
    short = (total_tax-ammount)
    print(f"You are short by {short}")

print("Thanks - Have a Great Day - Come Again!")'''
