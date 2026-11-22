"""Runs each uplink's speed test in turn and pushes the results to the Pushgateway.

The speedtest exporter runs a test whenever it is scraped, so Prometheus cannot choose
when tests happen. This scheduler calls every uplink's exporter one after another at
fixed times, so two tests never compete for the CPU, and stores the results in the
Pushgateway, which Prometheus scrapes instead of the exporters.
"""
import http.client
import logging
import os
import time
import urllib.request

EXPORTER_URL_TEMPLATE = os.environ.get(
    "EXPORTER_URL_TEMPLATE", "http://uplink-{uplink_name}-probe:9798/metrics")
PUSHGATEWAY_URL_TEMPLATE = os.environ.get(
    "PUSHGATEWAY_URL_TEMPLATE", "http://pushgateway:9091/metrics/job/speedtest/uplink/{uplink_name}")
EXPORTER_TIMEOUT_SECONDS = 150  # the exporter itself gives up on a test after 90 seconds
PUSHGATEWAY_TIMEOUT_SECONDS = 10
SPEEDTEST_METRIC_PREFIX = "speedtest_"
SPEEDTEST_LINE_PREFIXES = (
    SPEEDTEST_METRIC_PREFIX,
    "# HELP " + SPEEDTEST_METRIC_PREFIX,
    "# TYPE " + SPEEDTEST_METRIC_PREFIX,
)


def seconds_until_next_run(interval_seconds, offset_seconds, now_epoch_seconds):
    """Seconds until the next interval boundary (aligned to UTC) plus the offset."""
    elapsed_in_interval = (now_epoch_seconds - offset_seconds) % interval_seconds
    return interval_seconds - elapsed_in_interval


def speedtest_lines_only(exporter_metrics):
    """Keeps the speedtest_* samples and their HELP/TYPE lines, drops process metrics."""
    speedtest_lines = [
        metrics_line for metrics_line in exporter_metrics.splitlines()
        if metrics_line.startswith(SPEEDTEST_LINE_PREFIXES)
    ]
    return "\n".join(speedtest_lines) + "\n"


def fetch_speedtest_metrics(uplink_name):
    exporter_url = EXPORTER_URL_TEMPLATE.format(uplink_name=uplink_name)
    with urllib.request.urlopen(exporter_url, timeout=EXPORTER_TIMEOUT_SECONDS) as exporter_response:
        return speedtest_lines_only(exporter_response.read().decode("utf-8"))


def push_speedtest_metrics(uplink_name, speedtest_metrics):
    """Replaces the uplink's group in the Pushgateway with the latest results."""
    pushgateway_request = urllib.request.Request(
        PUSHGATEWAY_URL_TEMPLATE.format(uplink_name=uplink_name),
        data=speedtest_metrics.encode("utf-8"),
        method="PUT",
        headers={"Content-Type": "text/plain; version=0.0.4"},
    )
    with urllib.request.urlopen(pushgateway_request, timeout=PUSHGATEWAY_TIMEOUT_SECONDS):
        return


def run_uplink_speedtest(uplink_name):
    try:
        push_speedtest_metrics(uplink_name, fetch_speedtest_metrics(uplink_name))
    except (OSError, http.client.HTTPException) as speedtest_error:
        logging.error("speed test for uplink %s failed: %s", uplink_name, speedtest_error)
        return
    logging.info("speed test for uplink %s pushed", uplink_name)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    uplink_names = [uplink_name for uplink_name in os.environ["UPLINK_NAMES"].split(",") if uplink_name]
    interval_seconds = int(os.environ["SPEEDTEST_INTERVAL_SECONDS"])
    offset_seconds = int(os.environ["SPEEDTEST_OFFSET_SECONDS"])
    logging.info(
        "testing uplinks %s every %d s, %d s after each interval boundary",
        ", ".join(uplink_names), interval_seconds, offset_seconds,
    )
    while True:
        time.sleep(seconds_until_next_run(interval_seconds, offset_seconds, time.time()))
        for uplink_name in uplink_names:
            run_uplink_speedtest(uplink_name)


if __name__ == "__main__":
    main()
