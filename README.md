# Online Twitch Checker

This script checks if one or more Twitch streamers are currently live.

## Description

This Python script takes a list of Twitch channel names as command-line arguments and checks their online status using the `decapi.me` API. It uses `httpx` for asynchronous requests to check multiple channels concurrently, with a rate limiter to avoid sending too many requests at once.

The output will indicate whether each channel is "ONLINE" or "OFFLINE". For online channels, it will also display their stream uptime.

**Note:** The script currently has some of its output messages in Russian.

## Installation

1.  **Clone the repository or download the files.**

2.  **Make sure you have Python 3.12 or newer.**

3.  **Install the dependencies.**

    This project uses `uv` for package management. You can install the dependencies from `pyproject.toml` and `uv.lock` using `uv`:

    ```bash
    pip install uv
    uv sync
    ```

    Alternatively, you can install the packages listed in `pyproject.toml` using `pip`:

    ```bash
    pip install "aiolimiter>=1.2.1" "httpx>=0.28.1" "requests>=2.3.2"
    ```

## Usage

Run the script from your terminal and pass the Twitch channel names you want to check as arguments:

```bash
uv run main.py <nickname1> <nickname2> <nickname3>
```

**Example:**

```bash
uv run main.py shroud summit1g
```

### Example Output

```
shroud: ONLINE
Uptime: 2 hours, 3 minutes, 4 seconds
summit1g: OFFLINE
Ответ сервиса: summit1g is offline
```

### The `input.txt` file

The project includes an `input.txt` file containing a list of nicknames. However, in its current version, the script **does not** read from this file. You must provide the nicknames as command-line arguments as shown above.

```bash
cat input.txt | xargs uv run main.py
```
