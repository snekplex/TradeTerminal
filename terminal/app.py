from cmd import Cmd

class TradeTermial(Cmd):

    prompt = '> '

    def do_echo(self, text):
        print(text)

    def do_exit(self, args):
        raise SystemExit()
