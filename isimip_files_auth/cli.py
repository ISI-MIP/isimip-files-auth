import click
from dotenv import load_dotenv

from .utils import decode_token, encode_token

load_dotenv()


@click.group()
def main():
    """This CLI tool can be used to encode and decode tokens for isimip-files-auth."""
    pass


@main.command()
@click.argument("subject", type=str)
@click.argument("path", type=str)
def encode(subject, path):
    """Encode a token using a subject and a path."""
    click.echo(encode_token(subject, path))


@main.command()
@click.argument("token", type=str)
def decode(token):
    """Decode a token and print its contents."""
    click.echo(decode_token(token))
