# MixMatch
Mixmatch is a command-line interface which allows users to interact with Spotify from the terminal. <br>

## Features
| Feature  | Status |
| ------------- | ------------- |
| Liked albums  |✅|
| Liked playlists  |✅|
| Liked tracks     |✅|
| Featured playlists from Spotify |✅|
| Search artists and profile |✅|
| Search for albums, tracks, playlists |🚧|
| Recommendations |🚧|


## Get Started
**Disclaimer: This CLI only supports Windows 10/11**<br>
**<i>Working on making this work as a executable</i>**

If you want to try out this tool, follow these instructions:

First, install:
- Python (3.10 or higher)
- Clone this repository by running `git clone https://github.com/cayyus/mixmatch-spotify-cli.git`

Then navigate over to the folder using `cd mixmatch-spotify-cli`

Before going forward, you will need a Spotify Developer Key and Secret, so navigate over to https://developer.spotify.com/dashboard and click the create new app button. You can type whatever you want as the name and description, however make sure the **Redirect URI is https://open.spotify.com/ and that Web API is selected on the question "Which API/SDKs are you planning to use?"**, these are crucial and the CLI won't work without them. 

Click on your app in the dashboard and click settings, there you should see your Client ID and the Client Secret, take those and create a new file in the project directory called `creds.env`, and type the Client ID and the Client Secret in this format:
```
CLIENT_ID='your client id here'
CLIENT_SECRET='your client secret here'
```

After that you will need to run `pip install -r requirements.txt` and then you can finally run `python mixmatch.py` where all you'll need to do is go to the  URL given, click Agree, and then just paste the URL you received into the terminal, then you finally start using the CLI. Next time you run the program, you won't need to authenticate, though you might get a error on start (a **KeyError** or a error message which says **the access-token is expired**), just re-run and you should be fine. 

Run `python mixmatch.py -h` and a help menu should pop up, listing out all the commands you can use.

