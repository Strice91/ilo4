
# Settings

You can adjust the settings using the `setting.toml` file. An example is provided. 
The following table describes the individual setting variables. Note the Dynaconf-compatible notation with the double underscore.

| Variable                  | Description                                                                                   | Default         | Optional           |
|---------------------------|-----------------------------------------------------------------------------------------------|-----------------|--------------------|
| ILO__URL                  | URL or IP address of the iLO                                                                  | -               |                    |
| ILO__USER                 | User name to authenticate to iLO                                                              | -               |                    |
| ILO__PASSWORD             | Password to authenticat to iLO                                                                | -               |                    |
| ILO__POLL_INTERVAL        | Determins how often the data from the iLO is polled (minutes)                                 | 5               | :heavy_check_mark: |
| ILO__TEMPERATURE__PATH    | API path where to find the temperature information                                            | -               |                    |
| ILO__TEMPERATURE__EXCLUDE | Sensor data which should be excluded from the report (e.g. not connected sensors)             | []              | :heavy_check_mark: |
| ILO__SYSTEM__PATH         | API path where to find the system information                                                 | -               |                    |
| MQTT__URL                 | URL of the MQTT broker                                                                        | -               |                    |
| MQTT__PORT                | Port on which the MQTT broker is listening                                                    | 1883            | :heavy_check_mark: |
| MQTT__CLIENT_ID           | Name which the client describe itself to the broker                                           | -               | :heavy_check_mark: |
| MQTT__BASE_TOPIC          | Base topic under which the iLO data will be published                                         | None            | :heavy_check_mark: |
| MQTT__KEEPALIVE           | Keep alive interval for the MQTT connection (seconds)                                         | 60              |                    |
| MQTT__USER                | User name to authenticate to the MQTT broker                                                  | -               | :heavy_check_mark: |
| MQTT__PASSWORD            | Password to authenticate to the MQTT broker                                                   | -               | :heavy_check_mark: |
| MQTT__DELAY               | Sets the delay between the indivdual sensor values to be sent to avoid package loss (seconds) | 1               | :heavy_check_mark: |
| LOGGING__FILE             | Specifies the file destination for the logger                                                 | config/ilo4.log | :heavy_check_mark: |
| LOGGING__LEVEL            | Specifies the log level                                                                       | INFO            | :heavy_check_mark: |
| LOGGING__SIZE_KB          | Max size of the log file before it gets rotated (KB)                                          | 1000            | :heavy_check_mark: |

# API Reference
- Temperatures: https://hewlettpackard.github.io/ilo-rest-api-docs/ilo4/?python#thermal
- System: https://hewlettpackard.github.io/ilo-rest-api-docs/ilo4/?python#computersystem

