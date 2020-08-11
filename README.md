# DHT22 Temperature and Humidity Monitor

Simple Python app (microservice) to read Temperature and Humidity from a DHT22 temperature sensor connected to a Raspberry PI via GPIO. The program writes output to stdio or Redis server on a Raspberry Pi running Raspbian or Ubuntu Server. It is intended to be run from systemd as a service.

requires a running Redis server, Python 3.7+, Redis-py, e.g., pip install redis.

## installation as a systemd service

Assuming you are running this as `pi` user, with a virtual environment setup under `~/.venvs/default/`, and your script is installed under `~/Projects/dht22_temp_monitor`,
add the following to your `/etc/systemd/system` folder, name it something sensible like `dht22-temperature-monitor.service`:

```
[Unit]
Description=Temperature Monitor Service
After=network.target

[Service]
Type=simple
User=ubuntu
ExecStart=/home/pi/.venvs/default/bin/python /home/pi/Projects/dht22_temp_monitor/dht22_temp_monitor.py -r localhost -f 30
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

After installation, run `sudo systemctl daemon-reload` to pick up the changes, then `sudo systemctl start dht22-temperature-monitor.service` (assuming that's the name you gave it).

You can be sure it's running by checking `sudo systemctl status dht22-temperature-monitor` and `sudo journalctl -u dht22-temperature-monitor` for details.

When satisfied that everything is working as intended, you can permanently install the temperature monitor by entering `sudo systemctl enable dht22-temperature-monitor.service`.

## License

Do what you want with this.
