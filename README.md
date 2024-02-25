# cs411-finalproject

# Project Description

## Overview

We decided to create a website that allows users to enter their interests and get suggested travel itineraries. Our approach leverages the ChatGPT API to take the user's interests and construct a travel itinerary for them based on their input. Additionally, we will use a database to store previous user-generated itineraries.

# Product Requirements

## Product Goal

- **Create a web interface for personalized travel itineraries based on a user's preferences.**

## Non-goal

- **Intelligently convert a user's personality into locations, restaurants, and flights they would like.**

## Non-functional Requirements

### Security

- Use OAuth to log into Google.
- Securely store locations and itineraries in a SQL database.

### Usability

- The ChatGPT API will be used to make recommendations personalized to the user.
- Users won’t have to search to plan their itinerary. The app will provide direct links to book flights and find locations.

# Product Management

## Theme

- **Enhancing the travel planning experience using AI and user customization.**

## Epic

- **Website Beta**

## User Stories

### User Story 1

**As a newcomer to a city, I want to easily create a trip itinerary based on my preferences.**

#### Task

- Implement ChatGPT API to automate the planning process.

#### Tickets

- **Ticket 1:** Take user inputs of trip preferences (cuisine, trip style, etc.).
- **Ticket 2:** Use the user inputs to create a ChatGPT prompt and return the ChatGPT output to the user in the UI. Also, return flights and Yelp reviews of destinations that ChatGPT recommended. Automate the prompt creation process and the output creation process.

### User Story 2

**As a returning user, I want to be able to customize the itinerary.**

#### Task

- Implement itinerary customization feature.

#### Tickets

- **Ticket 1:** Design UI for itinerary customization in Python and JavaScript. Ensure the interface allows for easy addition, removal, and modification of itinerary items.
- **Ticket 2:** Develop the itinerary customization logic. Implement the backend logic to support adding, removing, and modifying items within itineraries. Implement a DB with Flask and SQL.
