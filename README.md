# Talk-to-my-Projects

Interact with my projects to quickly assess their value and relevance to your academic or business needs. Check it out here: [talk-to-aman-projects.streamlit.app](https://talk-to-aman-projects.streamlit.app/)

## About

"Talk-to-my-Projects" is a repository that allows you to explore and understand the potential applications of my research works and projects through interactive conversations. The Streamlit app and LLaMA-3 language model enable users to determine if any of my projects align with their requirements efficiently.

## Key Features

- Curated list of my research works and projects
- Intuitive conversational interface powered by Streamlit and LLaMA-3-7B-Chat
- Quick assessment of project relevance and value to user needs
- Suitable for both academic and business use cases

### Demo Images
![base](/images/base.png)
![base](/images/federated-learning.png)
![base](/images/keywords.png)
![base](/images/differential-privacy.png)

## Method/Implementation:

![flow-chart](/images/flow_chart.png)

### Efficient Keyword Extraction
- The `extract_keywords_custom` function utilizes Aman's library [AdaptKeyBERT](https://github.com/AmanPriyanshu/AdaptKeyBERT) model with the 'all-MiniLM-L6-v2' configuration for keyword extraction.
- It extracts keyphrases of 1-2 ngrams, excludes common stop words, and returns the top 10 most relevant keywords.
- This optimization ensures focused and meaningful keyword extraction from project descriptions.

### Caching and Performance Enhancement
- The `load_projects` function is decorated with `@st.cache` to cache the loaded projects dataframe.
- Caching avoids unnecessary reloading of the projects data on each app refresh, improving performance.
- A spinner is displayed during the loading process to provide a smooth user experience.

### Semantic Similarity Ranking
- The `rank_projects` function employs the SentenceTransformer model to generate embeddings for user keywords and project keywords.
- Cosine similarity is computed between the user and project embeddings to determine relevance scores.
- Projects are then ranked based on their similarity scores, enabling users to quickly identify the most relevant projects.

### Memory-Efficient Session State Management
- Streamlit's session state is utilized to store and manage user messages, context TLDRs, and the selected OpenAI model.
- By leveraging session state, the app maintains a consistent conversation flow without consuming excessive memory.
- The app also imposes a limit of 10 messages per user to ensure fair usage and prevent resource exhaustion.

### Contextual Project Information
- The app intelligently incorporates the top 3 most relevant project TLDRs into the conversation context.
- This allows the LLaMA-3 model to provide more targeted and informative responses based on the user's interests.
- The context is dynamically updated based on the user's input, ensuring the conversation remains relevant and engaging.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/AmanPriyanshu/Talk-to-my-Projects.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the necessary API keys and secrets in the Streamlit secrets configuration.

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

5. Start exploring and interacting with my projects through the intuitive conversational interface.

## Contributions and Feedback

Contributions, suggestions, and feedback are welcome! If you have any ideas to enhance the app or encounter any issues, please feel free to open an issue or submit a pull request on the GitHub repository. Thank you for your interest in my research works and projects. I hope "Talk-to-my-Projects" proves to be a valuable resource in exploring the potential applications of my work to your academic or business needs.

## Other Usage Details

### Attribution

* If you use or share this work, please provide attribution with the following information:

_"Talk to my Projects" by Aman Priyanshu, licensed under CC BY-NC 4.0. Available at: https://github.com/AmanPriyanshu/Talk-to-my-Projects_

* When sharing adaptations of this work, please include a statement indicating that changes were made, such as:

_This work is adapted from "Talk to my Projects" by Aman Priyanshu, licensed under CC BY-NC 4.0. Original work available at: https://github.com/AmanPriyanshu/Talk-to-my-Projects_

### License
This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

TL;DR: My projects are licensed under CC BY-NC 4.0, which means you can freely use them for non-commercial purposes with attribution. If you're considering commercial use or are unsure whether your use case requires permission, please refer to the [LICENSE](/LICENSE) file or reach out to me via [email](amanpriyanshusms2001@gmail.com)—I'm always happy to chat!

* _I've learned my lesson from being a bit too naive in the past. I didn't include licenses for some of my earlier projects, and as a result, they were used commercially without me knowing about it. Don't get me wrong, I would've been cool with it, but I would've loved to be involved or at least kept in the loop, you know? That's why I'm planning on adding a license to each of my projects from now on. It's nothing major, just a quick heads up email if you're planning on using my work for commercial purposes._
