import discord
from cities import get_city, print_city
import csv
import cities
import sys




commands = []
__cities__ = []
__usstates__ = {}
__countries__ = {}



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        global commands
        
        if message.author.id == self.user.id:
            return
        commands.append(message.content)

        if message.content.startswith('hello'):
            await message.channel.send('Hello {0.author.mention}'.format(message))
            await message.channel.send('Dans quel langage avez-vous besoin d\'aide ?')
        
        if message.content.startswith('help'):
            await message.channel.send('Je vais essayer de vous aider {0.author.mention}'.format(message))
            await message.channel.send('Tapez history pour avoir l\'historique de vos messages')
            await message.channel.send('Tapez reset pour redemarrer la conversation')
            await message.channel.send('Tapez back pour faire un retour arrière à la dernière question posée')

        if message.content.startswith('reset'):
            await message.channel.send('Reset effectué')
            commands = []
        
        if message.content.startswith('history'):
            await message.channel.send('Voici l\'historique')
            for s in commands :
                await message.channel.send(s)
        
        if message.content.startswith('back'):
            commands.pop()
            s = commands.pop()
            await message.channel.send('Dernière commande ' + s + ' enlevée')
        
        if message.content.startswith('JavaScript') or  message.content.startswith('JS'):
            await message.channel.send('Voici un lien pour vous aider en JavaScript :(https://openclassrooms.com/fr/courses/6175841-apprenez-a-programmer-avec-javascript)')
        
        if message.content.startswith('Python') or  message.content.startswith('python'):
            await message.channel.send('Voici un lien pour vous aider en Python :(https://openclassrooms.com/fr/courses/7168871-apprenez-les-bases-du-langage-python)')
        
        if message.content.startswith('Ville') or message.content.startswith('ville') :
            for s in __cities__ :
                if s.name == message.content[6:] :           
                    await message.channel.send(s.country)
                    await message.channel.send('Population:' + str(s.population))

class City:
    def __init__(self, name, countrycode, population, latitude, longitude):
        temp = name.encode(sys.stdout.encoding, 'ignore')
        self.name = temp.decode(sys.stdout.encoding)
        self.countrycode = countrycode
        self.country = __countries__[countrycode.upper()]
        self.population = int(population)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

def __init__():
    global __cities__
    global __usstates__
    global __countries__
    with open('countrycodes.csv', 'r') as countryfile:
        csvreader = csv.reader(countryfile, delimiter=',')
        for row in csvreader:
            __countries__[row[4]] = row[7]

    with open('cities.txt', 'r', encoding='utf-8') as cityfile:
        csvreader = csv.reader(cityfile, delimiter='\t')
        next(csvreader)
        for row in csvreader:
            new_city = City(row[2], row[8], row[14], row[4], row[5])
            if new_city.country == 'United States':
                new_city.us_state = row[10]
            __cities__.append(new_city)

    with open('usstates.csv', 'r') as statesfile:
        csvreader = csv.reader(statesfile, delimiter=',')
        for row in csvreader:
            __usstates__[row[1]] = row[0]

    __cities__.sort(key=lambda city: city.population, reverse=True)

__init__()

            
client = MyClient()
client.run('OTgxMTU4NjI0OTU1MDc2Njcw.GgC-CO.WdVcwUXEDS07CrHm0iz4cWDjZ0c_mpK_DujdAQ')