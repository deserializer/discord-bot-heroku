# Hosting your repl based discord.py bot on Heroku to keep it running **INDEFINETLY**
[![Run on Repl.it](https://repl.it/badge/github/syntax-corp/discordpy-replit-heroku)](https://repl.it/github/syntax-corp/discordpy-replit-heroku)

### Prerequisites
You must have an account for [Discord](https://discord.com/register), [GitHub](https://github.com/join) , [Heroku](https://signup.heroku.com/), and [Repl.it](https://repl.it/signup) (you probably have an account already).

### 1. Create a bot and get its token
* Create an application in the developer portal [here](https://discordapp.com/developers/applications/)
* Open up your new application and click 'Add Bot' under the Bot settings to create your bot.
* After creating the bot, click the 'Copy' button under the title Token. Take note of your token as you will need it later.

### 2. Clone the GitHub repository and set it up to work with Heroku
* Clone my Github repository into a repl [here](https://repl.it/github/syntax-corp/discordpy-replit-heroku). This contains all the code you need to host your bot on Heroku. You can also view it [here](https://github.com/syntax-corp/discordpy-replit-heroku)
* Link your repl to a GitHub repository
* Create an application for Heroku [here](https://dashboard.heroku.com/new-app).
* Under 'Deploy', do the following:
  * Deployment Method => Connect your GitHub
  * App connected to GitHub => Search for the forked repository
  * Automatic Deploy => Enable Automatic Deploy (to redeploy after every commit)
* Under 'Settings', click on 'Reveal Config Vars' and enter the following:
  * KEY => DISCORD_TOKEN
  * VALUE => (Enter the bot token that you copied from the developer portal)
  * Click the 'Add' button after entering all of this information.
* Under 'Resources', do the following:
  * Click on the 'Pencil' icon.
  * Switch the worker from off to on.
  * Click 'Confirm' to finalize the decision.
  * NOTE: You are given 550 free Dyno hours, which will not last the entire month. However, if you provide a credit card to verify your identity, you are given an additional 450 hours, which will allow your bot to run indefinitely. You will not be charged for this.

### What's next?
* Now you can tweak the main.py file as you please! just don't mess with the first 5 or last 2 lines (you can change the prefix in line 4 though.)

### Original code belongs to audieni. I just made it more suitable for repl.it bot creators. Visit his repository [here](https://github.com/audieni/discord-py-heroku)