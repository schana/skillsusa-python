from game.internal import body


class Snake:
    def __init__(self, head, mover):
        self.mover = mover
        self.body = body.Body(head)
        self.alive = True
        self.consumed_food = False

    def move(self, food):
        d = self.mover.get_next_direction()
        next_head = self.body.get_head().get_neighbor(d)
        self.consumed_food = next_head == food
        self.body.move(next_head, self.consumed_food)
        self.alive = self.alive and self.body.is_valid()
