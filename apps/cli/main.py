import argparse
p=argparse.ArgumentParser(); p.add_argument('command',nargs='?',default='health'); print(f'NEELASTACK CLI: {p.parse_args().command}')
