"""
bot_player.py — Phase 6
Polymorphic player model: HumanPlayer waits for socket input,
BotPlayer runs an instant decision algorithm.
"""


class Player:
    """Base player — holds shared state."""

    def __init__(self, nickname: str, chips: int = 1000):
        self.nickname = nickname
        self.chips = chips
        self.hand = []
        self.bet = 0
        self.round_bet = 0
        self.folded = False

    def get_action(self, game_state: dict) -> dict:
        """Return an action dict: {action: 'fold'|'call'|'raise', amount: int}"""
        raise NotImplementedError

    def to_dict(self):
        return {
            'nickname': self.nickname,
            'chips': self.chips,
            'bet': self.bet,
            'round_bet': self.round_bet,
            'folded': self.folded,
        }


class HumanPlayer(Player):
    """Action comes from the player's phone via Socket.IO."""

    def __init__(self, nickname: str, sid: str, chips: int = 1000):
        super().__init__(nickname, chips)
        self.sid = sid

    def get_action(self, game_state: dict) -> dict:
        raise RuntimeError('HumanPlayer actions come from socket events, not get_action()')


class BotPlayer(Player):
    """Base bot — subclass and override get_action() for different personalities."""

    def __init__(self, nickname: str, personality: str = 'calculator', chips: int = 1000):
        super().__init__(nickname, chips)
        self.personality = personality
        self.sid = None

    def get_action(self, game_state: dict) -> dict:
        hand_strength = self._evaluate_hand(game_state)

        if self.personality == 'rock':
            return self._rock_strategy(hand_strength, game_state)
        elif self.personality == 'maniac':
            return self._maniac_strategy(hand_strength, game_state)
        else:
            return self._calculator_strategy(hand_strength, game_state)

    # ── Personalities ──────────────────────────────────────────────────────────

    def _rock_strategy(self, strength: float, game_state: dict) -> dict:
        """Folds unless hand is very strong (> 0.7)."""
        if strength > 0.7:
            return {'action': 'raise', 'amount': game_state.get('current_bet', 20) * 2}
        elif strength > 0.4:
            return {'action': 'call', 'amount': 0}
        return {'action': 'fold', 'amount': 0}

    def _maniac_strategy(self, strength: float, game_state: dict) -> dict:
        """Raises aggressively; rarely folds."""
        if strength > 0.3:
            return {'action': 'raise', 'amount': game_state.get('current_bet', 20) * 3}
        return {'action': 'call', 'amount': 0}

    def _calculator_strategy(self, strength: float, game_state: dict) -> dict:
        """Plays by pot odds and hand strength."""
        call_amount = game_state.get('call_amount', 0)
        pot = game_state.get('pot', 1)
        pot_odds = call_amount / (pot + call_amount) if (pot + call_amount) > 0 else 0

        if strength > pot_odds + 0.2:
            return {'action': 'raise', 'amount': game_state.get('current_bet', 20) * 2}
        elif strength > pot_odds:
            return {'action': 'call', 'amount': call_amount}
        return {'action': 'fold', 'amount': 0}

    # ── Hand evaluation ────────────────────────────────────────────────────────

    def _evaluate_hand(self, game_state: dict) -> float:
        """Returns a strength score 0.0–1.0 based on best available hand."""
        community = game_state.get('community_cards_objects', [])
        cards = (self.hand or []) + community
        if len(cards) >= 5:
            from game_engine import best_hand_value
            val = best_hand_value(cards)
            return val[0] / 8.0
        # Pre-flop: use a simple hole card heuristic
        if len(self.hand) == 2:
            high = max(c.value for c in self.hand) / 14.0
            pair = 0.3 if self.hand[0].value == self.hand[1].value else 0.0
            return min(1.0, high * 0.6 + pair)
        import random
        return random.uniform(0.2, 0.5)
