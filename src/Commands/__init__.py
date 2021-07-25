import ClearCommand
import DevCommand
import GamesCommand
import HelpCommand
import PingCommand
import EmptyCommand

def registerCommands():
    generators = [
        ClearCommand.makeCommand,
        DevCommand.makeCommand,
        GamesCommand.makeCommand,
        HelpCommand.makeCommand,
        PingCommand.makeCommand
    ]
    Commands = {}
    for gen in generators:
        cmd = gen()
        for name in cmd.register:
            Commands[name] = gen
    Commands.setdefault(EmptyCommand.makeCommand)
    return Commands

