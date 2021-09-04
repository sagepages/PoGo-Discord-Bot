# PoGo Discord Bot

This repository is for a Pokemon Go Discord bot that takes a users pokemon and IV combination as input to compare against all other combinations at their highest potential and determine their placement. Included is a Jupyter notebook that explains the concept and formulas used to derive a specified pokemons rank for each competetive league.  **I take no credit for the discovery of these formulas. A more in depth description and respective credits can be found on [gamepress.gg](https://gamepress.gg/pokemongo/pokemon-stats-advanced).**

# Using this repository

To use this repository:
    - You can use the `git clone` command to clone to local machine
    - [Create](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications) a discord bot and authenticate it on your server
    - In `config.json` replace `INSERT_BOT_TOKEN` with your personal bot token
    
# To run    
 
 Before running the bot you need to open your terminal of choice and run this command:   ``` pip install -r requirements.txt ```

 Then you can run ``` python Bot.py``` to start the bot

# Built with

- [Python 3.9](https://www.python.org/)