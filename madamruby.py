#!/usr/bin/env python

import os
import sys
import re
import random
from subprocess import Popen, PIPE
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

HANDEY = ["I can imagine a world of love, peace, and no wars. Then I imagine myself attacking that place because they would never expect it.",
"I guess we were kinda poor when we were kids, but we didn't know it. That's because my dad always refused to let us look at the family's financial records.",
"Maybe in order to understand mankind, we have to look at the word itself. Basically, it's made up of two separate words: \"mank\" and \"ind.\" What do these words mean? It's a mystery, and that's why so is mankind.",
"It takes a big man to cry, but it takes a bigger man to laugh at that man.",
"If trees could scream, would we be so cavalier about cutting them down? We might, if they screamed all the time, for no good reason.",
"One thing kids like is to be tricked. For instance, I was going to take my nephew to Disneyland, but instead I drove him to an old burned-out warehouse. \"Oh no,\" I said, \"Disneyland burned down.\" He cried and cried, but I think that deep down he thought it was a pretty good joke. I started to drive over to the real Disneyland, but it was getting pretty late.",
"When I found the skull in the woods, the first thing I did was call the police. But then I got curious about it. I picked it up, and started wondering who this person was, and why he had deer horns.",
"If a kid asks where rain comes from, I think a cute thing to tell him is, \"God is crying.\" And if he asks why God is crying, another cute thing to tell him is, \"Probably because of something you did.\"",
"If you ever fall off the Sears Tower, just go real limp, because maybe you'll look like a dummy and people will try to catch you because, hey, free dummy.",
"When I was a kid my favorite relative was Uncle Caveman. After school we'd all go play in his cave, and every once in a while he would eat one of us. It wasn't until later that I found out that Uncle Caveman was a bear.",
"Anytime I see something screech across a room and latch onto someone's neck, and the guy screams and tries to get it off, I have to laugh, because what is that thing.",
"To me, it's always a good idea to always carry two sacks of something when you walk around. That way, if anybody says, \"Hey, can you give me a hand?,\" you can say, \"Sorry, got these sacks.\"",
"To me, clowns aren't funny. In fact, they're kinda scary. I've wondered where this started and I think it goes back to the time I went to the circus and a clown killed my dad.",
"If you're in a war, instead of throwing a hand grenade at the enemy, throw one of those small pumpkins. Maybe it'll make everyone think how stupid war is, and while they are thinking, you can throw a real grenade at them.",
"Dad always thought laughter was the best medicine, which I guess is why several of us died of tuberculosis.",
"If you want to be the popular one at a party, here's a good thing to do: Go up to some people who are talking and laughing and say, \"Well, technically that's illegal.\" It might fit in with what somebody just said. And even if it doesn't, so what, I hate this stupid party.",
"When you die, if you get a choice between going to regular heaven or pie heaven, choose pie heaven. It might be a trick, but if it's not, mmmmmmm, boy.",
"I think a good product would be \"Baby Duck Hat.\" It's a fake baby duck, which you strap on top of your head. Then you go swimming underwater until you find a mommy duck and her babies, and you join them. Then all of the sudden, you stand up out of the water and roar like Godzilla. Man those ducks really take off! Also Baby Duck Hat is good for parties.",
"If you ever drop your keys into a river of molten lava, let'em go, because, man, they're gone.",
"I bet a funny thing about driving a car off a cliff is, while you're in midair, you still hit those brakes! Hey, better try the emergency brake!",
"It makes me mad when people say I turned and ran like a scared rabbit. Maybe it was like an angry rabbit, who was going to fight in another fight, away from the first fight.",
"If I ever get real rich, I hope I'm not real mean to poor people, like I am now.",
"If I lived back in the wild west days, instead of carrying a six-gun in my holster, I'd carry a soldering iron. That way, if some smart-aleck cowboy said something like \"Hey, look. He's carrying a soldering iron!\" and started laughing, and everybody else started laughing, I could just say, \"That's right, it's a soldering iron. The soldering iron of justice.\" Then everybody would get real quiet and ashamed, because they had made fun of the soldering iron of justice, and I could probably hit them up for a free drink.",
"How come the dove gets to be the peace symbol? How about the pillow? It has more feathers than the dove, and it doesn't have that dangerous beak.",
"Laurie got offended that I used the word \"puke.\" But to me, that's what her dinner tasted like.",
"I hope that someday we will be able to put away our fears and prejudices and just laugh at people.",
"Broken promises don't upset me. I just think, why did they believe me?",
"I hope that after I die, people will say of me: \"That guy sure owed me a lot of money.\"",
"I believe in making the world safe for our children, but not our children's children, because I don't think children should be having sex.",
"Instead of a trap door, what about a trap window? The guy looks out it, and if he leans too far, he falls out. Wait. I guess that's like a regular window.",
"Is there anything more beautiful than a beautiful, beautiful flamingo, flying across in front of a beautiful sunset? And he's carrying a beautiful rose in his beak, and also he's carrying a very beautiful painting with his feet. And also, you're drunk.",
"Once while walking through the mall a guy came up to me and said, \"Hey, how's it going?\" So I grabbed his arm and twisted it up behind his head and said 'Now who's asking the questions?'",
"If I was the head of a country that lost a war, and I had to sign a peace treaty, just as I was signing, I'd glance over the treaty and then suddenly act surprised. \"Wait a minute! I thought we won!\"",
"Sometimes I think I'd be better off dead. No, wait, not me, you.",
"We used to laugh at Grandpa when he'd head off and go fishing. But we wouldn't be laughing that evening when he'd come back with some whore he picked up in town.",
"If you think a weakness can be turned into a strength, I hate to tell you this, but that's another weakness.",
"Instead of trying to build newer and bigger weapons of destruction, we should be thinking about getting more use out of the ones we already have.",
"I wish I had a dollar for every time I spent a dollar, because then, yahoo!, I'd have all my money back.",
"Whenever I see an old lady slip and fall on a wet sidewalk, my first instinct is to laugh. But then I think, what if I was an ant and she fell on me. Then it wouldn't seem quite so funny.",
"If you define cowardice as running away at the first sign of danger, screaming and tripping and begging for mercy, then yes, Mr. Brave man, I guess I'm a coward.",
"Why do the caterpillar and the ant have to be enemies? One eats leaves, and the other eats caterpillars. Oh, I see now.",
"If you go parachuting, and your parachute doesn't open, and you friends are all watching you fall, I think a funny gag would be to pretend you were swimming.",
"If you go through a lot of hammers each month, I don't think it necessarily means you're a hard worker. It may just mean that you have a lot to learn about proper hammer maintenance.",
"During the Middle Ages, probably one of the biggest mistakes was not putting on your armor because you were \"just going down to the corner.\"",
"I hope if dogs ever take over the world and they choose a king, they don't just go by size, because I bet there are some Chihuahuas with some good ideas.",
"I'd like to see a nature film where an eagle swoops down and pulls a fish out of a lake, and then maybe he's flying along, low to the ground, and the fish pulls a worm out of the ground. Now that's a documentary!",
"One thing a computer can do that most humans can't is be sealed up in a cardboard box and sit in a warehouse.",
"Somebody told me how frightening it was how much topsoil we are losing each year, but I told that story around the campfire and nobody got scared.",
"Consider the daffodil. And while you're doing that, I'll be over here, looking through your stuff.",
"I think there should be something in science called the \"reindeer effect.\" I don't know what it would be, but I think it'd be good to hear someone say, \"Gentlemen, what we have here is a terrifying example of the reindeer effect.\"",
"The face of a child can say it all, especially the mouth part of the face.",
"Love can sweep you off your feet and carry you along in a way you've never known before. But the ride always ends, and you end up feeling lonely and bitter. Wait. It's not love I'm describing. I'm thinking of a monorail.",
"I hope they never find out that lightning has a lot of vitamins in it, because do you hide from it or not?",
"One thing vampire children have to be taught early on is, don't run with a wooden stake.",
"I can't stand cheap people. It makes me real mad when someone says something like, \"Hey, when are you going to pay me that $100 you owe me?\" or \"Do you have that $50 you borrowed?\" Man, quit being so cheap!",
"We like to praise birds for flying. But how much of it is actually flying, and how much of it is just sort of coasting from the previous flap?",
"Contrary to what most people say, the most dangerous animal in the world is not the lion or the tiger or even the elephant. It's a shark riding on an elephant's back, just trampling and eating everything they see.",
"To me, boxing is like a ballet, except there's no music, no choreography and the dancers hit each other.",
"You know what would make a good story? Something about a clown who make people happy, but inside he's real sad. Also, he has severe diarrhea.",
"Many people never stop to realize that a tree is a living thing, not that different from a tall, leafy dog that has roots and is very quiet.",
"Sometimes I think you have to march right in and demand your rights, even if you don't know what your rights are, or who the person is you're talking to. Then on the way out, slam the door.",
"For mad scientists who keep brains in jars, here's a tip: Why not add a slice of lemon to each jar, for freshness.",
"Once when I was in Hawaii, on the island of Kauai, I met a mysterious old stranger. He said he was about to die and wanted to tell someone about the treasure. I said, \"Okay, as long as it's not a long story. Some of us have a plane to catch, you know.\" He told us about his life and all, and I thought: \"This story isn't too long.\" But then, he kept going, and I started thinking, \"Uh-oh, this story is getting long.\" But then the story was over, and I said to myself: \"You know, that story wasn't too long after all.\" I forget what the story was about, but there was a good movie on the plane. It was a little long, though.",
"Something tells me that the first mousetrap wasn't designed to catch mice at all, but to protect little cheese \"gems\" from burglars.",
"I guess I kinda lost control, because in the middle of the play I ran up and lit the evil puppet villain on fire. No, I didn't. Just kidding. I just said that to help illustrate one of the human emotions, which is freaking out. Another emotion is greed, as when you kill someone for money, or something like that. Another emotion is generosity, as when you pay someone double what he paid for his stupid puppet.",
"I think somebody should come up with a way to breed a very large shrimp. That way, you could ride him, then after you camped at night, you could eat him. How about it, science?",
"I guess we were all guilty, in a way. We all shot him, we all skinned him, and we all got a complimentary bumper sticker that said, \"I helped skin Bob.\"",
"If you get invited to your first orgy, don't just show up nude. That's a common mistake. You have to let nudity \"happen.\"",
"Probably the earliest fly swatters were nothing more than some sort of striking surface attached to the end of a long stick.",
"If you ever reach total enlightenment while you're drinking a beer, I bet it makes beer shoot out your nose.",
"I wish I had a Kryptonite cross, because then you could keep both Dracula AND Superman away.",
"Whenever you read a good book, it's like the author is right there, in the room talking to you, which is why I don't like to read good books.",
"You know something that would really make me applaud? A guy gets stuck in quicksand, then sinks, then suddenly comes shooting out, riding on water skis! How do they do that?!",
"I wouldn't be surprised if someday some fishermen caught a big shark and cut it open, and there inside was a whole person. Then they cut the person open, and in him is a little baby shark. And in the baby shark there isn't a person, because it would be too small. But there's a little doll or something, like a Johnny Combat little toy guy---something like that.",
"A man doesn't automatically get my respect. He has to get down in the dirt and beg for it.",
"Of all the tall tales, I think my favorite is the one about Eli Whitney and the interchangeable parts.",
"When I think back on all the blessings I have been given in my life, I can't think of a single one, unless you count that rattlesnake that granted me all those wishes.",
"I can see why it would be prohibited to throw most things off the Empire State Building, but what's wrong with little bits of cheese?  They would probably break down into their various gases before they even hit.",
"Before you criticize someone, you should walk a mile in their shoes. That way when you criticize them, you are a mile away from them and you have their shoes."]

PEEWEE = ["There's a lotta things about me you don't know anything about, Dottie. Things you wouldn't understand. Things you couldn't understand. Things you shouldn't understand.",
"You don't wanna get mixed up with a guy like me. I'm a loner, Dottie. A rebel.",
"Everyone I know has a big \"But\". C'mon, Simone, let's talk about *your* big \"But\"",
"I remember... the Alamo.",
"Is this something you can share with the rest of us, Amazing Larry?",
"I bought this pen exactly one hour before my bike was stolen. Why? What's the significance? I DON'T KNOW!",
"Well, I lost my temper and I took a knife and I uh-- Do you know those \"Do Not Remove Under the Penalty of Law\" labels they put on mattresses? Well, I CUT one of them off!",
"On this very night, ten years ago, along this same stretch of road in a dense fog just like this, I saw the worst accident I ever seen. There was this sound, like a garbage truck dropped off the Empire State Building... And when they finally pulled the driver's body from the twisted, burning wreck...it looked like THIS!!",
"There's no basement at the Alamo!",
"I meant to do that.",
"I'll say! I'm going to start a paper route right now.",
"I don't have to see it, Dottie. I *lived* it.",
"You wanna wear a wet jacket, it's all right with Madame Ruby.",
"That's my name, don't wear it out.",
"For twenty dollars I can tell you a lot of things. For thirty dollars I can tell you more. And for fifty dollars I can tell you *everything*",
"Nobody hipped me to that, dude.",
"What exactly leads you to believe the Soviets were involved?",
"Hot? Who's hot? Feels just fine to me. I feel just PERFECT! In fact, I can't remember when I felt quite so COZY down here!",
"Take a picture, it'll last longer.",
"Your mind plays tricks on you. You play tricks back! It's like you're unraveling a big cable-knit sweater that someone keeps knitting and knitting and knitting and knitting and knitting and knitting and knitting.",
"That old highway's a-calling. Gotta move on."]

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# def restart(channel):
#     """
#         Dirty workaround until CI or similar can exist.
#         Usage: @madamruby restart
#     """
#     p = Popen(['git', 'pull'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
#     for line in p.stdout:
#         if "Already up-to-date." in line:
#             slack_client.api_call("chat.postMessage", channel=channel,
#                           text="Already up-to-date.", as_user=True)
#         else:
#             os.execv(__file__, sys.argv)
#
# def handle_command(quotes, command, channel):
#     """
#         Receives commands directed at the bot and determines if they
#         are valid commands. If so, then acts on the commands. If not,
#         returns back what it needs for clarification.
#     """
#     if command == "restart":
#         restart(channel)
#
#     try:
#         response = quotes[int(command) - 1]
#     except (ValueError, IndexError):
#         response = random.choice(quotes)
#
#     if response:
#         slack_client.api_call("chat.postMessage", channel=channel,
#                           text=response, as_user=True)

@app.message("!hedge")
def hedge(message, say):
    print(message)
    if "!yoda" in message['text']:
        response = "https://media1.giphy.com/media/12FLhMHdanoLJK/giphy.gif"
    else:
        response = "https://media3.giphy.com/media/a93jwI0wkWTQs/giphy.gif"
    say(response)

@app.message("!bold")
def bold(message, say):
    say("BE BOLD!")

@app.message("!jerome")
def jerome(message, say):
    say("point Jerome!")

@app.message("!mattk")
def hbdmattk(message, say):
    say("happy birthday mattk!")

@app.message("!womp")
def womp(message, say):
    say("https://wompwompwomp.com/")

@app.message("!logistics")
def logistics(message, say):
    say("https://media.giphy.com/media/HaTyTRF78zslO/giphy.gif")

@app.message("!fuckit")
def fuckit(message, say):
    say("https://local.theonion.com/man-says-fuck-it-eats-lunch-at-10-58-a-m-1819574888")

@app.message("!peewee")
def peewee(message, say):
    say(random.choice(PEEWEE))

@app.message("!handey")
def handey(message, say):
    say(random.choice(HANDEY))

# def parse_slack_output(slack_rtm_output):
#     """
#         The Slack Real Time Messaging API is an events firehose.
#         this parsing function returns None unless a message is
#         directed at the Bot, based on its ID.
#     """
#     output_list = slack_rtm_output
#     if output_list and len(output_list) > 0:
#         for output in output_list:
#             if output and 'text' in output:
#                 if "!handey" in output['text']:
#                     return HANDEY, output['text'].split("!handey")[1].strip().lower(), \
#                        output['channel']
#                 if "!peewee" in output['text']:
#                     return PEEWEE, output['text'].split("!peewee")[1].strip().lower(), \
#                        output['channel']
#                 if "!hedge" in output['text']:
#                     if "!yoda" in output['text']:
#                         return hedge(output['channel'], True)
#                     else:
#                         return hedge(output['channel'], False)
#                 if "!bold" in output['text']:
#                     return bold(output['channel'])
#                 if "!jerome" in output['text']:
#                     return jerome(output['channel'])
#                 if "!mattk" in output['text']:
#                     return hbdmattk(output['channel'])
#                 if "!womp" in output['text']:
#                     return womp(output['channel'])
#                 if "!logistics" in output['text']:
#                     return logistics(output['channel'])
#                 if "!fuckit" in output['text']:
#                     return fuckit(output['channel'])
#                 if AT_BOT in output['text']:
#                     # return text after the @ mention, whitespace removed
#                     return None, output['text'].split(AT_BOT)[1].strip().lower(), \
#                            output['channel']
#
#     return None, None, None

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
