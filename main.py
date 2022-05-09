import discord

TOKEN = 'OTczMDg1MjI2NTM4NTIwNTg3.GRUbFl.3HoTV2kLiYMbjL8xQYZqz3VS2GlT1UBVkxAdM4'

client = discord.Client()

isXTurn = True
board = [[1, 1, False], [2, 1, False], [3, 1, False],
         [1, 2, False], [2, 2, False], [3, 2, False],
         [1, 3, False], [2, 3, False], [3, 3, False]]
tiles = [' ', ' ', ' ',
         ' ', ' ', ' ',
         ' ', ' ', ' ']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    message = f"```{getTurn()}\n{printBoard()}```"
    text_channel_list = []
    for server in client.guilds:
        for channel in server.channels:
            if str(channel.name) == 'tictactoe':
                text_channel_list.append(channel)

    await text_channel_list[0].send(message)


# @client.event(discord.reaction)
# async def someReactionFuntion():
#     print("someone reacted")
# basically saying: on_message = client.event(on_message)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]  # the 0 means everything before the hashtag
    user_message = str(message.content)
    channel = str(message.channel)
    print(len(user_message))

    if user_message == "!help" and message.channel.name == 'tictactoe' and message.author != client.user:
        await message.channel.send(f'Proper Test From {username}')

    if len(user_message) != 4 or user_message[0] != '!' or not user_message[1].isdigit() or \
            not user_message[3].isdigit() or int(user_message[1]) < 1 or int(user_message[1]) > 3 \
            or message.author == client.user or int(user_message[3]) < 1 or int(user_message[3]) > 3 \
            or user_message[2] != ',':
        return
    if message.channel.name != 'tictactoe':
        return
    print(f'{username}: {user_message} ({channel})')
    boardPosition = [int(user_message[1]), int(user_message[3]), False]
    checkIfPositionIsTaken(boardPosition)

    if checkWinCondition() or checkDrawCondition():  # the game is over and you need to reset board
        await message.channel.send(f"```{printBoard()}\n {resetBoard()}\n\n\n```")

    #  we are now able to send something to the user (This ends the event)
    await message.channel.send(f"```{getTurn()}\n{printBoard()}```")


# checks if tile is taken, if not place an x or o there depending on the turn
def checkIfPositionIsTaken(pos):
    for i in range(9):
        if pos == board[i]:
            print("MATCH")
            board[i] = [pos[0], pos[1], True]
            print(board[i])
            if isXTurn:
                tiles[i] = 'x'
                listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
                listOfGlobals['isXTurn'] = False
            elif not isXTurn:
                tiles[i] = 'o'
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
    return line == ['o', 'o', 'o']  # returns true of an line in lines has a list containing 3 o's
def filled_with_Xs(line):
    return line == ['x', 'x', 'x']  # returns true of an line in lines has a list containing 3 X's

# checks if all tiles are taken up
def checkDrawCondition():
    for i in range(len(tiles)):
        if tiles[i] == ' ':
            return False
    return True

def resetBoard():
    # Game Over printing
    if checkDrawCondition():
        gameOverText = "GAME OVER! DRAW!"
        # refresh the screen, board, and tiles if I want a gameplay loop
    elif isXTurn:
        gameOverText = "GAME OVER O Wins"
    else:
        gameOverText = "GAME OVER X Wins"
    # reset the board variables
    for i in range(len(tiles)):
        tiles[i] = ' '
    for i in range(len(board)):
        board[i][2] = False
        print(board)
    # board[i] = [i, False]

    listOfGlobals = globals()  # only way to assign new values to "Undetermined value" globals
    listOfGlobals['isXTurn'] = True  # resetting first player
    return gameOverText


def printBoard():
    boardText = f"   1       2      3\n1 {tiles[0]}\t| {tiles[1]}\t| {tiles[2]}"\
                f"\t\n_____________________\n2 {tiles[3]}\t| {tiles[4]}\t| {tiles[5]}"\
                f"\t\n_____________________\n3 {tiles[6]}\t| {tiles[7]}\t| {tiles[8]}\t"
    return boardText

def getTurn():
    if isXTurn:
        return "X's Turn"
    else:
        return "O's Turn"


client.run(TOKEN)
