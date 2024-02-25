# cs411-finalproject

Project Description:
We decided to make a website that allows users to enter their interests and get suggested travel itineraries. We are going to use the Chatgpt API to take the user's interests and construct a travel itinerary for them based on their input. We will use the database to store previous user-generated itineraries.

Product Requirements:

Product Goal: Create a web interface for personalized travel itineraries based on a users preferences
Non-goal: Intelligently convert a users personality into locations, restaurants, and flights they would like
Non-functional requirement: Security
Use OAuth to log into Google
Securely store locations and itineraries in a SQL database 
Non-functional requirement: Usability 
ChatGPT API will be used to make recommendations personalized to the user
Users won’t have to search to plan their itinerary. The app will provide direct links to book flights and find locations. 

Product Management: 
Theme: Enhancing the travel planning experience using AI and user customization.
Epic: Website Beta
User Story 1: As a newcomer to a city, I want to easily create a trip itinerary based on my preferences.
Task: Implement Chat GPT API to automate planning process
Ticket 1: Take user inputs of trip preferences: (cuisine, trip style, etc.)
Ticket 2: Use the user inputs to create a chat gpt prompt and return the chat gpt output to the user in the UI. Also return flights and Yelp reviews of destinations that ChatGPT recommended. 
Automate the prompt creation process and the output creation process

User Story 2: As a returning user, I want to be able to customize the itinerary.
Task: Implement itinerary customization feature
Ticket 1: Design UI for itinerary customization in Python and Javascript
Ensure the interface allows for easy addition, removal, and modification of itinerary items
Ticket 2: Develop the itinerary customization logic
Implement the backend logic to support adding, removing, and modifying items within itineraries
Implement a DB with Flask and SQL
