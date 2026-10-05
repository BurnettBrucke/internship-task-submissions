# Day 8 - Microservices & Production Backend

## Overview

Production-style microservice system built with FastAPI.

## Architecture

Client
    |
    v
Gateway Service
    |
    v
Processing Service
    |
    +--> PostgreSQL
    |
    +--> Redis / ARQ Worker

## Services

### Gateway Service

Public-facing API.

### Processing Service

Internal job processing API.

### Worker

Background job execution using ARQ.

## Infrastructure

- FastAPI
- PostgreSQL
- Redis
- ARQ
- Docker
- OpenTelemetry
- Pytest

## Status

Phase 0 - Project Bootstrap