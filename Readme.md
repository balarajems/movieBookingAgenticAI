               
# Movie Booking AI System

## Overview
This project is an AI-powered movie booking assistant using **AutoGen Selector Group Chat** to intelligently route user queries. The system integrates multiple agents to handle movie recommendations, reservations, and membership validation.

---

## Architecture Overview

               
               
                     +--------------------------------------+
                     |          Flask Backend API          |
                     +--------------------------------------+
                                   |
           ---------------------------------------------------
           |                         |                       |
 +--------------------+    +--------------------+   +-------------------+
 |  Movie Booking    |    |  Movie Search      |   |  Membership Check  |
 |  Reservation API  |    |  Bing Search API   |   |  Semantic Kernel   |
 +--------------------+    +--------------------+   +-------------------+
           |                         |                       |
           |                         |                       |
+--------------------+      +--------------------+   +----------------------+
| MovieReservation  |      | MovieRecommendation |   | MembershipValidation |
|     Agent        |      |      Agent         |   |        Agent        |
+--------------------+      +--------------------+   +----------------------+
           \                         |                      /
            \                        |                     /
             \------------------+-----------------------+
                                |
               +--------------------------------+
               |  AutoGen Selector Group Chat  |
               |  (Routes Queries to Agents)  |
               +--------------------------------+
                                |
                  +-------------------------------+
                  |        User Input Layer       |
                  | (Flask API receives queries) |
                  +-------------------------------+

---

## Components

### 1 **User Input Layer (Flask Backend API)**
- Accepts and processes user requests.
- Routes queries to the **AutoGen Selector Group Chat**.

### 2 **AutoGen Selector Group Chat**
- Dynamically selects and routes queries to the appropriate agent.

### 3 **Agents**
| Agent                    | Responsibility                                      |
|--------------------------|----------------------------------------------------|
| **MovieReservationAgent**  | Handles movie ticket reservations. |
| **MovieRecommendationAgent** | Fetches movie recommendations using **Bing Search API**. |
| **MembershipAgent** | Verifies user eligibility for booking via **Azure Semantic Kernel**. |

### 4 **External Services**
| Service                 | Functionality                                      |
|--------------------------|----------------------------------------------------|
| **Movie Booking API**     | Processes and confirms movie reservations. |
| **Bing Search API**      | Retrieves movie information for recommendations. |
| **Semantic Kernel (Azure Functions)** | Checks user membership and eligibility. |

---

## How It Works

1. **User makes a request** via the Flask API (e.g., *"Recommend a movie"* or *"Book me a ticket for Inception at 7 PM"*).
2. **AutoGen Selector Group Chat** routes the request to the relevant agent:
   - **Recommendation requests** → MovieRecommendationAgent (uses Bing Search).
   - **Booking requests** → MovieReservationAgent (checks membership, then books the movie).
   - **Membership validation** → MembershipValidationAgent (calls Azure Semantic Kernel).
3. **Agents use external services** to fetch movie data, verify membership, and process reservations.
4. **Final response** is sent back to the user with relevant details.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Flask
- AutoGen
- Azure OpenAI API
- Bing Search API
- Azure Semantic Kernel

