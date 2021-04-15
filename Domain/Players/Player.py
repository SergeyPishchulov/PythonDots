class Player:
    def __init__(self, _id, field=None, UI=None):
        self.id = _id
        self.UI = UI
        self.occupied_dots = set()

    def __str__(self):
        return 'Player {}'.format(self.id)

    def act(self, field):
        success = False
        while not success:
            act_pos = self.UI.get_act_position()
            if act_pos == -1:  # command to quit
                return -1
            if act_pos is not None:
                x, y = act_pos
                success = field.mark_dot(x, y, self)

    @property
    def score(self):
        return len(self.occupied_dots)
