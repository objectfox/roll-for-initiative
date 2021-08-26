# roll-for-initiative
A slack bot for randomizing the order of adventuring parties, aka standup.

Sample Use

```
/initiative Tom, Mary, Gandalf, Tina, Bilbo, Joan

```

It generates simplified output to you, for easy cutting and pasting into Zoom or what have you.

```

Frodo, Bilbo, Mary, Joan, Gandalf, Tom and Tina
```

Then it sends a more exciting version to the conversation.

```
From a neighboring tavern table a commotion erupts, roll for initiative!
🧚‍♂️ Frodo (20), 👨‍🎤 Bilbo (20), 🤖 Mary (15), 👽 Joan (13), 🧙‍♂️ Gandalf (5), 🧟‍♂️ Tom (2) and 💂‍♀️ Tina (1)

```

Note that character class emojis are the gender-neutral default slack versions.

<a href="https://roll-for-initiative-kp73hsfita-uw.a.run.app/slack/install"><img alt="Add to Slack" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>

Most of the documentation for how to build this came from the Slack [Python Bolt docs](https://slack.dev/bolt-python/tutorial/getting-started) and [this excellent gist](https://gist.github.com/seratch/d81a445ef4467b16f047156bf859cda8) by [seratch](https://github.com/seratch).

Licensed as MIT, except for the Dungeon Door png, which is by smalllikeart on flaticon.com, and datastore.py which is by seratch.
