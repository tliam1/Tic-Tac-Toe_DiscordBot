import discord
import time
TOKEN = ''  # blank for security reasons

client = discord.Client()

isXTurn = True
board = [[1, False], [2, False], [3, False],
         [4, False], [5, False], [6, False],
         [7, False], [8, False], [9, False]]
tiles = [':white_large_square:', ':white_large_square:', ':white_large_square:',
         ':white_large_square:', ':white_large_square:', ':white_large_square:',
         ':white_large_square:', ':white_large_square:', ':white_large_square:']
players = ["", ""]
playerIDs = [0, 0]
timeSinceLastPlay = 0
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    message = f"```Type !p to to join a queue or !help for more info!\n\n\n```{printBoard()}"
    text_channel_list = []
    for server in client.guilds:
        for channel in server.channels:
            if str(channel.name) == 'tictactoe':
                text_channel_list.append(channel)

    await text_channel_list[0].send(message)


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]  # the 0 means everything before the hashtag
    user_message = str(message.content)
    channel = str(message.channel)
    print(len(user_message))

    if user_message == "!help" and message.channel.name == 'tictactoe' and message.author != client.user:
        await message.channel.send(f'```Type !p to join queue.\nWhen the game starts use numbers 1-9 '
                                   f'using !(1-9) to place an X or an O.'
                                   f' Number increases left to right, top to bottom'
                                   f'\nIf an active game or queue runs over 2 minutes, '
                                   f'you can end the game/queue with !r\n\n```')

    if user_message == "!r" and message.channel.name == 'tictactoe' and message.author != client.user:
        await message.channel.send(f"```{checkTime()}```")

    if user_message == "!p" and message.channel.name == 'tictactoe' and message.author != client.user:
        if players[0] == "":
            players[0] = username
            playerIDs[0] = message.author.id
            listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
            listOfGlobals['timeSinceLastPlay'] = time.time()  # starts the timer for queue and game length
            await message.channel.send(f'```{username}, you are X, waiting on O```')
            return
        elif players[1] == "" and username != players[0]:
            players[1] = username
            playerIDs[1] = message.author.id
            listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
            listOfGlobals['timeSinceLastPlay'] = time.time()  # resets the queue reset timer when game actually starts
            await message.channel.send(f"```{username}, you are O.\n\n```" + f"<@{playerIDs[0]}> <@{playerIDs[1]}>" + f"```\nYour game can now be played\n\n{getTurn()}\n```{printBoard()}")
    len(user_message)
    if len(user_message) != 2 or user_message[0] != '!' or not user_message[1].isdigit()\
            or int(user_message[1]) < 1 or int(user_message[1]) > 9 \
            or message.author == client.user \
            or not checkUsernameMatch(username):
        return
    if message.channel.name != 'tictactoe':
        return

    print(f'{username}: {user_message} ({channel})')
    boardPosition = [int(user_message[1]), False]
    print(boardPosition)
    if not checkIfPositionIsTaken(boardPosition):
        await message.channel.send(f"```Coordinate Is Taken Please Try Again\n```")

    if checkWinCondition() or checkDrawCondition():  # the game is over and you need to reset board
        await message.channel.send(f"{printBoard()}\n```{resetBoard()}\n\n\n Use !p To Start A New Game!```")
        return

    #  we are now able to send something to the user (This ends the event)
    await message.channel.send(f"```{getTurn()}```\n\n{printBoard()}")


# checks if tile is taken, if not place an x or o there depending on the turn
def checkIfPositionIsTaken(pos):
    for i in range(9):
        if pos == board[i]:
            print("MATCH")
            board[i] = [pos[0], True]
            print(board[i])
            if isXTurn:
                tiles[i] = ':x:'
                listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
                listOfGlobals['isXTurn'] = False
            elif not isXTurn:
                tiles[i] = ':blue_circle:'
                listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
                listOfGlobals['isXTurn'] = True
            return True
    return False

def checkWinCondition():
    lines = [
        # --- horizontal ---
        tiles[0:3],
        tiles[3:6],
        tiles[6:9],
        # --- vertical ---
        tiles[0:9:3],
        tiles[1:9:3],
        tiles[2:9:3],
        # --- diagonal ---
        tiles[0:9:4],
        tiles[2:7:2]
        ]
    assert all(len(line) == 3 for line in lines)  # program fails if any line indexes have length > 3
    if any(filled_with_Xs(line) or filled_with_Os(line) for line in lines):  # Line = lines[i] (or tiles[x:x])
        return True
# The any() function returns True if any element of an iterable is True. If not, it returns False.

    # else game isn't over
    return False

def filled_with_Os(line):  # I like these declared outside of the scope of another function, more like c++
    return line == [':blue_circle:', ':blue_circle:', ':blue_circle:']  # returns true of an line in lines has a list containing 3 o's
def filled_with_Xs(line):
    return line == [':x:', ':x:', ':x:']  # returns true of an line in lines has a list containing 3 X's

# checks if all tiles are taken up
def checkDrawCondition():
    for i in range(len(tiles)):
        if tiles[i] == ':white_large_square:':
            return False
    return True

def resetBoard():
    # Game Over printing

    # refresh the screen, board, and tiles if I want a gameplay loop
    if isXTurn and checkWinCondition():
        gameOverText = f"GAME OVER {players[1]} Wins"
    elif not isXTurn and checkWinCondition():
        gameOverText = f"GAME OVER {players[0]} Wins"
    elif checkDrawCondition():
        gameOverText = "GAME OVER! DRAW!"
    else:
        gameOverText = f"Restarting Game...\n\n Type !p To Start A New Game!"
    # reset the board variables
    for i in range(len(tiles)):
        tiles[i] = ':white_large_square:'
    for i in range(len(board)):
        board[i][1] = False
    # board[i] = [i, False]
    for i in range(len(players)):  # resets active players
        players[i] = ""
        print(players[i])
    listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
    listOfGlobals['isXTurn'] = True  # resetting first player
    listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
    listOfGlobals['timeSinceLastPlay'] = 0
    return gameOverText


def printBoard():
    boardText = f"{tiles[0]}{tiles[1]}{tiles[2]}\n"\
                f"{tiles[3]}{tiles[4]}{tiles[5]}\n"\
                f"{tiles[6]}{tiles[7]}{tiles[8]}"
    return boardText

def getTurn():
    if not isXTurn:
        return f"{players[1]}'s Turn"
    return f"{players[0]}'s Turn"

def checkUsernameMatch(username):
    if (username == players[0] and isXTurn) or (username == players[1] and not isXTurn):
        return True
    return False

def checkTime():
    listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
    returnText = ""
    if listOfGlobals['timeSinceLastPlay'] == 0:
        returnText = "No Currently Active Game\n"
    elif abs(listOfGlobals['timeSinceLastPlay'] - time.time()) < 180:
        returnText = f"Time Till Game Ends: {round(180 - (abs(listOfGlobals['timeSinceLastPlay'] - time.time())), 1)} " \
                     f"seconds\nActive Players:\nX's: {players[0]}\nO's: {players[1]}\n"
    elif abs(listOfGlobals['timeSinceLastPlay'] - time.time()) > 180:
        returnText = f"{resetBoard()}"

    return returnText


client.run(TOKEN)
