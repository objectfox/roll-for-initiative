
import logging
import os, random

from flask import Flask, request, make_response
from google.cloud import datastore
from google.cloud.datastore import Client
from slack_bolt import App, BoltContext
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings

from datastore import GoogleDatastoreInstallationStore, GoogleDatastoreOAuthStateStore


datastore_client: Client = datastore.Client()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

installation_store = GoogleDatastoreInstallationStore(
    datastore_client=datastore_client,
    logger=logger,
)

app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    oauth_settings=OAuthSettings(
        client_id=os.environ["SLACK_CLIENT_ID"],
        client_secret=os.environ["SLACK_CLIENT_SECRET"],
        scopes=["chat:write.public", "commands", "chat:write"],
        installation_store=installation_store,
        install_page_rendering_enabled=False,
        state_store=GoogleDatastoreOAuthStateStore(
            datastore_client=datastore_client,
            logger=logger,
        ),
        install_path="/slack/install",
        redirect_uri_path="/slack/oauth_redirect",
    ),
)

def generate_initiative(party):
    unsorted_party = []
    for adventurer in party:
        initiative = random.randrange(1,21)
        unsorted_party += [[initiative,["%s %s (%s)" % (random_class_emoji(),adventurer,initiative),adventurer]]]

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


@app.command("/initiative")
def repeat_text(ack, say, respond, command):
    # Acknowledge command request
    ack()
    actors = result = [x.strip() for x in command['text'].split(',')]
    party_data = generate_initiative(actors)
    adventurer_names = [x[0] for x in party_data]
    simple_names = [x[1] for x in party_data]
    adventure_hook = adventure_hooks()

    if len(adventurer_names) > 1:
        room_message = "%s and %s" % (", ".join(adventurer_names[:-1]), adventurer_names[-1])
        response_message = "%s and %s" % (", ".join(simple_names[:-1]), simple_names[-1])
        respond(f"{response_message}")
    else:
        room_message = adventurer_names[0]
    say(f"{adventure_hook}\n{room_message}")


@app.event("tokens_revoked")
def handle_token_revocations(event: dict, context: BoltContext):
    user_ids = event["tokens"].get("oauth")
    if user_ids is not None and len(user_ids) > 0:
        for user_id in user_ids:
            installation_store.delete_installation(
                context.enterprise_id, context.team_id, user_id
            )
    bot_user_ids = event["tokens"].get("bot")
    if bot_user_ids is not None and len(bot_user_ids) > 0:
        installation_store.delete_bot(context.enterprise_id, context.team_id)


@app.event("app_uninstalled")
def handle_uninstallations(context: BoltContext):
    installation_store.delete_all(context.enterprise_id, context.team_id)


flask_app = Flask(__name__)

handler = SlackRequestHandler(app)


@flask_app.route("/", methods=["GET"])
def root():
    return make_response("Hello World!", 200)


@flask_app.route("/slack/install", methods=["GET"])
def install():
    return handler.handle(request)


@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return handler.handle(request)


@flask_app.route("/slack/events", methods=["POST"])
def events():
    return handler.handle(request)

if __name__ == "__main__":
    # for local development
    flask_app.run(
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
        use_debugger=True,
        debug=True,
        use_reloader=True,
    )