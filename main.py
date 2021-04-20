import discord
from discord.ext import commands
import random
import json
import requests
import string
from datetime import datetime, timedelta
import asyncio

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix='.',intents=intents)

with open('config.json','r') as configfile:
    CONFIG = json.load(configfile)

print(CONFIG)

APIKEY = CONFIG['shopify']['APIKEY']
PASSWORD = CONFIG['shopify']['PASSWORD']
DISCTOKEN = CONFIG['discord']['DISCTOKEN']

shop_url = f"https://%s:%s@{CONFIG['shopify']['MYSHOPIFY_STORE_URL']}" % (APIKEY, PASSWORD) #{CONFIG['company_name']}shop



def generatekey():
    key = 'SYN'
    for i in range(0,25):
        if i%5 ==0:
            key+= '-'
        else:
            key += (str(random.randint(0,9)))
    return key

async def monitor():
    logchannel = client.get_channel(CONFIG["discord"]["IDS"]["LOGCHANNEL_ID"])
    while True:
        await asyncio.sleep(5)
        print('monitoring...')
        with open(f'{CONFIG["dir"]}/maindb.json') as jsonfile:
            jsonform = json.load(jsonfile)
        for value in jsonform["entries"]:
            expire = datetime.strptime(value['expiredate'],"%m/%d/%Y, %H:%M:%S")
            user = client.get_guild(CONFIG["discord"]["IDS"]["GUILD_ID"]).get_member(int(value['discid']))
            print(f'STATS FOR {user} --------------------------')
            print(f'EXPIRE : {datetime.now()} expi res: {expire}, {datetime.now() >= expire}')
            print(f'1DAY : {expire - timedelta(days=1)} now: {datetime.now()}, {(expire - timedelta(minutes=1)) <= datetime.now()}')
            print(f'3DAY : {expire - timedelta(days=3)} now: {datetime.now()}, {(expire - timedelta(minutes=3)) <= datetime.now()}')
            if datetime.now() >= expire:
                try:
                    embed = discord.Embed(title='',
                                        description=f"Hey, {user.mention}. Sadly, you have let your subscription expire...\n\nIf you wish to use {CONFIG['company_name']} again, message me `.subscribe` at any time, but your roles, license key, and access to all the tools available have been revoked.\nSad to see you go :frowning:",
                                        colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await user.send(embed=embed)
                except:
                    try:
                        embed = discord.Embed(title='',
                                            description=f"Hey. Sadly, you have let your subscription expire...\n\nIf you wish to use {CONFIG['company_name']} again, message me `.subscribe` at any time, but your roles, license key, and access to all the tools available have been revoked.\nSad to see you go :frowning:",
                                            colour=0xFFA800)
                        embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                        await user.send(embed=embed)
                    except Exception as e:
                        print(e)
                        embed = discord.Embed(title='',
                                      description=f"""{value["discname"]} has left the server and it seems their subscription has just run out""",
                                      colour=0xFFA800)
                        embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                        await logchannel.send(embed=embed)
                jsonform['entries'].remove(value) #destroy key
                with open(f'{CONFIG["dir"]}/maindb.json', 'w') as jsonfile:
                    json.dump(jsonform, jsonfile)
                try:
                    role = client.get_guild(CONFIG["discord"]["IDS"]["GUILD_ID"]).get_role(CONFIG["discord"]["IDS"]["EXCLUSIVEROLE_ID"])
                    await user.remove_roles(role)
                    embed = discord.Embed(title='',
                                        description=f"{user.mention} just let their subscription run out",
                                        colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await logchannel.send(embed=embed)
                except:
                    pass
            elif (expire - timedelta(days=1)) <= datetime.now():
                if value['1daywarning'] == 'false':
                    embed = discord.Embed(title='',
                                          description=f"**THIS IS AN AUTOMATED 1 DAY WARNING** YOUR KEY WILL EXPIRE SOON! \n\nBe sure to use `.topup` to ensure you dont loose access to {CONFIG['company_name']}, if you do not do this within 1 days time, you will loose access to the discord, the address generators, and all the other tools you have been using here!",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await user.send(embed=embed)
                    embed = discord.Embed(title='',
                                          description=f"`THIS IS YOUR LAST WARNING BEFORE YOUR SUBSCRIPTION EXPIRES`\nIf you do not act on this your key will be destroyed within under 24 hours.\n\nRemember, if your key gets destroyed, you have to resubscribe, costing you more than it would to top up!",
                                          colour=0xfc1c03)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await user.send(embed=embed)
                    value['1daywarning'] = 'true'
                    with open(f'{CONFIG["dir"]}/maindb.json', 'w') as jsonfile:
                        json.dump(jsonform, jsonfile)
                    embed = discord.Embed(title='',
                                          description=f"{user.mention} just recieved their 1day warning",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await logchannel.send(embed=embed)
            elif (expire - timedelta(days=3)) <= datetime.now():
                if value['3daywarning'] == 'false':
                    embed = discord.Embed(title='',
                                          description=f"**THIS IS AN AUTOMATED 3 DAY WARNING** YOUR KEY WILL EXPIRE SOON! \n\nBe sure to use `.topup` to ensure you dont loose access to {CONFIG['company_name']}, if you do not do this within 3 days time, you will loose access to the discord, the address generators, and all the other tools you have been using here!",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await user.send(embed=embed)
                    value['3daywarning'] = 'true'
                    value['amountremainingresettime'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    with open(f'{CONFIG["dir"]}/maindb.json','w') as jsonfile:
                        json.dump(jsonform, jsonfile)

                    embed = discord.Embed(title='',
                                          description=f"{user.mention} just recieved their 3 day warning",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await logchannel.send(embed=embed)


@client.event
async def on_ready():
    print("online")
    game = discord.Game(".helpme for assistance!")
    await client.change_presence(activity=game)
    client.loop.create_task(monitor())

@client.event
async def on_member_join(member):
    embed = discord.Embed(title='',
                          description=f"Hey, {member.mention}, and welcome to {CONFIG['company_name']}\n\nIf you with to become a member of {CONFIG['company_name']} and benefit from the services available, please DM me `.subscribe`",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await member.send(embed=embed)

@client.command()
async def helpme(ctx):
    embed = discord.Embed(title='',
                          description=f"**Here are a list of commands available:**\n\n`.subscribe` - if you are new here, do this and follow the instructions to purchase yourself a subscription.\n`.topup` - allows you to renew your subscription here as to not loose it!\n`.keystatus` - allows you to see information regarding your key and how long it has on it before needing to be renewed.",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await ctx.message.author.send(embed=embed)

@client.command()
async def keystatus(ctx):
    authorid = ctx.message.author.id
    print(authorid)
    with open(f'{CONFIG["dir"]}/maindb.json') as jsonfile:
        jsonform = json.load(jsonfile)
    for value in jsonform['entries']:
        if value['discid'] == str(authorid):
            embed = discord.Embed(title='',
                                  description=f"Hey {ctx.message.author.mention}, here are your key details associated with your email {value['email']}:",
                                  colour=0xFFA800)
            embed.add_field(name="expires", value=f"{value['expiredate']}", inline=True)
            embed.add_field(name="license key", value=f"{value['licensekey']}", inline=True)
            embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
            await ctx.message.author.send(embed=embed)

            def strfdelta(tdelta, fmt):
                d = {"days": tdelta.days}
                d["hours"], rem = divmod(tdelta.seconds, 3600)
                d["minutes"], d["seconds"] = divmod(rem, 60)
                return fmt.format(**d)

            timediff = strfdelta(((datetime.strptime(value['expiredate'],"%m/%d/%Y, %H:%M:%S")) - datetime.now()),"{days} days, {hours} hrs, {minutes} mins and {seconds} seconds!")

            embed = discord.Embed(title='',
                                  description=f"""Your license needs to be renewed (via `.topup`) within {timediff}""",
                                  colour=0xFFA800)
            embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
            await ctx.message.author.send(embed=embed)
            return
    embed = discord.Embed(title='',
                          description=f"""You do not have a license.""",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await ctx.message.author.send(embed=embed)

@client.command()
async def topup(ctx):
    logchannel = client.get_channel(CONFIG["discord"]["IDS"]["LOGCHANNEL_ID"])
    author = ctx.message.author
    with open(f'{CONFIG["dir"]}/maindb.json') as jsonfile:
        jsonform = json.load(jsonfile)
    if str(author.id) not in [value['discid'] for value in jsonform['entries']]:
        embed = discord.Embed(title='',
                              description=f"You dont have a subscription, use `.subscribe` to join {CONFIG['company_name']}!",
                              colour=0xFFA800)
        embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
        await author.send(embed=embed)
        return
    else:
        for value in jsonform['entries']:
            if value['discid'] == str(author.id):
                embed = discord.Embed(title='',
                                      description=f"""**Hey, we have found your account with license *{value['licensekey']}* and email *{value['email']}***\nWould you like me to generate you a checkout link so that you can add another 30 days to your license?\n\nThis will change your current expiry, of: \n`{value['expiredate']}` \nto: \n`{((datetime.strptime(value['expiredate'],"%m/%d/%Y, %H:%M:%S"))+timedelta(days=30)).strftime("%m/%d/%Y, %H:%M:%S")}` """,
                                      colour=0xFFA800)
                embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                await author.send(embed=embed)
                embed = discord.Embed(title='',
                                      description=f"If you would like to proceed, reply to this with `yes`",
                                      colour=0xFFA800)
                embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                await author.send(embed=embed)

                def check(m):
                    return m.author == author and m.guild is None

                yes = await client.wait_for('message', check=check)
                if yes.content.lower() == 'yes':
                    chars = [char for char in string.ascii_lowercase] + [str(num) for num in list(range(0, 10))*2]
                    randnumber = ''.join(random.choice(chars) for i in range(20))
                    if author.name.replace(' ','').isalnum():
                        handle = f"subscription-topup-for-{author.name.replace(' ','-')}-{randnumber}"
                    else:
                        handle = f"subscription-topup-for-a-{CONFIG['company_name']}-user-{randnumber}"
                    payload = {"product": {
                        "title": f"Subscription top-up for {author.name}",
                        "body_html": f"This product is for purchase via the holder of the email <b>{value['email']} only.</b> If you purchase this not under this email, or without access to this email, you will be paying on someone else's behalf and will not be refunded. :)\n\n",
                        "handle": f"{handle}",
                        "variants": [
                            {
                                "price": f"{CONFIG['price']}",
                                "inventory_management": "shopify",
                                "inventory_quantity": "1",
                                "requires_shipping": 'false'
                            }
                        ]
                    }}
                    headers = {'Content-Type': 'application/json'}
                    resp = requests.post(f'{shop_url}/admin/api/2020-04/products.json', json=payload, headers=headers)
                    print(resp, resp.text)
                    productid = resp.json()['product']['id']
                    print(productid)

                    embed = discord.Embed(title='',
                                          description=f"""I have just generated you a unique payment URL, specially for you! **Be sure to pay this with the email __{value['email']}__**, in order for it to sync properly with this request. :slight_smile:\n\n > Your unique URL can be found here:\n > https://{CONFIG['shopify']['DOMAIN']}/products/{handle}""",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await author.send(embed=embed)
                    timetopay = (datetime.now() + timedelta(minutes=10)).strftime('%H:%M:%S')
                    realtimetoopay = datetime.now() + timedelta(minutes=15)
                    embed = discord.Embed(title='',
                                          description=f"Please be prompt about paying this link, as it will expire in 10 minutes time. Moreover, it is recommended that you do not attempt a payment any later than {timetopay}, as there is a risk your payment wont be captured.",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await author.send(embed=embed)
                    payed = False
                    while not payed:
                        if realtimetoopay >= datetime.now():
                            await asyncio.sleep(5)
                            orders = requests.get(f'{shop_url}/admin/api/2020-04/orders.json?status=open').json()
                            for order in orders['orders']:
                                # print(order["email"],order["line_items"][0]["product_id"])
                                if order["email"].lower() == value['email'].lower() and order["line_items"][0]["product_id"] == productid:
                                    embed = discord.Embed(title='',
                                                          description=f"Hey {author.mention}! We have just recieved your payment successfully @ {datetime.now().strftime('%H:%M:%S')}\n\nThank you for continuing to choose {CONFIG['company_name']}, you will receive your `+30 days` shortly",
                                                          colour=0xFFA800)
                                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                                    await author.send(embed=embed)
                                    oldproduct = requests.delete(f'{shop_url}/admin/api/2020-04/products/{productid}.json')
                                    print(oldproduct)
                                    orderid = order['id']
                                    payed = True
                                    break
                        else:
                            oldproduct = requests.delete(f'{shop_url}/admin/api/2020-04/products/{productid}.json')
                            print(f'deleting that product: {oldproduct}')
                            embed = discord.Embed(title='',
                                                  description=f"Hey {author.mention}! Sadly your payment link has expired. Your product will be deleted within the next minute :frowning:",
                                                  colour=0xFFA800)
                            embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                            await author.send(embed=embed)
                            return

                    value['expiredate'] = ((datetime.strptime(value['expiredate'],"%m/%d/%Y, %H:%M:%S") + timedelta(days=30))).strftime("%m/%d/%Y, %H:%M:%S")
                    value['1daywarning'] = 'false'
                    value['3daywarning'] = 'false'
                    with open(f'{CONFIG["dir"]}/maindb.json', 'w') as jsonfile:
                        json.dump(jsonform, jsonfile)
                    embed = discord.Embed(title='',
                                          description=f"Your 30 days top-up has been added to the data base, and your license key ,{value['licensekey']}.\n\nYou can use `.keystatus` to see this affect!",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await author.send(embed=embed)

                    resp = requests.post(f'{shop_url}/admin/api/2020-04/orders/{orderid}/close.json', json={})
                    print(f'closing that order: {resp}')
                    embed = discord.Embed(title='',
                                          description=f"{author.mention} just topped up a subscription using email {value['email']}",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await logchannel.send(embed=embed)
                else:
                    embed = discord.Embed(title='',
                                          description=f"Seeing as you have replied with `{yes.content.lower()}`, this topup process will be terminated",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await author.send(embed=embed)
                    return

@client.command()
async def subscribe(ctx):
    logchannel = client.get_channel(CONFIG["discord"]["IDS"]["LOGCHANNEL_ID"])
    author = ctx.message.author
    with open(f'{CONFIG["dir"]}/maindb.json') as jsonfile:
        jsonform = json.load(jsonfile)
        for value in jsonform['entries']:
            if value['discid'] == str(author.id):
                embed = discord.Embed(title='',
                                      description=f"You already have a subscription, if you want to renew your subscription, use `.topup`",
                                      colour=0xFFA800)
                embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                await author.send(embed=embed)
                return

    embed = discord.Embed(title='',
                          description=f"Hey, {author.mention}\n\nIn order to subscribe, you will need to make a payment to a custom-generated shopify payment site, with a specified email.\n\n**What email do you have access to and will be using to make your transaction today?**",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await author.send(embed=embed)

    def check(m):
        return m.author == author and m.guild is None

    email = await client.wait_for('message', check=check)

    with open(f'{CONFIG["dir"]}/maindb.json') as jsonfile:
        jsonform = json.load(jsonfile)

    if email.content.lower() in [entry['email'].lower() for entry in jsonform['entries']]:
        embed = discord.Embed(title='',
                              description=f"Your email, {email.content} already has an active subscription with us!",
                              colour=0xFFA800)
        embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
        await author.send(embed=embed)

        return


    chars = [char for char in string.ascii_lowercase] + ['0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9']
    randnumber = ''.join(random.choice(chars) for _ in range(20))
    if author.name.replace(' ', '').isalnum():
        handle = f"{CONFIG['company_name']}-subscription-for-{author.name.replace(' ', '-')}-{randnumber}"
    else:
        handle = f"{CONFIG['company_name']}-subscription-for-a-{CONFIG['company_name']}-user-{randnumber}"
    payload = {"product":{
        "title": f"Initial {CONFIG['company_name']} Subscription for {author.name}",
        "body_html" : f"This product is for purchase via the holder of the email <b>{email.content} only.</b> If you purchase this not under this email, or without access to this email, you will be paying on someone else's bahalf and will not be refunded. :)\n\nPlease be aware this gives untapped access to the things that {CONFIG['company_name']} provides, however a small cooldown is enforced in the last days of your subscription being valid to ensure you do not abuse the things {CONFIG['company_name']} offer.\n\nAny questions, feel free to open a ticket!",
        "handle" : f"{handle}",
        "variants":[
            {
                "price":f"{CONFIG['price']}",
                "inventory_management":"shopify",
                "inventory_quantity": "1",
                "requires_shipping": 'false'
            }
        ]
    }}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(f'{shop_url}/admin/api/2020-04/products.json',json=payload,headers=headers)
    productid = resp.json()['product']['id']

    embed = discord.Embed(title='',
                          description=f"I have just generated you a unique payment URL, specially for you! **Be sure to pay this with the email {email.content}**, in order for it to sync properly with this request. :slight_smile:\n\n > Your unique URL can be found here:\n > https://{CONFIG['shopify']['DOMAIN']}/products/{handle}",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await author.send(embed=embed)
    timetopay = (datetime.now() + timedelta(minutes=10)).strftime('%H:%M:%S')
    realtimetoopay = datetime.now() + timedelta(minutes=15)
    embed = discord.Embed(title='',
                          description=f"Please be prompt about paying this link, as it will expire in 10 minutes time. Moreover, it is recommended that you do not attempt a payment any later than {timetopay}, as there is a risk your payment wont be captured.",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await author.send(embed=embed)
    payed = False
    while not payed:
        if realtimetoopay >= datetime.now():
            await asyncio.sleep(5)
            orders = requests.get(f'{shop_url}/admin/api/2020-04/orders.json?status=open').json()
            for order in orders['orders']:
                # print(order["email"],order["line_items"][0]["product_id"])
                if order["email"].lower() == email.content.lower() and order["line_items"][0]["product_id"] == productid:
                    embed = discord.Embed(title='',
                                          description=f"Hey {author.mention}! We have just recieved your payment successfully @ {datetime.now().strftime('%H:%M:%S')}\n\nThank you for choosing {CONFIG['company_name']}, you will receive licensing and roles shortly.",
                                          colour=0xFFA800)
                    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
                    await author.send(embed=embed)
                    oldproduct = requests.delete(f'{shop_url}/admin/api/2020-04/products/{productid}.json')
                    print(oldproduct)
                    orderid = order['id']
                    payed = True
                    break
        else:
            oldproduct = requests.delete(f'{shop_url}/admin/api/2020-04/products/{productid}.json')
            print(f'deleting that product: {oldproduct}')
            embed = discord.Embed(title='',
                                  description=f"Hey {author.mention}! Sadly your payment link has expired. Your product will be deleted within the next minute :frowning:",
                                  colour=0xFFA800)
            embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
            await author.send(embed=embed)
            return

    licensekey = generatekey()

    expires = (datetime.now() + timedelta(days=30)).strftime("%m/%d/%Y, %H:%M:%S")
    with open(f'{CONFIG["dir"]}/maindb.json') as jsonfile:
        jsonform = json.load(jsonfile)
    licenseunique = False
    while not licenseunique:
        licensekey = generatekey()
        if licensekey in [entry['licensekey'] for entry in jsonform['entries']]:
                licenseunique = False
        else:
            licenseunique = True



    jsonform['entries'].append({'discname':f'{author.name}','discid':f'{author.id}','email':f'{email.content.lower()}','licensekey':f'{licensekey}','expiredate':f'{expires}','3daywarning':'false','1daywarning':'false','activated':'true','_comment': 'THESE FOLLOWING ATTRIBUTES ARE IN REGARDS TO THE NEAR TERMINATION COOLDOWN','amountremaining': '50','amountremainingresettime': ''})
    with open(f'{CONFIG["dir"]}/maindb.json','w') as jsondumpfile:
        json.dump(jsonform,jsondumpfile)
    embed = discord.Embed(title='',
                          description=f"You have been successfully added to the database, with the license: \n**{licensekey}**\n and via the email {email.content}",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await author.send(embed=embed)

    resp = requests.post(f'{shop_url}/admin/api/2020-04/orders/{orderid}/close.json',json={})
    print(f'closing that order: {resp}')

    await client.get_guild(CONFIG["discord"]["IDS"]["GUILD_ID"]).get_member(author.id).add_roles(client.get_guild(CONFIG["discord"]["IDS"]["GUILD_ID"]).get_role(CONFIG["discord"]["IDS"]["EXCLUSIVEROLE_ID"]))
    embed = discord.Embed(title='',
                          description=f"You have been successfully given the `member` role",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await author.send(embed=embed)

    embed = discord.Embed(title='',
                          description=f"{author.mention} just started a subscription using email {email.content}",
                          colour=0xFFA800)
    embed.set_footer(text=f"{CONFIG['company_name']} | created by syntax#9999 with love")
    await logchannel.send(embed=embed)

client.run(DISCTOKEN)
