Valorant Match Tracker

A structured Python console application for tracking Valorant match performance, calculating advanced statistics, and visualising KD trends over time.

This project focuses on clean menu-driven architecture, data persistence using CSV, and performance analysis.

Overview

The Valorant Match Tracker allows users to:

Record match details (map, agent, kills, deaths, assists)

Store matches persistently using CSV

Calculate performance metrics (KD, KAD)

View stats by map

View stats by agent

Detect performance streaks

Visualise KD trends with graphs

Edit and delete match records safely

The application is designed with modular functions to keep logic readable, reusable, and maintainable.

Technologies Used

Python 3

csv module for data persistence

matplotlib for performance visualisation

Structured functional program design

Project Structure
valorant-match-tracker/
│
├── main.py
└── README.md


The matches.csv file is automatically created when the first match is added.

How to Run

Install Python 3.x

Install required dependency:

pip install matplotlib


Run the application:

python main.py


Follow the on-screen menu options.

Features
Match Management

Add new matches

Edit existing matches

Delete matches

View last N matches

Performance Metrics

KD (Kill/Death ratio)

KAD (Kill + Assist / Death ratio)

Map-based performance breakdown

Agent-based performance breakdown

Performance streak detection

Automatic match labelling based on rolling baseline

Data Handling

Automatic CSV creation

Safe file rewriting for edits and deletes

Defensive handling of division-by-zero

Outlier clipping for graph stability

Visualisation

KD over time graph

Average KD reference line

Percentile-based clipping to prevent distortion

Technical Highlights

Defensive ratio calculations to prevent runtime errors

Rolling baseline scoring system for streak classification

Percentile-based outlier clipping for clearer graphs

Modular function structure for maintainability

Structured menu-driven application flow

Lessons Learned

This project strengthened my understanding of:

Structured program design

File handling and persistent storage

Data aggregation and statistical calculations

Defensive programming

Graph generation using matplotlib

Designing user-friendly console applications

It serves as a foundation for transitioning into database-driven and API-based backend systems.

Future Improvements

Replace CSV storage with SQL database

Convert to REST API backend

Add a web-based dashboard interface

Implement advanced analytics and performance modelling
