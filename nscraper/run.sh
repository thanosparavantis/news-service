#!/bin/bash
cd /home/ubuntu/news-service/nscraper
source .venv/bin/activate
python run_instant.py
deactivate
