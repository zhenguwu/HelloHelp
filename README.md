# HelloHelp

## Usage

### 1) Clone Repository

### 2) Install Dependencies

```cd HelloHelp```

```python -m venv env```

```source env/bin/activate```

```brew install geos```

```pip install -r requirements.txt```

Note: Make sure to rerun the 'source' command whenever the terminal is restarted

### 3) Set up env
Create file named ".env" and put OPENAI_API_KEY = YOUR_API_KEY_HERE

### 3 A) Start Server Locally

```flask --app=HHServer run```

### 3 B) Start Server in Prod

```flask --app=HHServer --host=0.0.0.0 run```