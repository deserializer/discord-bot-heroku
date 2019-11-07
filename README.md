# Hosting your discord.py bot on Heroku
### What are the prerequisites for this guide?
You must have an account for Discord [[Link](https://discordapp.com/developers/applications/)], GitHub [[Link](https://github.com/join)] , and Heroku [[Link](https://signup.heroku.com/)].

### How do I create a bot and get a bot token?
* Create an application in the developer portal by clicking [here](https://discordapp.com/developers/applications/)
* Open up your new application and click 'Add Bot' under the Bot settings to create your bot.
* After creating the bot, click the 'Copy' button under the title Token. Take note of your token as you will need it later.

### How to fork the repository and set it up to work with Heroku?
* Fork a copy of this repository by clicking the 'Fork' on the upper right-hand.
* Create an application for Heroku by clicking [here](https://dashboard.heroku.com/new-app).
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
  * NOTE: You are allocated 550 free Dyno hours, which will not last the entire month. However, if you provide a credit card to verify your identity, you are given an additional 450 hours, which will allow your bot to run indefinitely.

# TO-DO LIST
* Revise the tutorial to be easier to understand for any user.
* Add some images for following along with the process.
