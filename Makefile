VENV_NAME := venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
SERVICE_FILE := dakuf.service
SYSTEMD_DIR := /etc/systemd/system

check_root:
	@if [ "$$(id -u)" -ne 0 ]; then \
		echo "This script must be run as root"; \
		exit 1; \
	fi
	@echo "Running as root"

install: check_root create_venv enable_service

create_venv:
	python3 -m venv $(VENV_NAME)
	source $(VENV_ACTIVATE)
	pip install -r requirements.txt

enable_service:
	cp $(SERVICE_FILE) $(SYSTEMD_DIR)
	systemctl enable $(SERVICE_FILE)

clean:
	rm -rf $(VENV_NAME)

.PHONY: install create_venv enable_service clean check_root