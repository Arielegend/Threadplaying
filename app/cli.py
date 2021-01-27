import click
import sys
from .main import main


@click.command()
@click.option('--wc', default=500, type=int)
@click.option('--tc', default=0, type=int)
def cli(wc, tc):
    """Welcome to wordsplay Reporter"""
    wordscount = wc
    threadscount = tc
    main(wordscount, threadscount)

    print("done main.. Shutting down")


def getAndCheckArguments():
    x = sys.argv[1:]
    print(x)
    pass
