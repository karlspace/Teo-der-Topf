# Project "Teo der Topf" - A Child's Interactive Learning and Tinkering Companion

"Teo der Topf" is an interactive, engaging, and educational child's tinkering project that employs a Raspberry Pi, sensors, and display technology to create a fun and instructive playmate. This project aims to provide children with hands-on experience in programming, hardware setup, and IoT (Internet of Things) concepts while maintaining a playful and enjoyable experience.

![Final Build Example](./_Hardware/Assembly/Final%20Build%20Example.png)

## Project Overview

At the heart of "Teo der Topf" lies a Raspberry Pi connected to various sensors that measure parameters such as soil moisture, temperature, and ambient light. These measurements are then translated into emotive responses displayed on the Raspberry Pi's screen, represented by an animated "face".

For instance, if the ambient light level is low, "Teo" may display a "sleepy" face. If the soil's moisture level drops, indicating that a plant may need water, "Teo" might exhibit a "thirsty" face. Through this personification, children can interact and engage with technology in a more intuitive and fun way.

Furthermore, the project integrates with the Home Assistant smart home system, allowing further interaction and exploration of IoT concepts. Children can see how the measurements "Teo" collects can be used and accessed in other ways, such as through a smart home dashboard.

## Key Learning Outcomes
* Programming Concepts: By working with the provided Python scripts and libraries, children will grasp basic programming concepts like variables, conditionals, functions, and more.
* Hardware Setup: Children will learn about different types of sensors, how they work, and how to connect them to the Raspberry Pi.
* IoT Concepts: By integrating with Home Assistant, children will be introduced to IoT concepts and how individual devices can contribute to a larger, interconnected system.
* Data Interpretation: As they interact with "Teo", children will learn to interpret sensor data, correlating physical world conditions with numerical data and visual feedback.

## Hands-On and Fun!

"Teo der Topf" combines education and entertainment, fostering an environment where learning is an enjoyable adventure. As children tinker, experiment, and play with "Teo", they are not only developing valuable skills but also nurturing curiosity, creativity, and a love for technology.

# Software Setup

## Raspberry Pi OS installation

Before setting up the software scripts, you need to install the Raspberry Pi OS image on a microSD card. This can be done using the Raspberry Pi Imager, available for download from the [official Raspberry Pi website](https://www.raspberrypi.org/software/).

### Steps:

1. Download and install the Raspberry Pi Imager on your computer.

2. Insert the microSD card into your computer.

3. Open Raspberry Pi Imager and choose the OS from the list presented (select Raspberry Pi OS Lite 32bit).

4. As we're setting up a headless Raspberry Pi Zero W, you'll need to set up WiFi and login credentials during the image writing process. To do so, click on `Ctrl + Shift + X` on your keyboard to open the advanced options in Raspberry Pi Imager. Provide your WiFi network's SSID, password, and set your desired hostname. Also, set up the user account and password.

5. Select the microSD card you have inserted.

6. Click on 'WRITE' and wait for the process to complete.

Once the image has been written to the microSD card, safely remove it and insert it into your Raspberry Pi Zero W. Power up the Raspberry Pi. 

The device should boot up and connect to your WiFi network using the credentials you provided. As the Raspberry Pi Zero W is a headless device (i.e., without a dedicated display), you can connect to it remotely using SSH.

After you've established an SSH connection to your Raspberry Pi, you can proceed with the application setup as described below.

## Application download and setup

Once you have successfully connected to your Raspberry Pi Zero W via SSH, you can use the one-click setup script to automatically download and configure the entire "Teo der Topf" application.

### Option 1: One-Click Setup (Recommended)

The easiest way to install the application is using the one-click setup script. This script will automatically:
- Update the package lists
- Install Git (if not already installed)
- Clone the latest version of the repository
- Run the complete application setup

You can execute the one-click setup using one of the following commands:

**Using curl:**
```bash
curl -sSL https://raw.githubusercontent.com/karlspace/Teo-der-Topf/main/other/one-click-setup.sh | bash
```

**Using wget:**
```bash
wget -O - https://raw.githubusercontent.com/karlspace/Teo-der-Topf/main/other/one-click-setup.sh | bash
```

The script will download the project to `~/teotopf` directory and automatically run the `ApplicationSetup.sh` script to complete the installation.

### Option 2: Manual Setup

If you prefer to set up the application manually, follow these steps:

1. **Install Git** (if not already installed):
   ```bash
   sudo apt-get update
   sudo apt-get install -y git
   ```

2. **Clone the repository**:
   ```bash
   mkdir -p ~/teotopf
   cd ~/teotopf
   git clone --depth 1 https://github.com/karlspace/Teo-der-Topf.git .
   ```

3. **Run the application setup**:
   ```bash
   chmod +x ApplicationSetup.sh
   ./ApplicationSetup.sh
   ```

> **Note:** that the steps under "Configuration and usage information" are optional and you can already start after the steps in this section. The soil moisture sensor must be calibrated, but the project will work without calibrating it (lower accuracy).

## Important First Run Information

When you start the application for the first time, the initial setup includes the generation of image assets required for the operation. This process involves shifting and potentially rotating a large number of image files, which is a computationally intensive task.

Due to this, **the first start-up may take up to 30 minutes** depending on the processing power of your hardware.

Please be patient and allow the application to complete this one-time setup process. After this initial setup, the generated assets will be stored and reused in subsequent runs, significantly speeding up the startup time.

> **Note:** Do not interrupt the setup process as this may lead to incomplete file generation and could cause issues in the application's operation.

## Information about configuration and useage

This software setup consists of three bash scripts: `ApplicationSetup.sh`, `app.sh`, and `stop_app.sh`. These scripts are used for configuring the operating system, setting up the necessary dependencies, and controlling the execution of a Python application.

### Overview

1. **ApplicationSetup.sh**: This script is responsible for the primary setup of the application environment. It performs package installation, configures autologin, sets up the application's autostart, and adjusts specific operating system parameters. 

    Steps:
    - Installs necessary packages
    - Sets up autologin for the current user
    - Configures the operating system
    - Creates an autostart entry for the application
    - Reboots the system (if approved by the user)

2. **app.sh**: This script is used to start the Python application manually. 

    Steps:
    - Checks if the application is already running to prevent duplicate instances
    - Installs Python dependencies (if necessary)
    - Starts the Python application

3. **stop_app.sh**: This script is used to stop the Python application that is running in another shell (console autostart usually).

    Steps:
    - Identifies the PID of the running Python application
    - Sends a SIGTERM signal to the application
    - Checks for successful termination and notifies if the application fails to stop

### Useage

1. Run `ApplicationSetup.sh` script for initial setup.
    ```bash
    bash ./ApplicationSetup.sh
    ```
    Approve the reboot when prompted.

2. After reboot, you can start the application manually using `app.sh`. Be aware that it is automatically starting already after the reboot.
    ```bash
    ./app.sh
    ```

3. To stop the application, use the `stop_app.sh` script. That is required if the application is already running after reboot in local console and you want start it using ssh shell, for example.
    ```bash
    ./stop_app.sh
    ```
   
With this setup, the application will automatically start upon boot due to the autostart configuration set up by `ApplicationSetup.sh`. Manual start and stop controls are also available through `app.sh` and `stop_app.sh` respectively.

This setup ensures a streamlined deployment and execution process for the application, making it easier for users and systems to handle the application lifecycle effectively.

### .env Configuration File

The `.env` file is a simple configuration file that sets environment variables for your application. This file is used to store key-value pairs, with each pair representing an environment variable and its value.

Here's a description of the settings you can configure in the `.env` file for this project:

#### Logging Settings

- `LOG_LEVEL`: Sets the level of logging detail. Possible values include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

#### Sensor Settings

- `SOIL_MAX`: The maximum value read by the capacitive soil sensor. This value depends on your calibration and the GAIN setting (in this case, GAIN = 1.0).
- `SOIL_MIN`: The minimum value read by the capacitive soil sensor. Again, this depends on your calibration and the GAIN setting.
- `SOIL_DRY_ABOVE`: A threshold value for the soil sensor. If the sensor reads a value above this, the soil is considered "dry".
- `SOIL_WET_BELOW`: A threshold value for the soil sensor. If the sensor reads a value below this, the soil is considered "wet".
- `TEMPERATURE_COLD_BELOW`: A threshold temperature in degrees Celsius. If the sensor reads a temperature below this, it is considered "cold".
- `TEMPERATURE_HOT_ABOVE`: A threshold temperature in degrees Celsius. If the sensor reads a temperature above this, it is considered "hot".
- `NIGHT_MODE_BELOW`: A threshold light level in Lux. If the sensor reads a light level below this, it is considered "night mode".

#### Telemetry Settings

- `HOMEASSISTANT_ENABLED`: Enables or disables integration with Home Assistant. Set this to `True` to enable, and `False` to disable.
- `HOMEASSISTANT_ID`: The identifier for the device in Home Assistant.
- `HOMEASSISTANT_MQTT_SERVER`: The IP address or hostname of your Home Assistant MQTT server.
- `HOMEASSISTANT_MQTT_USER`: The username for the MQTT server.
- `HOMEASSISTANT_MQTT_PASSWORD`: The password for the MQTT server.

Here's a sample `.env` file with some example values:

```plaintext
### Logging ###
LOG_LEVEL=DEBUG

### Sensors ###

# Capacitive Sensor Values, depending on Calibration (GAIN = 1.0)
SOIL_MAX=18600
SOIL_MIN=6900
SOIL_DRY_ABOVE=13500
SOIL_WET_BELOW=9500

# Temperature in Celsius
TEMPERATURE_COLD_BELOW=18.0
TEMPERATURE_HOT_ABOVE=24.0

# Light in Lux
NIGHT_MODE_BELOW=5.00

### Telemetry ###
HOMEASSISTANT_ENABLED=False
HOMEASSISTANT_ID=TeoTopf
HOMEASSISTANT_MQTT_SERVER=10.20.30.40
HOMEASSISTANT_MQTT_USER=teotopf
HOMEASSISTANT_MQTT_PASSWORD=yourpassword
```

Remember not to share your `.env` file publicly, especially if it contains sensitive information like passwords or API keys. Always add it to your `.gitignore` file if you're using Git version control.

# Hardware Setup

## Required Components

This project requires the following hardware:
- Raspberry Pi Pico W (any model with 40 GPIO pins)
- A display with ILI9341 controller and resolution of 320x240px
- BH1750 light sensor
- BMP280 barometric pressure sensor
- ADS1115 analog-to-digital converter for the soil sensor 
- Capacitive soil sensor

## SPI Communication

The display communicates with the Raspberry Pi over the SPI protocol. Make sure SPI communication is enabled on your Raspberry Pi. You can enable it using `raspi-config` under "Interfacing Options".

### Raspberry Pi to ILI9341 Display Pinout

This is the pinout connection from Raspberry Pi to the ILI9341 display.

| Raspberry Pi       | ILI9341 Display |
|--------------------|-----------------|
| GPIO 23 (PIN 16)   | LED             |
| VCC (PIN 17)       | VCC             |
| GPIO 24 (PIN 18)   | RESET           |
| SPI0 MOSI (PIN 19) | MOSI            |
| GND (PIN 20)       | GND             |
| SPI0 MISO (PIN 21) | MISO            |
| GPIO 25 (PIN 22)   | D/C             |
| SPI0 SCLK (PIN 23) | SCK             |
| SPI0 CE0 (PIN 24)  | CS              |

Please refer to the Raspberry Pi pinout diagram for the pin numbers.

**Important:** Make sure to connect all the pins correctly to avoid any damage to your Raspberry Pi or the display. Always power off the Raspberry Pi when connecting or disconnecting the display to prevent any accidental short circuits.

# I2C Connection

## I2C Communication

The sensor devices communicate with the Raspberry Pi over the I2C protocol. Ensure I2C communication is enabled on your Raspberry Pi. You can enable it using `raspi-config` under "Interfacing Options".

Once all your connections are established and your I2C is enabled, you should be able to see all connected devices by typing the following command in the terminal: `i2cdetect -y 1`

Each device will have a different address, so ensure you've noted the addresses of each device for further use in your code. The addresses are usually provided in the device datasheets.

### Raspberry Pi to BH1750, ADS1115, BMP280 Pinout

Here is the pinout connection from Raspberry Pi to the BH1750, ADS1115, and BMP280 devices:

| Raspberry Pi     | BH1750 | ADS1115 | BMP280 |
|------------------| ------ | ------- | ------ |
| 3.3V (PIN 1)     | VCC    | VDD     | VCC    |
| GND (PIN 6 or 9) | GND    | GND     | GND    |
| SDA (PIN 3)      | SDA    | SDA     | SDA    |
| SCL (PIN 5)      | SCL    | SCL     | SCL    |

Again, refer to the Raspberry Pi pinout diagram for the pin numbers.

**Important:** Ensure all the connections are correctly established. Always power off the Raspberry Pi when connecting or disconnecting these devices to prevent any accidental short circuits.

![Raspberry Pi pinout diagram](./_Hardware/Raspberry%20Pi%20Zero%20W/Raspberry%20PI,%20GPIO%20Overview.png)

# Useful information

## Python Envorinment

After changing the code, you need to update the requirements.txt file for automatic package installation: `pip3 freeze > requirements.txt`.

## Notes

### Sensors
* The A/D sensor need to be calibrated. My values for a "normal" plant are predefined. 
* If you like, you can use the ADS1115 A/D converter for the other sensors. For this you have to update the Python code accordingly. It has a total of 4 analog inputs. You can also use an analog temperature and light sensor instead of the I2C sensors. This lowers the cost a bit.
* The standard I2C addresses for the sensors are used. If other addresses are to be used, the source code must be adapted accordingly.

### Home Assistant
The integration of Home Assistant is intended for the older kids (parents) who are helping the younger ones with the build. It's an advanced feature and requires additional knowledge about Home Assistant and MQTT protocol. It's perfectly okay to skip this part if you are working with your kids. The plant pot will work perfectly fine without this feature.

![Home Assistant Sensors](./_Hardware/HomeAssistant/Sensor%20Data%20–%20Home%20Assistant.png)

## Kown Issues

### 3D Model

* The hole for the display is a bit too big. You can see the frame. It must be reduced by about 5mm in diameter.
* The 3D print in my printing is cut open on the inside at the inner bottom of the planter, which was split. So that one can reduce support material. This is not included in the 3D model, but only in my print file (3MF).

### Components

#### Display
* The Display is not centered on the PCB. The Images are centered on the Display. To Display the Image in the Center of the Hole a software extension is in display class to compensate that.

## Implemented Emotions

![Happy](./_Hardware/Assembly/Implemented%20Emotions.png) 

## Impressions

![Assembling the Items 1](./_Hardware/Assembly/Assembling%20the%20Items%20(1).jpg)

![Assembling the Items 2](./_Hardware/Assembly/Assembling%20the%20Items%20(2).jpg)

![Assembling the Items 3](./_Hardware/Assembly/Assembling%20the%20Items%20(3).jpg)

![Assembling the Items 4](./_Hardware/Assembly/Assembling%20the%20Items%20(4).jpg)

![Assembling the Items 5](./_Hardware/Assembly/Assembling%20the%20Items%20(5).jpg)

![Assembling the Items 6](./_Hardware/Assembly/Assembling%20the%20Items%20(6).jpg)

![Assembling the Items 7](./_Hardware/Assembly/Assembling%20the%20Items%20(7).jpg)

![Assembling the Items 8](./_Hardware/Assembly/Assembling%20the%20Items%20(8).jpg)

![Assembling the Items 9](./_Hardware/Assembly/Assembling%20the%20Items%20(9).jpg)

![Assembling the Items 10](./_Hardware/Assembly/Assembling%20the%20Items%20(10).jpg)

![Assembling the Items 11](./_Hardware/Assembly/Assembling%20the%20Items%20(11).jpg)

![Assembling the Items 12](./_Hardware/Assembly/Assembling%20the%20Items%20(12).jpg)

![Assembling the Items 13](./_Hardware/Assembly/Assembling%20the%20Items%20(13).jpg)

# Disclaimer

This project is a child's tinkering project. Both the hardware and software are not designed with production readiness, fault resistance, or maintainability in mind. This project is provided "as is," without any warranty of any kind, either expressed or implied. 

By using the provided code and hardware design, you acknowledge and agree that you are doing so at your own risk. The author of this project shall not be held liable for any damages or injuries resulting from the use or inability to use this project.

This is not a production-ready product that can be certified for mass production and sale. It's designed for educational purposes only. Always exercise caution and supervision when children are involved in DIY projects.

Unfortunately, the provided programming or source code does not reach the required standard in terms of quality and security necessary for productive deployment. There exist a number of shortcomings and deficits that affect the optimal functionality, efficiency, and above all, security of the code in a productive environment. A detailed examination and improvement of the code is required to ensure that it meets the strict criteria for quality and security expected in software development. Only in this way can smooth and secure application be guaranteed, without leading to unwanted disruptions or security risks that could negatively impact the overall project and its efficiency. Therefore, we recommend a thorough review and corresponding improvement of the code before deploying it in a productive context.
