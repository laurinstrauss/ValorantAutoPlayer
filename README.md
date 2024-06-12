# ValorantAutoPlayer
ValorantAutoPlayer can run in the background of VALORANT and auto pause media when the player is in an active round and respectively playing the music as soon as the player dies or the round has ended. Works for the default Windows Media Player and Apps that access it (e.g. Spotify, Apple Music, YouTube in Browser, Netflix, ...)
***
## Requirements
\- Windows System
\- VALORANT and System Screen Resolution is "1920 x 1080 16:9" (Framerate / Refreshrate does not matter)
\- VALORANT is running on the systems primary monitor
\- VALORANT language is set to english
\- VALORANT Display Mode is "Fullscreen" or "Windowed Fullscreen"
***
## How to install
\- download this repository
\- make sure you have Python installed ([text]https://www.python.org/downloads/)
\- run InstallDependencies.bat once (simply double click)
\- move the Application /dist/ValorantAutoPlayer.exe to wherever you want (single file application)
***
## Troubleshooting
The Application works by simply periodically taking a screenshot of VALORANT and search for pixels that correlate to a gamestate and then play/pause the media, if VALORANT changes its UI-Layout you just have to adjust the coordinates of the pixels that are checked by ValorantAutoPlayer and the Application works fine again. Correlating to that, if you have another screen resolution than 1920x1080 just take screenshots and measure the coordinates of the pixels that are checked and replace them.
Which pixels are checked is described in the .py file, and there are also screenshots under /ReferencedImages/ that can be used to find out which pixels are checked.
You can open the ValorantAutoPlayer.py file and make changes that might fix problems, such as resolution changes, VALORANT UI changes in future patches or system resource changes.
***
## Buy me a coffee
If you like the application, you can send me some money via PayPal, you can find me there under @laurinstrauss
Of course this is open source and im glad if you like the application so also feel free to use it for free.