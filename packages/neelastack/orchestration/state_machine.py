from enum import StrEnum
class State(StrEnum):
    PLANNING="planning"; EXECUTING="executing"; REVIEWING="reviewing"; DONE="done"; FAILED="failed"
