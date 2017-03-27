# madamruby

  ![Alt text](/madamruby.jpg?raw=true "You're here because you ... WANT something ...")

_"For twenty dollars I can tell you a lot of things. For thirty dollars I can tell you more. And for fifty dollars I can tell you *everything*."_

### Setup

Clone the repository.
```
virtualenv madamruby
source madamruby/bin/activate
pip install slackclient
```
Create a development bot at https://wetjacket.slack.com/apps/new/A0F7YS25R-bots.
```
export SLACK_BOT_TOKEN='your slack token pasted here'
export BOT_NAME='your slack bot name pasted here'
python print_bot_id.py
export BOT_ID='bot id returned by script'
python madamruby.py
```
In Slack, join `#madamruby-test`, Settings, and Invite team members to join... and invite your development bot to the `#madamruby-test` channel.

### Run
```
source madamruby/bin/activate
python madamruby.py
```

### Deploy
In Slack:
```
@madamruby restart
```

### References

https://www.fullstackpython.com/blog/build-first-slack-bot-python.html (thanks!)
