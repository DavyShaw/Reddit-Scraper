import requests
import requests.auth
import json

# Reddit API credentials
CLIENT_ID = '<Insert ID>' #ID for your app
CLIENT_SECRET = '<Insert Secret Key>' #Reddit secret key
USER_AGENT = 'App V1' #Your name for app
USERNAME = '<Insert Reddit username>' #Reddit username
PASSWORD = '<Insert Reddit password>' #Reddit Password

def get_reddit_token(): #Getting your access token from Reddit
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    headers = {'User-Agent': USER_AGENT}
    data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    response.raise_for_status()
    return response.json().get('access_token')

def fetch_reddit_data(token, subreddit, limit=1000): #Fetch reddit data - data return is limited to 1000 posts
    headers = {'Authorization': f'bearer {token}', 'User-Agent': USER_AGENT}
    url = f'https://oauth.reddit.com/r/{subreddit}/new.json?limit={limit}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def check_user_info(token): #Checking your user info - for testing
    headers = {'Authorization': f'bearer {token}', 'User-Agent': USER_AGENT}
    response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    response.raise_for_status()
    return response.json()

def check_subreddit_info(token, subreddit): #Checking your chosen subreddit info - for testing
    headers = {'Authorization': f'bearer {token}', 'User-Agent': USER_AGENT}
    url = f'https://oauth.reddit.com/r/{subreddit}/about.json'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_json(data, filename='reddit_data.json'): #Saves reddit data to JSON file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Data saved to {filename}')

if __name__ == "__main__":
    try:
        # Fetch and check Reddit token
        token = get_reddit_token()
        print(f'Token: {token}')  # For debugging

        # Check user info
        user_info = check_user_info(token)
        print(f'User Info: {user_info}')

        # Check subreddit info
        subreddit_info = check_subreddit_info(token, 'ukpolitics')
        print(f'Subreddit Info: {subreddit_info}')

        # Fetch Reddit data
        reddit_data = fetch_reddit_data(token, '<Insert chosen subreddit>')  #Insert your subreddit of choice here
        print(f'Reddit Data: {reddit_data}')

        # Save data to JSON
        save_to_json(reddit_data)

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
