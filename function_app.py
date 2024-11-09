import azure.functions as func
import logging
import os
import requests
import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.timer_trigger(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def daily(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    # Fetch news data from the API
    url = 'https://newsdata.io/api/1/latest?country=vi&category=politics&apikey=pub_58695ffe53513b97d78ce05437d91b5109031'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch news data. Status code: {response.status_code}")
        return

    content = response.json()
    news_list = content.get('results', [])

    # Format message with fetched news data
    msg = f"**Today's Hot News - {datetime.datetime.now().strftime('%Y-%m-%d')}**\n\n"
    for result in news_list[:5]:  # Limiting to the first 5 articles for brevity
        title = result.get('title', 'No title')
        link = result.get('link', 'No link')
        msg += f"**Tiêu đề**: {title}\n**Link**: {link}\n\n"

    # Send message to Discord
    discord_webhook_url = os.getenv('https://discord.com/api/webhooks/1304729546934980668/RurMeu02XAOVJIET1xOc-AJSksNXC6pa5jRV9U_-kB5XwLu-TcMW-9pPZDFL0UBGOe1v')  # Set your Discord webhook URL in environment variables
    discord_message = {"content": msg}

    discord_response = requests.post(discord_webhook_url, json=discord_message)
    if discord_response.status_code == 204:
        print("News sent successfully to Discord")
    else:
        print(f"Failed to send news to Discord. Status code: {discord_response.status_code}")
    # Call the main function from __init__.py