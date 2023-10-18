"""
Rock paper scissors game manager
"""

import hikari
import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar


class Status(Enum):
    """
    Rock paper scissors match statuses
    """

    WIN = auto()
    LOSE = auto()
    DRAW = auto()


class Shape(Enum):
    """
    Rock paper scissors shapes
    """

    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


class Color(Enum):
    """
    Colors for embeds
    """

    GRAY = hikari.Color.from_rgb(109, 109, 109)
    RED = hikari.Color.from_rgb(204, 48, 48)
    GREEN = hikari.Color.from_rgb(51, 198, 54)
    YELLOW = hikari.Color.from_rgb(226, 166, 24)


@dataclass
class Game():
    """
    Main game class
    """

    user: hikari.Member
    target_score: int = field(default=3)
    round_num: int = field(default=1, init=False)
    game_over: bool = field(default=False, init=False)
    user_score: int = field(default=0, init=False)
    comp_score: int = field(default=0, init=False)
    SCORE_FORMAT: ClassVar[str] = "Player : Computer\n{}"
    INSTRUCTIONS: ClassVar[str] = ("Type \"rock\", \"paper\", or \"scissors\""
                                   "to select your choice."
                                   "\nType \"!stop\" to stop the game")
    EMOJIS: ClassVar[dict[Shape, str]] = {
        Shape.ROCK: "✊",
        Shape.PAPER: "🤚",
        Shape.SCISSORS: "✌"
    }
    COLORS: ClassVar[dict[Status, hikari.Color]] = {
        Status.WIN: Color.GREEN.value,
        Status.LOSE: Color.RED.value,
        Status.DRAW: Color.YELLOW.value
    }
    
    def advance_round(self, user: Shape) -> hikari.Embed | None:
        """
        :param user: Shape - The user's choice
        :return: Status - The result of the round

        Advances the level to the next level
        """

        if self.game_over:
            return
        
        comp = random.choice(list(Shape))
        result = self.check_winner(user, comp)
        if result == Status.WIN:
            self.user_score += 1
        elif result == Status.LOSE:
            self.comp_score += 1
        
        if self.target_score in {self.user_score, self.comp_score}:
            self.game_over = True
            return self.create_end_embed()

        self.round_num += 1
        return self.create_round_embed(user, comp)

    @staticmethod
    def check_winner(user: Shape, comp: Shape) -> Status:
        """
        :param user: Shape - The user's choice
        :param comp: Shape - The comp's choice
        :return: Status - The result of the match (win, lose, draw)

        Calculates the result of a match
        """

        wins: tuple[tuple[Shape, Shape]] = ((Shape.ROCK, Shape.SCISSORS),
                                            (Shape.SCISSORS, Shape.PAPER),
                                            (Shape.PAPER, Shape.ROCK))
        result: Status

        if user == comp:
            result = Status.DRAW
        elif (user, comp) in wins:
            result = Status.WIN
        else:
            result = Status.LOSE
        return result
    
    def create_template_embed(self,
                              color: hikari.Color | None = None
                              ) -> hikari.Embed:
        """
        :param color: hikari.Color - The Color of embed
        :return: hikari.Embed - The template hikari embed

        Creates a template embed
        """

        if color is None:
            color = Color.GRAY.value
        template = hikari.Embed(title="Rock Paper Scissors",
                                 color=color)
        icon = (self.user.avatar_url or self.user.default_avatar_url).url
        score_string = f"{self.user_score} : {self.comp_score}"
        template.set_author(name=f"{self.user.display_name}",
                            icon=icon)
        template.add_field(name="Score",
                           value=self.SCORE_FORMAT.format(score_string),
                           inline=False)
        template.set_footer(text=self.INSTRUCTIONS)
        return template
    
    def create_round_embed(self,
                           user: Shape,
                           comp: Shape) -> hikari.Embed:
        """
        :param user: Shape - The user's choice
        :param comp: Shape - The comp's choice
        :return: hikari.Embed - The current round hikari embed

        Creates the embed for the current round
        """

        status = self.check_winner(user, comp)
        color: hikari.Color = self.COLORS[status]

        template = self.create_template_embed(color)
        user_emoji = self.EMOJIS[user]
        comp_emoji = self.EMOJIS[comp]
        template.add_field(name=f"Round {self.round_num}",
                           value=f"{user_emoji} vs {comp_emoji}",
                           inline=False)
        return template
    
    def create_end_embed(self) -> hikari.Embed:
        """
        :return: hikari.Embed - The ending hikari embed

        Creates the embed for the ending
        """

        result: str
        color: hikari.Color
        if self.user_score > self.comp_score:
            result = "You win!"
            color = Color.GREEN.value
        elif self.user_score < self.comp_score:
            result = "You lost..."
            color = Color.RED.value
        template = self.create_template_embed(color)
        template.add_field(name="Result",
                           value=result)
        return template
