# Community Creator!

Community Creator is a Discord Bot made specifically for those of you who want to start a community server, but without doing a lot of work. It is simple and easy to setup. 

# Setup

To start the using the bot, install [Python 3.10](https://python.org/downloads/). After installing it, clone this GitHub repository and extract its contents to a folder. Then open a command line window and CD to the current directory (do a Google search if you don't know what I'm talking about). Now once you're in here, run the command
For Windows users:
```
py -m pip install -r requirements.txt
```
For MacOS & Linux users:
```
python -m pip install -r requirements.txt
```
After the command is done, open the `.env` file, inside of it, you'll find something like this:
```
TOKEN = 
MAIN_GUILD = 
OWNER_ID = 
PREFIX = !
```

`TOKEN`: This is the token for the Discord Bot, you'll be generating this in a minute.
`MAIN_GUILD`: This is the ID for the main Discord Server.
`OWNER_ID`: This is the ID for the owner of the bot
`PREFIX`: This is the prefix that will be used for [Jishaku](https://github.com/Gorialis/jishaku/) commands.

To get the `TOKEN` for the Discord Bot, head on over to the [Discord Develop Portal](https://discord.com/developers/applications). Once you're there, follow the gif below:
![alt text](https://imgur.com/sduWAks)
After copying the token, put it in the `.env` file like this:
```
TOKEN = TokenHere
```

For Windows users:
```
py main.py
```
For MacOS & Linux users:
```
python main.py
```
