#!/bin/bash

SERVICE_WORKER="celery-worker-dev"
SERVICE_BEAT="celery-beat-dev"

start_services() {
    echo "Starting Celery Worker and Beat services..."
    sudo systemctl start $SERVICE_WORKER
    sudo systemctl start $SERVICE_BEAT
    echo "Services started."
}

stop_services() {
    echo "Stopping Celery Worker and Beat services..."
    sudo systemctl stop $SERVICE_WORKER
    sudo systemctl stop $SERVICE_BEAT
    echo "Services stopped."
}

restart_services() {
    echo "Restarting Celery Worker and Beat services..."
    sudo systemctl restart $SERVICE_WORKER
    sudo systemctl restart $SERVICE_BEAT
    echo "Services restarted."
}

status_services() {
    echo "Checking the status of Celery Worker and Beat services..."
    sudo systemctl status $SERVICE_WORKER
    sudo systemctl status $SERVICE_BEAT
}

case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        status_services
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
