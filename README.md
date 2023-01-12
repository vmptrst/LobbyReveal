## LCU-Exploit
Simple CLI application to decode player igns while inside champion select

## Usage
* Download from the <a href="https://github.com/Scary777/LCU-Exploit/releases/tag/lcu-exploit">releases</a> here and simply run the program.

* Enter the command: `pull` any time you want to grab player information. </br>
You'll run into an error anytime you try using this command outside of champion select.

* Copy paste the names into <a href="https://op.gg">op.gg</a> or <a href="https://u.gg">u.gg</a> for a multi-link

<img src="https://media.discordapp.net/attachments/1051258953755000924/1062954400995344414/image.png?width=770&height=428">

## Safety

This is **not** bannable/detectable. The only possible way you could get banned from this is if you made it obvious you had this information and someone reported you. </br>

Player data is gotten by accessing the LCU API which is something that automatically happens behind the scenes within your client, this program is just displaying that information, it's not accessing any data that you weren't authorized for.

## How?

This is accomplished by using <a href="https://github.com/rrthomas/psutils">psutils</a> to grab the `LeagueClient.exe` process and pulling the LCU port and auth token from the process. We then encode the token with a base64 encryption and use it to make an API call to `/chat/v5/participants/champ-select` where we then parse the lobby data back.
