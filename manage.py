
import typer
from pathlib import Path

AUDIO_BASE_DIR = Path("./audio")

app = typer.Typer()

@app.command()
def generate_playlist(channel: str = typer.Argument(None)):
    """
    Finds all audio files in the channel directories and generates
    the playlist.txt files required by Ices.
    """
    typer.echo(f"Starting Playlist Generator for channel {channel}")

    if not AUDIO_BASE_DIR.is_dir():
        typer.secho(f"Error: Base audio directory '{AUDIO_BASE_DIR}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    channel_dir = AUDIO_BASE_DIR / channel
    playlist_file = AUDIO_BASE_DIR / channel / "playlist.txt"


    if not channel_dir.is_dir():
        typer.secho(f"Warning: Directory for '{channel}' not found. Skipping.", fg=typer.colors.YELLOW)

    # Find all files recursively in the channel directory
    audio_files = [f for f in channel_dir.rglob('*') if f.is_file() and f.suffix == ".mp3"]

    if not audio_files:
        typer.secho(f"Warning: No audio files found in '{channel_dir}'. Playlist will be empty.", fg=typer.colors.YELLOW)
        # Still create an empty playlist to prevent errors
        playlist_file.write_text("\n") # Write just the blank line

    with open(playlist_file, "w") as f:
        for file_path in audio_files:
            container_path = f"/{file_path}"
            f.write(f"{container_path}\n")

        # Ices0 requires a blank line at the end of the playlist
        f.write("\n")

    typer.secho(f"Playlist for '{channel}' created successfully at {playlist_file} with {len(audio_files)}" , fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()