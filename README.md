
# Settings

You can adjust the settings using the `setting.toml` file. An example is provided. 
The following table describes the individual setting variables. Note the Dynaconf-compatible notation with the double underscore.

| Variable                  | Description                                                                                    | Default         | Optional           | Example                         |
|---------------------------|------------------------------------------------------------------------------------------------|-----------------|--------------------|---------------------------------|
| ILO__URL                  | URL or IP address of the iLO                                                                   | -               |                    | "http://192.168.178.5"          |
| ILO__USER                 | User name to authenticate to iLO                                                               | -               |                    | "my_user_name"                  |
| ILO__PASSWORD             | Password to authenticate to iLO                                                                | -               |                    | "secret_pw"                     |
| ILO__POLL_INTERVAL        | Determines how often the data from the iLO is polled (minutes)                                 | 5               | :heavy_check_mark: | 3                               |
| ILO__TEMPERATURE__PATH    | API path where to find the temperature information                                             | -               |                    | "/redfish/v1/Chassis/1/Thermal" |
| ILO__TEMPERATURE__EXCLUDE | Sensor data which should be excluded from the report (e.g. not connected sensors)              | []              | :heavy_check_mark: | ["sensor01", "name03"]          |
| ILO__SYSTEM__PATH         | API path where to find the system information                                                  | -               |                    | "/redfish/v1/systems/1"         |
| MQTT__URL                 | URL of the MQTT broker                                                                         | -               |                    | "192.168.178.3"                 |
| MQTT__PORT                | Port on which the MQTT broker is listening                                                     | 1883            | :heavy_check_mark: | 8883                            |
| MQTT__CLIENT_ID           | Name which the client describe itself to the broker                                            | -               | :heavy_check_mark: | "my_client_name"                |
| MQTT__BASE_TOPIC          | Base topic under which the iLO data will be published                                          | None            | :heavy_check_mark: | "my_ilo"                        |
| MQTT__KEEPALIVE           | Keep alive interval for the MQTT connection (seconds)                                          | 60              |                    | 10                              |
| MQTT__USER                | User name to authenticate to the MQTT broker                                                   | -               | :heavy_check_mark: | "my_mqtt_user"                  |
| MQTT__PASSWORD            | Password to authenticate to the MQTT broker                                                    | -               | :heavy_check_mark: | "another_secret"                |
| MQTT__DELAY               | Sets the delay between the individual sensor values to be sent to avoid package loss (seconds) | 1               | :heavy_check_mark: | 0.5                             |
| MQTT__WEBSOCKET           | Flag to use websockets instead of standard TCP connection                                      | False           | :heavy_check_mark: | True                            |
| LOGGING__FILE             | Specifies the file destination for the logger                                                  | config/ilo4.log | :heavy_check_mark: | "some_file_path"                |
| LOGGING__LEVEL            | Specifies the log level                                                                        | INFO            | :heavy_check_mark: | "WARNING"                       |
| LOGGING__SIZE_KB          | Max size of the log file before it gets rotated (KB)                                           | 500             | :heavy_check_mark: | 1000                            |

# API Reference
- Temperatures: https://hewlettpackard.github.io/ilo-rest-api-docs/ilo4/?python#thermal
- System: https://hewlettpackard.github.io/ilo-rest-api-docs/ilo4/?python#computersystem

