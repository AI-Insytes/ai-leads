# AI Leads

## Installation

1. Clone project repository
1. Navigate to the cloned repository if not already
1. Install [Python](https://www.python.org/) if not already
1. Create and activate a virtual environment

    `python3 -m venv .venv`

    `source .venv/bin/activate` (Linux/Mac)

    `source .venv/Scripts/activate` (Windows)

1. Install dependencies

    `pip install -r requirements.txt`

1. Install [Playwright dependencies](https://playwright.dev/python/docs/intro) *(only required if you have not used Playwright on your system before)*

    `playwright install`

## Run App

Leads data will be saved in the `leads_and_messages` directory as a csv file

### CLI

From the root of the installed directory run the main module `python -m app.app`

### GUI

From the root of the installed directory run the main module `python -m app.gui`

## Project Members

* [Lana Zumbrunn](https://github.com/lana-z)
* [Caleb Hemphill](https://github.com/kaylubh)
* [Rhett Chase](https://github.com/rhettchase)  
* [Felix Traveras](https://github.com/f-taveras)
* [Immanuel Shin](https://github.com/ImmanuelShin)

## Lead Generation App MVP

An app to assist with finding people of interest:

* User input (to command line)
* Stretch: Generate top keywords for the target via AI
* Search capability based on user input of the internet or specific app [LinkedIn public profiles]
* Database storage of results
  * Name
  * Relevant information about person/company
  * Way to find them LinkedIn profile link (public)
* AI generated messaging suggested to user
  * Based on information gathered from search  
  * limited by specified length

***Pain Points:***

* Eases the difficulty of reaching the “early adopters” (first people interested in buying the product) in early stage of business growth
* Reduces time for each outreach

## Project Documentation

* [User Stories](/Proj-Mngmt/userstories.md)
* [Software Requirements](/Proj-Mngmt/requirements.md)
* [Domain Model](/Proj-Mngmt/domain-model.md)
* [Wireframe](/Proj-Mngmt/wireframe.md)
