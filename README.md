# Discord Quote Bot - 
uses python 3.5 or up and https://github.com/Rapptz/discord.py For chat only interaction

One instance can interact with and store persistent data for multiple servers by storing using separate json files.

### Usage:
1. Create a discord bot at https://discordapp.com/developers/ and insert the token into the line below
```py
  client.run("INSERTTOKENHERE")
```
2. make sure discord.py and all prerequisites are installed correctly.
3. uses the new python 3.5 or higher coroutine syntax.

File creation for new servers does not happen dynamically, if bot is added to a new server, it needs to be restarted to use persistent storage operations.

## Commands:
* !addquote - Add a quote to be stored
* !addquotewithname - Add a quote to be stored that can be retrieved by name
* !quote - get random quote stored with number only
* !quote X - where X is the specific number of the quote
* !quoteaddedby - retrieves what user added which quote
* !popcorn - post an image

### Learning Outcomes:
1. Asynchronous python
2. Problem solving, the single main thread deals with all messages from all servers, the solution was to create a .json file for each server and store all persistent data there.
