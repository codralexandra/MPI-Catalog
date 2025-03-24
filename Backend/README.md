# Setting Up the Python Environment

## 1. Setting Up a Python Environment

### Using Anaconda (Recommended)

1. Download and install Anaconda from [here](https://www.anaconda.com/products/distribution).
2. Create a new environment:
    ```bash
    conda create --name myenv python=3.13.0
    ```
3. Activate the environment:
    ```bash
    conda activate myenv
    ```

## 2. Installing Requirements

1. Ensure your environment is activated.
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## 3. Creating the `.env` File

1. In the root directory of your project, create a file named `.env`.
2. Add your database URL to the `.env` file:
    ```env
    DB_URL=your_database_url_here
    ```

## 4. Running the Application

1. Ensure your environment is activated.
2. Run the main application:
    ```bash
    python main.py
    ```

# Running tests
```terminal
python test_file_name.py
```