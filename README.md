## Part 1: Initial Project Ideas

### 1. Project Idea 1: Basic Customer Service Bot for a Fictional Company
- **Description:** A chatbot that can answer frequently asked questions about a hypothetical product or service (e.g., a "Zoom-like" video conferencing app, a local restaurant, or an online clothing store).
  
- **Rule-Based Approach:**  
  - Keywords: Identify keywords in user input (e.g., "price," "shipping," "hours," "menu," "returns").
  - Predefined Responses: Map these keywords to specific, pre-written answers.
  - Clarification: If a query is ambiguous, the bot asks clarifying questions.
  - Fallback: A general "I'm sorry, I don't understand" message if no rules match.
### 2. Project Idea 2: Simple Adventure Game Narrator
- **Description:** A text-based adventure game where the "AI" narrates the environment and responds to player commands based on predefined rules.
  
- **Rule-Based Approach:**  
  - Location Descriptions: Rules describing different rooms/areas.
  - Object Interactions: Rules for what happens when a player tries to "use," "take," or "examine" an object in a specific location.
  - Commands: Recognize commands like "go north," "look around," "take key," "use sword."
  - Inventory Management: Track items the player is carrying.

### 3. Project Idea 3: Movie/Book Recommender based on Genres and User Preferences
- **Description:** Recommend movies or books based on a user's stated preferences or a few initial choices.  
- **Rule-Based Approach:**  
  - Genre Matching: If a user likes "action" and "sci-fi," recommend movies tagged with both.
  - Director/Author Matching: If a user likes a particular director or author, recommend their other works.
  - Keyword Matching: If a user expresses interest in "space exploration" or "detective stories," recommend items with those keywords in their descriptions.
  - Exclusion Rules: Avoid recommending items the user has already seen/read or explicitly disliked.

### **Chosen Idea:** Simple Adventure Game Narrator  
**Justification:** I chose this project because to me the project make the most sense. I am not highly versed in python, but I do have a fair amount of experience in C++/C# and Kotlin so of the three project I chose the one that seemed the most involved without being overly complex. This project gave me great insight into what it takes to learn using AI and what the future capabilities are. It allowed me to collaborate with the AI in ways that I am both completely familiar and unfamiliar at the same time. 

---

## Part 2: Rules/Logic for the Chosen System

The **Simple Adventure Game Narrator** system will follow these rules:

1. **Go:**  
   - **IF** The direction is a valid and unlocked exit. → **Change current_location to the new location.**
   - - **IF** The direction is locked or does not exist. → **Inform the player they cannot go that way.**

2. **Look:**  
   - **IF** No specific item is mentioned. → **Describe the current location and any visible items.**
   - **IF** A specific item is mentioned and is present. → **Describe the item in detail.**  

3. **Take:**  
   - **IF** The item is present and can be picked up. → **Add the item to inventory and remove it from the location.**
   - **IF** The item is not present or cannot be picked up. → **Inform the player they cannot take the item.**  

4. **Use:**  
   - **IF** The player has the item, and it has a specific purpose. → **Trigger the corresponding event (unlock a door, defeat a monster) and update the game_flags.**
   - **IF** The player has the item, but it has no effect.→ **Inform the player that nothing happens.**
   - **IF** The player does not have the item.→ **Inform the player they do not have the item.**

5. **Inventory:**  
   - **IF** The inventory is not empty. → **List the items the player is carrying.**
   - **IF** The inventory is empty. → **Inform the player their inventory is empty**  

6. **Other:**  
   - **IF** The command is not recognized. → **Inform the player that the command is not understood and suggest valid actions.**

---

## Part 3: Rules/Logic for the Chosen System

Sample input and output: 

AI: "You are in a dimly lit cave. To the north, you see a faint light. There is a rusty sword on the ground."

User: "take sword"

AI: "You pick up the rusty sword."

User: "go north"

AI: "You emerge from the cave into a sunlit forest. A winding path leads east."

---

## Part 4: Reflection

So overall the reason I chose to go with the idea for the Adventure Game Narrator is because of the amount of actual coding that I knew it would require. I have a background in C++/C# and Kotlin, but I have essentially zero experience in Python. Knowing this, I wanted to utilize the AI particularly Gemini and GPT to help me learn as much as I could on Python within one project. I had a pretty good idea of how I would go about it but being about to work with the AI to pitch it ideas or logic and have it turn around and show me the best way to go about it while using an unfamiliar language. This gave me a ton of insight into the future of learning through AI and just how informative it can be. AI is far from perfect, that is for sure. The main thing that I noticed is that the AI likes to do things one way and even when that does not work just keep trying changes or fixes until it does work. I found this to be the case more with Gemini than I did GPT. There seem to be many cases with Gemini that rather than just look at what I was asking it to do and try a different way, it would just essentially act convinced that I was doing something wrong. I had one case where Gemini would tell me that I was spelling a word wrong when that was clearly not that case, and it was not until I told it where in the logic to look did it realize what the issue was. Overall, I was happy with the experience, and I am excited to see what AI will bring us in the future.

### Project Overview:
This project involved designing a practical, rule-based system to narrate a play through a basic Adventure Game. The system uses logical conditions (Look, Go, Take, Use, Inventory, Other) to evaluate user-provided input to determine the progression of the game.

### Challenges:
- **Asking Questions To AI**  
  I learned that it is not always what you ask the AI, but how you ask the AI. You have to be clear and concise.