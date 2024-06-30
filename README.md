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
| Recommendations from Spotify |✅|
| Play songs, playlist, album |🚧|
| Pause, Resume, Replay songs |🚧|
| Check playback, see song details, artists, album |🚧|
| Go to previous song, next song, toggle repeat, shuffle |🚧|


## Get Started
**Disclaimer: This CLI only supports Windows 10/11**<br>

If you want to try out this tool, follow these instructions:

First, install:
- Python (3.10 or higher)
- Clone this repository by running `git clone https://github.com/cayyus/mixmatch-spotify-cli.git`

Then navigate over to the folder using `cd mixmatch-spotify-cli`

Before going forward, you will need a Spotify Developer Key and Secret, so navigate over to https://developer.spotify.com/dashboard and click the create new app button. You can type whatever you want as the name and description, however make sure the **Redirect URI is https://open.spotify.com/ and that Web API is selected on the question "Which API/SDKs are you planning to use?"**, these are crucial and the CLI won't work without them. 

Click on your app in the dashboard and click settings, there you should see your Client ID and the Client Secret, take those and store it somewhere for now.

In the project folder, there is a file called `csetup.py`, run the file, there, you'll be asked to input those `Client ID` and `Client Secret` from earlier, and also, you will be asked to give a command prefix, a prefix is a short way to run a file, meaning you won't need to type in the absolute path of `mixmatch.py` every time you want to run a command from the CLI, making running stuff a lot easier. 

Upon completion of the setup, in the current project directory, `mixmatch-spotify-cli`, there will be a `.cmd` file, which basically just contains a `python run` for the `mixmatch.py` file. All you need to do now is just to put this `.cmd` file into the C folder, at `C:/`. Just cut the file from the directory and paste it there, it may ask you to provide administrative privileges to make the move, just agree. If you are uncomfortable with putting this file in the C Drive, well unfortunately this is a required step to make this CLI work. But I assure you, this file is completely safe, you can even check out the source code for `csetup.py` and the `.cmd` file creation process if you want.

Now, just type in your chosen prefix with `\` (`\your_command_prefix`) and a browser window will open with the OAuth screen in Spotitfy, click Agree, and then you will be redirected to an `open.spotify.com` link, just copy the entire link and pasted it in the terminal, after a bit, if your authentication was successful, you will be displayed a welcome text along with a 
direction on how to get all the commands using `\your_command_prefix -h`. You can now finally run CLI commands, Enjoy!


