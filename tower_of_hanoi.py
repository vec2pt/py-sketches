"""
20240803

Tower of Hanoi (Recursive solution)

Links:
    https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""


class TowerOfHanoi:
    def __init__(self, q=3, from_peg=0, buff_peg=1, to_peg=2) -> None:
        self._q = q
        self._from_peg = from_peg
        self._buff_peg = buff_peg
        self._to_peg = to_peg
        self._map = [[], [], []]
        self._map[self._from_peg] = [self._q - i for i in range(self._q)]

    def __str__(self) -> str:
        lens = sum(len(peg) for peg in self._map)
        rows = []
        for i in range(lens):
            row = ""
            for peg in self._map:
                try:
                    offset = (lens - peg[i]) * " "
                    row += offset + "-" * (peg[i] * 2) + offset + " "
                except IndexError:
                    row += " " * (lens * 2) + " "
            rows.append(row)
        rows.reverse()
        rows.append((lens * 6 + 2) * "=")
        return "\n".join(rows)

    def _move_peg(self, from_peg, to_peg):
        self._map[to_peg].append(self._map[from_peg][-1])
        del self._map[from_peg][-1]
        print(self)
        print(
            f"Move disk {self._map[to_peg][-1]} from peg {from_peg + 1} to peg {to_peg+ 1}."
        )

    def _hanoi(self, q, from_peg, buff_peg, to_peg):
        if q == 0:
            return
        self._hanoi(q - 1, from_peg, to_peg, buff_peg)
        self._move_peg(from_peg, to_peg)
        self._hanoi(q - 1, buff_peg, from_peg, to_peg)

    def run(self):
        self._hanoi(self._q, self._from_peg, self._buff_peg, self._to_peg)


if __name__ == "__main__":
    toh = TowerOfHanoi(5)
    toh.run()
