
import os, random
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

def generate_initiative(party):
    unsorted_party = []
    for adventurer in party:
        initiative = random.randrange(1,21)
        unsorted_party += [[initiative,"%s %s (%s)" % (random_class_emoji(),adventurer,initiative)]]

    # Sort the party by initiative
    sorted_party = sorted(unsorted_party, key=lambda x: x[0], reverse=True)
    return([a[1] for a in sorted_party])


def random_class_emoji():
    emojis = [
        ":mage:",
        ":ninja:",
        ":fairy:",
        ":astronaut:",
        ":farmer:",
        ":singer:",
        ":cook:",
        ":elf:",
        ":zombie:",
        ":robot_face:",
        ":alien:",
        ":ghost:",
        ":guardsman:"
    ]
    return random.choice(emojis)

def adventure_hooks():
    hooks = [
        "A haunted cry echoes through the canyon! The party rolls for inititive!",
        "From a neighboring tavern table a commotion erupts, roll for initiative!",
        "The full moon slips from behind a cloud, roll for initiative!",
        "Strange lights appear around your boat, roll for initiative!",
        "As you touch the stone, the ground begins to shake. Roll for initiative!",
        "Suddenly the ground gives way beneath you! Roll for initiative!"
    ]
    return random.choice(hooks)


# The echo command simply echoes on command
@app.command("/initiative")
def repeat_text(ack, say, command):
    # Acknowledge command request
    ack()
    print("Asked for initiative with %s" % command['text'])
    actors = result = [x.strip() for x in command['text'].split(',')]
    party = generate_initiative(actors)
    if len(party) > 1:
        message = "%s and %s" % (", ".join(party[:-1]), party[-1])
    else:
        message = party[0]
    adventure_hook = adventure_hooks()
    say(f"{adventure_hook}\n{message}")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 8080)))

