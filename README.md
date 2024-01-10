# MixMatch

## Work in Progress
Mixmatch is a command-line interface which allows users to interact with Spotify directly from their terminal, currently it can only show user albums, including tracks, but it is a work in progress and I will add more functionality in the future. 


## Get Started
If you want to try out the tool, follow these instructions:

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

After that you will need to run `pip install -r requirements.txt` and then you can finally run `python mixmatch.py` where all you'll need to do is go to a URL, click Agree, and then just paste the URL you received into the terminal, then you finally start using the CLI. Next time you run the app, you won't need to authenticate, though you might get a error on start, just re-run and you should be fine. 

Run `python mixmatch.py -h` and a menu like this should pop up:
```
options:
  -h, --help            show this help message and exit
  -al [ALBUMS], --albums [ALBUMS] Print out your saved albums or a specific album if a name is provided
```

Run `python mixmatch.py -al` to see all your saved albums, `python mixmatch.py -al "Album Name"` to see a specific album and all their tracks.



