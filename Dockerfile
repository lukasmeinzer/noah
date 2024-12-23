FROM python:3.10

ENV PATH="/root/.local/bin:$PATH"

RUN pip install --no-cache-dir poetry


# Copy only Poetry-related files first (to leverage Docker's caching mechanism)
COPY pyproject.toml poetry.lock ./
RUN poetry install 

COPY . .

# Command to run the bot
CMD ["poetry", "run", "python", "bot.py"]
