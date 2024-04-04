# My Ta-da Blog API


### Features

- **Retrieve Articles**: Retrieve the list of all articles or a specific article.
- **Create Article**: Add a new article to the list.
- **Update Article**: Update an existing article.
- **Delete Article**: Delete an article from the list.

### Model

The `Article` model represents a blog article in the database.

- `id`: Unique identifier for the article (UUID).
- `title`: Title of the article.
- `created_at`: Date and time when the article was created.
- `updated_at`: Date and time when the article was last updated.
- `content`: Content of the article.
- `status`: Status of the article (draft or published).

## Usage

To run the API, follow the appropriate steps based on your preferred method:

### Docker

1. Create a `.env` file in the project root directory:

    ```plaintext
    # .env
    DATABASE_URL=postgresql+asyncpg://user:password@db/postgres
    USE_SQLITE=false
    ```

    Adjust the `DATABASE_URL` variable to match your PostgreSQL database configuration. Set `USE_SQLITE` to `true` if you want to use SQLite instead.

2. Build and run the Docker image:

    ```bash
    docker-compose up
    ```
   Once the Docker containers are up and running, you can access the interactive documentation endpoint at the following URL:

    [Interactive Documentation (Doc)](http://0.0.0.0:8001/docs)

   If you want to run tests, execute the following command:
   ```bash
   docker-compose exec app pytest tada
   ```

### Python Executable

1. There is already a `.whl` file in the `dist` directory, you can install the package directly:

    ```bash
    pip install dist/tada-0.1.0-py3-none-any.whl
    ```

    Alternatively, you can rebuild a fresh package using Poetry:

    ```bash
    poetry build
    ```

    This will generate a new `.whl` file in the `dist` directory that you can install.

2. Set the environment variables:

    ```bash
    export DATABASE_URL="postgresql://user:password@localhost/db_name"
    export USE_SQLITE=false
    ```

    Adjust the `DATABASE_URL` variable to match your PostgreSQL database configuration. Set `USE_SQLITE` to `true` if you want to use SQLite instead.

3. Run the command to start the API:

    ```bash
    run-my-blog
    ```
    This command will start the API server.
