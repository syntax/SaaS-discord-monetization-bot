# SaaS-discord-monetization-bot
Simple discord bot that allows you to monetization usage of your discord server following a SaaS business model. Features a shopify integration for safe payment processing and the associated analytics.

This bot is appropriate for use where membership to a discord community or 'server' is intended in a non-exclusive manner; however I am sure modifications could be made.

Please excuse any poor coding practices, I wrote this application over a year ago and only maintained it for updates discord.py. It is perhaps in need of a rewrite, however in its current state still provides utility that may benefit some, and so I think its fair to leave it open source in its current state.

---
### PRIMARY FUNCTION

The bot allows for a user to create a new subscription, or reminds them to renew a current subscription when approaching the end of the renewal period, afterwhich they are redirected to a Shopify payment gateway to complete the payment, using the Shopify API. Upon a failed renewal, a role which provides further access is removed from their discord account. This same role was given to the user when they started their subscription. A monitor function runs asynchronously and waits for events to occur, reading from a JSON file used as a lacklustre database; this certainly needs rewriting to a real database file, however if you expect only small load, (a few 100 users), this JSON file should suffice albiet inefficient.

Moreover, users who start a subscription are given a license key. This perhaps allows for some expansion of this project and implementation alongside a software application, although in its current state offers no additional purpose.

---
### TO SETUP

- install recent version of python, python3.+
- install python dependencies for this project; asyncio, discord.py
- create a shopify store and an associated private application
- create a discord bot through the discord developer portal
- edit config.json with relevant data from last two steps
- run main.py :)
