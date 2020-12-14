TOPIC = "test.mosquitto.org"

# Temperature and umidity publish interval (seconds)
DATA_PUBLISH_INTERVAL = 5

# Data amount needed to start processing (reset after)
DATA_PROCESS_AMOUNT = 5

# Percentage of mean temperature which will be sent to the air conditioner
AIR_CONDITIONER_PERCENTAGE = 0.8

# Humidity below this level will turn the humidifier on
HUMIDIFIER_LOWER_THRESHOLD = 50

# Humidity above this level will turn the humidifier off
HUMIDIFIER_UPPER_THRESHOLD = 80