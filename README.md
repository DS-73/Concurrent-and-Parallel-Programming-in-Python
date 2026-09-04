# Concurrent and Parallel Programming in Python

This repository contains examples and exercises demonstrating concurrent and parallel programming concepts in Python, covering threading, multiprocessing, synchronization, and pipeline architectures.

## Topics Covered

| # | File | Concept | Description |
|---|------|---------|-------------|
| 01 | `01.Without-Thread.py` | Sequential Execution | Baseline sequential CPU-bound and I/O-bound tasks |
| 02 | `02.With-Thread.py` | Threading Basics | Same tasks with `threading.Thread` for concurrency |
| 03 | `03.Class-Example.py` | Worker Pattern | Custom `Thread` subclasses (`SquaredSumWorker`, `SleepyWorker`) |
| 04 | `04.StockPrice.py` | Web Scraping + Threads | Scrape S&P 500 symbols, fetch prices from Yahoo Finance |
| 05 | `05.0PSQL.py` | Database Connectivity | PostgreSQL connection test with psycopg2/SQLAlchemy |
| 06 | `05.1PSQLFinance.py` | Producer-Consumer Pipeline | Complete ETL: Wiki → Yahoo Finance → PostgreSQL |
| 07 | `06.0YamlReader.py` | Config Parsing | Read YAML pipeline definition as JSON |
| 08 | `06.1YamlReader-Class.py` | Dynamic Pipeline Executor | Class-based pipeline runner with dynamic imports |
| 09 | `07.Locking.py` | Thread Synchronization | `threading.Lock` for race condition prevention |
| 10 | `08.0MultiProcessing-Threads.py` | GIL Limitation | CPU-bound threading (limited by GIL) |
| 11 | `08.1MultiProcessing-Processes.py` | True Parallelism | CPU-bound multiprocessing (bypasses GIL) |
| 12 | `08.2Queues.py` | Inter-Process Communication | `multiprocessing.Queue` for work distribution |
| 13 | `09.Pool.py` | Process/Thread Pools | `Pool.map()` vs manual threads for CPU-bound work |
| 14 | `10.Partial.py` | `functools.partial` | Binding arguments for `Pool.map()` |
| 15 | `11.StarMap.py` | `Pool.starmap` | Multiple arguments with process pools |

## Workers Package (`Workers/`)

Reusable thread-based worker classes:

| File | Class | Purpose |
|------|-------|---------|
| `PostgresWorker.py` | `PostgresMasterScheduler`, `PostgresWorker` | Database write workers with queue consumption |
| `SleepyWorker.py` | `SleepyWorker` | I/O-bound sleep simulation (daemon support) |
| `SquaredSumWorker.py` | `SquaredSumWorker` | CPU-bound computation worker |
| `WikiWorker.py` | `WikiWorker` | Wikipedia S&P 500 symbol scraper |
| `YahooFinance.py` | `YahooFinance` | Yahoo Finance price fetcher with throttling |

## Pipeline Configuration (`pipelines/`)

| File | Description |
|------|-------------|
| `wiki_yahoo_scraper_pipeline.yaml` | Declarative pipeline: Wiki → Yahoo Finance → PostgreSQL |

## Key Concepts Demonstrated

### Threading vs Multiprocessing
- **Threading** (`threading`): Good for I/O-bound tasks (network, disk). Limited by GIL for CPU work.
- **Multiprocessing** (`multiprocessing`): True parallelism for CPU-bound tasks. Separate memory spaces.

### Synchronization Primitives
- **Lock** (`threading.Lock`): Mutual exclusion for shared state
- **Semaphore** (`threading.Semaphore`): Resource counting (rate limiting)
- **Queue** (`multiprocessing.Queue`): Thread/process-safe FIFO communication

### Patterns
- **Worker Thread**: Subclass `Thread`, override `run()`, auto-start
- **Producer-Consumer**: Queue between stages, sentinel for shutdown
- **Thread Pool**: `Pool.map()` / `Pool.starmap()` for batch parallelism
- **Pipeline**: Chained stages with queues, configurable via YAML

## Requirements

```bash
pip install requests beautifulsoup4 lxml psycopg2-binary sqlalchemy python-dotenv pyyaml
```

## Environment Variables (`.env`)

Required for PostgreSQL examples:

```env
PSQL_USER=your_username
PSQL_PASS=your_password
PSQL_HOST=your_host
PSQL_PORT=your_port
PSQL_DB=your_database
PSQL_MODE=require
```

## Running Examples

```bash
# Sequential baseline
python 01.Without-Thread.py

# Threading basics
python 02.With-Thread.py

# Worker classes
python 03.Class-Example.py

# Stock price scraping
python 04.StockPrice.py

# Database test
python 05.0PSQL.py

# Full pipeline
python 05.1PSQLFinance.py

# YAML config inspection
python 06.0YamlReader.py

# Locking demo
python 07.Locking.py

# GIL vs multiprocessing
python 08.0MultiProcessing-Threads.py
python 08.1MultiProcessing-Processes.py

# Queue communication
python 08.2Queues.py

# Pool comparison
python 09.Pool.py

# Partial/starmap
python 10.Partial.py
python 11.StarMap.py
```

## Learning Progression

1. **Basics** (01-03): Thread creation, worker pattern, timing comparison
2. **Real-world I/O** (04): Web scraping with concurrent requests
3. **Data Persistence** (05): Database integration with producer-consumer
4. **Configuration** (06): Declarative pipeline definitions
5. **Synchronization** (07): Locks for thread safety
6. **CPU Parallelism** (08-09): Multiprocessing vs threading, pools
7. **Advanced Patterns** (10-11): Argument binding, multiple arguments

## License

Educational examples for learning concurrent programming in Python.