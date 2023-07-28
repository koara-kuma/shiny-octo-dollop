import discord
from discord.ext import commands
import random
import asyncio

class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.board = [':white_large_square:'] * 9
        self.reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def is_board_full(self):
        return all(square != ':white_large_square:' for square in self.board)

    def check_winner(self, board):
        # Check rows
        for i in range(0, 9, 3):
            if board[i] == board[i + 1] == board[i + 2] and board[i] != '⬜':
                return board[i]

        # Check columns
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6] and board[i] != '⬜':
                return board[i]

        # Check diagonals
        if board[0] == board[4] == board[8] and board[0] != '⬜':
            return board[0]
        if board[2] == board[4] == board[6] and board[2] != '⬜':
            return board[2]

        return None

    def make_ai_move(self):
        empty_positions = [i for i, x in enumerate(self.board) if x == ':white_large_square:']
        if empty_positions:
            position = random.choice(empty_positions)
            self.board[position] = ':o:'

    async def display_board(self, ctx, is_player_turn=True, message=None):
        # Send or update the current board as an embed
        if message is None:
            embed = discord.Embed(title='Tic Tac Toe', color=discord.Color.purple())
            embed.description = f"{self.board[0]} {self.board[1]} {self.board[2]}\n{self.board[3]} {self.board[4]} {self.board[5]}\n{self.board[6]} {self.board[7]} {self.board[8]}"
            if is_player_turn:
                embed.set_footer(text="Your Turn")
            else:
                embed.set_footer(text="AI's Turn")
            message = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Tic Tac Toe', color=discord.Color.purple())
            embed.description = f"{self.board[0]} {self.board[1]} {self.board[2]}\n{self.board[3]} {self.board[4]} {self.board[5]}\n{self.board[6]} {self.board[7]} {self.board[8]}"
            if is_player_turn:
                embed.set_footer(text="Your Turn")
            else:
                embed.set_footer(text="AI's Turn")
            await message.edit(embed=embed)

        # Add reactions to the message for board positions
        for reaction in self.reactions:
            await message.add_reaction(reaction)

        return message

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tic Tac Toe cog is ready.')

    def reset_board(self):
        self.board = [':white_large_square:'] * 9

    @commands.command()
    async def tictactoe(self, ctx):
        self.reset_board()
        await ctx.send('Welcome to Tic Tac Toe! React with the corresponding number to place your piece. The board is as follows:')
        message = await self.display_board(ctx)

        def check_valid_move(reaction, user):
            return user == ctx.author and str(reaction.emoji) in self.reactions and \
                   self.board[self.reactions.index(str(reaction.emoji))] == ':white_large_square:'

        # Player and AI moves loop
        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60, check=check_valid_move)
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to make a move. The game is over.")
                return

            position = self.reactions.index(str(reaction.emoji))
            self.board[position] = ':x:'

            winner = self.check_winner(self.board)
            if winner == ':x:':
                await self.display_board(ctx, is_player_turn=False, message=message)
                await ctx.send('You win!')
                return
            elif self.is_board_full():
                await ctx.send("It's a tie!")
                return

            await self.display_board(ctx, is_player_turn=False, message=message)

            # AI's turn
            self.make_ai_move()

            winner = self.check_winner(self.board)
            if winner == ':o:':
                await self.display_board(ctx, is_player_turn=True, message=message)
                await ctx.send('You lose!')
                return
            elif self.is_board_full():
                await ctx.send("It's a tie!")
                return

            await self.display_board(ctx, is_player_turn=True, message=message)

async def setup(client):
    await client.add_cog(TicTacToe(client))
