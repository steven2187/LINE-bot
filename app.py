from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('vMof5Sfb6sZyKPShw400l0PUp5issD/JAplgqMZGaqmvfDSjUlsBIv0QJsyh8ACyjfsLdO1VzNl0Xn4nloRmJIYp7OnhgUOf7Z7UzuwH6Bbjd1qmKERA5PzqLfGrgdzy+RsFnqJ2r3EqGePNh32EHAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e7eee1603b717ee387a86bd1729072ca')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()