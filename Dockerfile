FROM python:3.10

ENV PATH="/root/.local/bin:$PATH"


WORKDIR /app
RUN pip install --no-cache-dir poetry


# Copy only Poetry-related files first (to leverage Docker's caching mechanism)
COPY pyproject.toml poetry.lock ./
RUN poetry install 

COPY . /app/

# Command to run the bot
CMD ["poetry", "run", "python", "bot/bot.py"]
