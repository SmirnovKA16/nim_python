from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        level = AgentLevels(level)
        if not (level in AgentLevels):
            raise ValueError(
                f"Invalid level: {level}"
            )
        self._level = level

    def lite(self, state_curr: list[int]):
        hint = choice([i for i in range(len(state_curr)) if state_curr[i] != 0])
        take = randint(1, state_curr[hint])
        return NimStateChange(hint, take)

    def dificult(self, state_curr: list[int]):
        x = 0
        for i in state_curr:  # считаем общий XOR
            x ^= i
        if x == 0:
            hint = choice([i for i in range(len(state_curr)) if state_curr[i] != 0])
            take = 1
            return NimStateChange(hint, take)

        else:
            for i in range(len(state_curr)):
                if state_curr[i] != 0:
                    for j in range(1, state_curr[i] + 1):
                        if (x ^ j == 0):
                            return NimStateChange(i, j)
            return NimStateChange(i, j)

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        if self._level == AgentLevels.NORMAL:
            return choice([self.lite(state_curr), self.dificult(state_curr)])

        if self._level == AgentLevels.EASY:
            return self.lite(state_curr)

        if self._level == AgentLevels.HARD:
            return self.dificult(state_curr)
