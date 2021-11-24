import click
import uvicorn
import os


@click.command()
@click.argument("port", type=int)
def main(port: int):
    if os.path.isfile("port"):
        raise RuntimeWarning(
            "file 'port' already exist, is the server already running?"
        )
    with open("port", "w") as f:
        f.write(str(port))

    uvicorn.run("app:app", host="localhost", port=port)

    if os.path.isfile("port"):
        os.remove("port")


if __name__ == "__main__":
    main()
