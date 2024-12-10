# coding=utf-8


class Disk:
    def __init__(self, setup: str):
        self.setup = setup
        self.files = []
        self.free_spaces = []
        for i, char in enumerate(setup):
            if i % 2 == 0:
                self.files.append(int(char))
            else:
                self.free_spaces.append(int(char))
        self.result = []

    def add(self, id_: int, count: int):
        for _ in range(count):
            self.result.append(id_)

    def checksum(self) -> int:
        self.add(0, self.files[0])
        done_files = 0
        file_idx, space_idx = len(self.files) - 1, 0
        while file_idx > done_files:
            if self.free_spaces[space_idx] >= self.files[file_idx]:
                self.add(file_idx, self.files[file_idx])
                self.free_spaces[space_idx] -= self.files[file_idx]
                file_idx -= 1
                if self.free_spaces[space_idx] == 0:
                    space_idx += 1
                    done_files += 1
                    self.add(done_files, self.files[done_files])
            else:
                self.add(file_idx, self.free_spaces[space_idx])
                self.files[file_idx] -= self.free_spaces[space_idx]
                space_idx += 1
                done_files += 1
                self.add(done_files, self.files[done_files])

        return sum(i * e for i, e in enumerate(self.result))


class DiskWholeFiles(Disk):
    def __init__(self, setup: str):
        super().__init__(setup)
        self.free_spaces_starts = []

    def prepare_resources(self):
        for i in range(len(self.free_spaces)):
            for _ in range(self.files[i]):
                self.result.append(i)
            self.free_spaces_starts.append(len(self.result))
            for _ in range(self.free_spaces[i]):
                self.result.append(-1)
        for _ in range(self.files[i + 1]):
            self.result.append(i + 1)

    def move_file(self, id_: int, free_space_beginning: int):
        for i in range(len(self.result)):
            if self.result[i] == id_:
                self.result[i] = -1
        for i in range(self.files[id_]):
            self.result[free_space_beginning + i] = id_

    def check_order(self, file_idx: int, free_space_beginning: int) -> bool:
        return self.result.index(file_idx) > free_space_beginning

    def checksum(self) -> int:
        self.prepare_resources()
        file_idx = len(self.files) - 1
        while file_idx > 0:
            for i, free_space in enumerate(self.free_spaces):
                if self.files[file_idx] > free_space:
                    continue
                if self.check_order(file_idx, self.free_spaces_starts[i]):
                    self.move_file(file_idx, self.free_spaces_starts[i])
                    self.free_spaces[i] -= self.files[file_idx]
                    self.free_spaces_starts[i] += self.files[file_idx]
                break
            file_idx -= 1
        result = 0
        for i, e in enumerate(self.result):
            result += i * e if e != -1 else 0
        return result


def main():
    with open('input.txt') as f:
        for line in f.readlines():
            disk = Disk(line.strip())
            disk_whole = DiskWholeFiles(line.strip())

    result = disk.checksum()
    result2 = disk_whole.checksum()
    assert result == 6330095022244
    assert result2 == 6359491814941
    print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
