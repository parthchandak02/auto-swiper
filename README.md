# Auto-Swiper

Automate swiping on Hinge using Bluestacks or any Android emulator.

![Auto-Swiper](logo.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Virtual Environment](#virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Contributing](#contributing)

## Introduction

Auto-Swiper is a tool designed to automate the process of swiping on Hinge using Bluestacks or any Android emulator. Follow the steps below to set up and run the script.

## Features

- Automatically swipe and like profiles on Hinge
- Customizable messages for interactions
- Logging of all activities

## Installation

### Prerequisites

- Python 3.6 or higher
- Bluestacks or any Android emulator with Hinge installed

### Virtual Environment

Create and activate a virtual environment:

python3 -m venv venv

#### Activate Virtual Environment

For macOS/Linux:

source venv/bin/activate

For Windows:

venv\\Scripts\\activate

### Installing Dependencies

Install the required packages:

pip install -r requirements.txt

## Usage

Run the script with the following command:

python main.py

## Disclaimer

This software is intended for educational and personal use only. Use of this software to automate interactions on third-party platforms, such as Hinge and Bluestacks, may violate their terms of service. The author does not condone or encourage any activities that violate the terms of service of any platform.

Users are responsible for their own actions when using this software. The author assumes no liability for any misuse of this software or any consequences resulting from its use.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Configuration

You can customize the behavior of the script by editing the config.yaml file.

default_wait_time_secs: 3
max_likes: 200
pun_array:
  - "Add joke here"
  - "Add pun here"

For more detailed usage and customization, please refer to the [Wiki](https://github.com/yourusername/auto-swiper/wiki).

---

For any questions, feel free to open an issue or contact the author directly.

Happy Swiping!
