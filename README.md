
# CANalyzer Mimic Pro    
![Build Status](https://github.com/kiranj26/CANalyzer-Mimic-Pro/actions/workflows/build.yml/badge.svg)
![Code Quality](https://img.shields.io/badge/code%20quality-pylint-brightgreen)](https://www.pylint.org/)


Welcome to CANalyzer Mimic Pro! This repository is a personal project to create a tool inspired by professional CAN analyzers, designed for visualizing and analyzing CAN bus logs.

## Purpose

The purpose of this repository is to:
- Provide a user-friendly tool for CAN bus log analysis.
- Allow filtering and plotting of CAN messages by ID.
- Offer a visualization of CAN data bytes over time.

## Features

- Load CAN log files in TXT format.
- Filter and plot CAN messages by ID.
- Visualize CAN data bytes over time.

## Documentation

The full documentation for this project can be found [here](https://kiranj26.github.io/CANalyzer-Mimic-Pro/).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/kiranj26/CANalyzer-Mimic-Pro.git
    cd CANalyzer-Mimic-Pro
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r src/requirements.txt
    ```

## Usage

1. Run the main script:
    ```bash
    python src/canalyzer_mimic.py
    ```

2. Use the UI to select a CAN log file, enter a CAN ID, and plot the data.

## Example

![UI Screenshot](docs/images/ui_screenshot.png)

## Code Quality

We use `pylint` for static code analysis to catch potential issues early.

## Documentation

We use Doxygen to generate detailed documentation for our code.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](docs/contributing.md) before getting started.

## Contact

Kiran Jojare  
Embedded Software Engineer  
Phone: 720-645-6212  
Email: kijo7257@colorado.edu

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Happy Coding! 🚀
