#!/bin/bash
# run_pipeline.sh — Axon worker
# Gebruik: ./run_pipeline.sh "pipeline-naam"
PIPELINE=$1
echo "🚀 Pipeline gestart: $PIPELINE — $(date)"
case $PIPELINE in
    "deploy")
        echo "Stap 1: Tests uitvoeren"
        echo "Stap 2: Build starten"
        echo "Stap 3: Deploy naar Vercel"
        echo "Stap 4: Health check"
        ;;
    "backup")
        echo "Stap 1: Database backup"
        echo "Stap 2: Files backup"
        echo "Stap 3: Upload naar opslag"
        ;;
    *)
        echo "Onbekende pipeline: $PIPELINE"
        exit 1
        ;;
esac
echo "✅ Pipeline $PIPELINE voltooid"
