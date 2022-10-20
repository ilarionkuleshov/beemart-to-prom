# Beemart to Prom

## Installation (Python3.8)
```
git clone https://github.com/ilarionkuleshov/beemart-to-prom.git
cd src/
poetry install
```
Configure `.env`, `beemart.bat` according to `.env.example`, `beemart.bat.example` respectively.

## Usage
- Manually (in `src/` directory): `poetry run python main.py`
- From Windows Task Scheduler: specify the program (script) to run - `beemart.bat`