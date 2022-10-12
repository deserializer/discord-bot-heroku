# Starting on Nov. 28, 2022, free Heroku dynos will no longer be available. This guide will still be relevant, but hosting your bot through Heroku will be a paid service.

## Prerequisites
Create accounts for the following:
* Discord: [https://discord.com/developers/applications/](https://discord.com/developers/applications/)
* GitHub: [https://github.com/join](https://github.com/join)
* Heroku: [https://signup.heroku.com/](https://signup.heroku.com/)

## Creating a Discord application and bot
Discord Developer Portal: [https://discord.com/developers/applications/](https://discord.com/developers/applications/)
* Create a new developer application using the '**New Application**' button.
* Open up your application and create your bot using the '**Add Bot**' button under the Bot settings.
* Make sure to use the '**Copy**' button under Token to copy your bot token. Take note of your token as you will need it to connect to your bot.

## Forking the repository and setting up Heroku
* Fork a copy of this repository using the '**Fork**' button on GitHub.
* Create a Heroku application: [https://dashboard.heroku.com/new-app?org=personal-apps](https://dashboard.heroku.com/new-app?org=personal-apps)
* Navigate to the '**Deploy**' section and do the following:
  * Under Deployment method, connect your GitHub account to Heroku.
  * Use the search field to search for the forked repository to connect to your Heroku application.
  * You can '**Enable Automatic Deploys**' to automatically redeploy the application after every commit on GitHub.

## Connecting your bot to Discord
* Navigate to the '**Settings**' section and do the following:
  * Under Config Vars, '**Reveal Config Vars**' to reveal KEY and VALUE and enter the following:
    * **KEY:** DISCORD_TOKEN
    * **VALUE:** *(Enter the bot token copied from the Discord Developer Portal)*
    * '**Add**' your bot token to Config Vars.
* Navigate to the '**Resources**' section and do the following:
  * Switch on your worker by using the 'Pencil' icon and confirming your decision.
  * ~Note: You are given 550 free Dyno hours, which will not span the entire month; however, if you provide a credit card to verify your identity, you are given an additional 450 Dyno hours, which will allow your bot to run 24/7.~ This will no longer be applicable as of Nov. 28, 2022.
