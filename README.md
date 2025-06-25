# MoodSync - Your Personal Mood Tracking Companion

![MoodSync Logo](https://via.placeholder.com/150?text=MoodSync)

## About MoodSync

**Unlock a Deeper Understanding of Your Emotional World with MoodSync.**

In today's fast-paced life, truly connecting with our emotions can be a challenge. MoodSync is more than just a mood tracker; it's your dedicated partner in navigating the complexities of your emotional landscape. Imagine having a clear map of your feelings, understanding what truly lifts you up, and recognizing a-ha moments that lead to lasting positive change.

With MoodSync, you're not just logging moods – you're embarking on a journey of self-discovery. Our intuitive platform empowers you to:
*   **Capture Your Emotional Nuances:** Effortlessly record your moods, thoughts, and the activities that color your day.
*   **Reveal Hidden Patterns:** Transform raw data into meaningful insights, helping you see the connections between your lifestyle and your feelings.
*   **Cultivate Resilience & Joy:** Identify your unique triggers and discover personalized strategies to nurture your mental wellbeing.

MoodSync is designed to help you build a stronger, more insightful relationship with yourself, paving the way for a more balanced and fulfilling life. **Start your journey to emotional clarity today.**

## Features

### 🌈 **Track Your Moods Effortlessly**
Log your feelings with a simple, intuitive interface. Add detailed notes, associate activities, and rate your mood to capture the full context of your emotional state.

### 📊 **Visualize Your Emotional Landscape**
Gain clarity through insightful charts and visualizations. See how your moods fluctuate over time, identify trends, and understand the bigger picture of your emotional wellbeing.

### 💡 **Smart, Personalized Insights**
MoodSync's intelligent backend analyzes your data to provide personalized suggestions and observations. (Future: These insights will become more sophisticated as the AI components are further developed).

### 🗣️ **Reflect and Grow with Comments**
Add comments to your mood entries to reflect on your feelings, track your progress, and understand your emotional triggers better. This creates a valuable dialogue with your past self.

### 🧠 **AI-Powered Support (Backend Foundation)**
The backend is built with AI-driven features in mind. Currently, it provides personalized motivational messages and habit suggestions based on your mood history and patterns.

## Why MoodSync?

Understanding your emotions is the first step to improving them. MoodSync helps you:

*   **Build Self-Awareness:** Recognize patterns in your moods and what influences them.
*   **Identify Triggers:** Pinpoint situations, activities, or thoughts that impact your emotional state.
*   **Cultivate Positive Habits:** Discover and reinforce activities that genuinely boost your wellbeing.
*   **Manage Stress & Anxiety:** By understanding your patterns, you can develop more effective coping strategies.
*   **Track Progress:** See how your emotional landscape changes over time, celebrating growth and navigating challenges.

## Getting Started

### For Users

MoodSync is currently in active backend development. A user-facing application (web and mobile) is planned for a future phase. Stay tuned for updates!

### For Developers (Backend Focus)

This section provides details for developers interested in understanding, contributing to, or extending the MoodSync backend.

#### Prerequisites
*   Python 3.8+ (preferably 3.11 as used in Dockerfile)
*   Django (version specified in `requirements.txt`, currently >=3.2,<4.0)
*   pip (Python package installer)
*   Virtualenv (recommended for managing project dependencies)
*   Git

#### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/mood_tracker.git
    cd mood_tracker
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    All Python dependencies are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Copy the example environment file and customize it:
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file. At a minimum, you'll need to ensure `DJANGO_SECRET_KEY` is set. You can generate one using:
    ```bash
    python generate_secret_key.py
    ```
    This script will also update your `.env` file with the new key.
    **Important:** Add `.env` to your `.gitignore` file if it's not already there.

5.  **Apply Database Migrations:**
    MoodSync uses SQLite by default for local development. Migrations define the database schema.
    ```bash
    python manage.py makemigrations tracker
    python manage.py migrate
    ```

6.  **Create a Superuser (Optional but Recommended):**
    This allows access to the Django admin interface.
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The API will typically be available at `http://127.0.0.1:8000/`.

#### Backend Architecture Overview

The MoodSync backend is built using the **Django REST framework (DRF)**, providing a robust and scalable foundation for the API.

*   **Project Structure:**
    *   `mood_tracker/`: The main Django project directory.
        *   `mood_tracker/settings.py`: Core project settings.
        *   `mood_tracker/urls.py`: Root URL configuration.
    *   `tracker/`: The primary Django app containing the core logic for mood tracking, comments, and AI suggestions.
        *   `models.py`: Defines the database schema (Mood, Comment, etc.).
        *   `views.py`: Contains the logic for handling API requests and responses (APIViews, Generic Views).
        *   `serializers.py`: Defines how complex data types (like model instances) are converted to and from native Python datatypes that can then be easily rendered into JSON.
        *   `urls.py`: URL routing for the `tracker` app.
        *   `admin.py`: Configuration for the Django admin interface.
        *   `tests/`: Contains automated tests.
            *   `test_comments_ai.py`: Specific tests for comments and AI suggestion features.
        *   `tests.py`: General tests for the tracker app.
        *   `middleware.py`: Custom middleware, e.g., for API request/response logging.
    *   `manage.py`: Django's command-line utility.
    *   `requirements.txt`: Lists project dependencies.
    *   `.env`: Stores environment-specific variables (e.g., `SECRET_KEY`, `DEBUG` status). **Should not be committed to version control.**
    *   `Dockerfile` & `docker-compose.yml`: For containerization with Docker (optional for local development but good for deployment).

*   **Authentication:**
    *   Supports both **Token Authentication** (legacy DRF tokens) and **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.
    *   Endpoints for registration, login, logout, and password change are provided.
    *   Custom JWT authentication (`tracker/authentication.py`) can be extended for additional validation.

    *   **Obtaining Authentication Tokens:**
        *   The primary way to get authentication tokens is by sending a `POST` request to the `/api/login/` endpoint with your `username` and `password`.
        *   Upon successful login, the response will include:
            *   `token`: Your legacy DRF authentication token.
            *   `access`: Your JWT access token.
            *   `refresh`: Your JWT refresh token.
        *   See `api_examples.md` for a `curl` example of the login request and response.
        *   You can then use either the DRF token (prefixed with `Token `) or the JWT access token (prefixed with `Bearer `) in the `Authorization` header for subsequent authenticated requests.

*   **Database:**
    *   Default: SQLite3 (for ease of local development).
    *   Configurable via `DATABASE_URL` in `.env` for PostgreSQL (as shown in `docker-compose.yml`).
    *   Schema changes are managed through Django migrations.

*   **API Documentation:**
    *   Auto-generated API documentation is available via Swagger and ReDoc UI.
        *   Swagger: `/swagger/`
        *   ReDoc: `/redoc/`
    *   Manual API examples are provided in `api_examples.md`.

*   **Testing:**
    *   Tests are written using Django's `APITestCase`.
    *   Key test files: `tracker/tests.py` and `tracker/tests/test_comments_ai.py`.
    *   A custom test runner script `test_runner.py` is available for more granular control over test execution.
    *   To run all tests for the `tracker` app:
        ```bash
        python manage.py test mood_tracker.tracker
        ```
    *   Or use the custom runner:
        ```bash
        python test_runner.py
        ```
        (Add `--reset-db` to recreate the test database before running tests).

*   **Leveraging AI in Development:**
    Modern AI assistants, such as GitHub Copilot, can be valuable tools during development for tasks like code completion, generating boilerplate, suggesting solutions to problems, and assisting with documentation. Exploring and utilizing such tools can enhance productivity and code quality.

*   **AI-like Features (Backend Implementation):**
    *   The "AI" suggestions (motivation, habits) are currently implemented using rule-based logic and template responses within `tracker/views.py` (e.g., `MotivationSuggestionAPIView`, `HabitImprovementAPIView`). This provides a functional baseline.
    *   Sentiment analysis is performed using the `TextBlob` library when mood entries with notes are created or updated.
    *   **Future Evolution:** The long-term vision is to replace these template-based systems with more sophisticated machine learning models for nuanced and personalized insights (see "Next Steps").

#### Key Backend Components:

*   **`tracker.models.Mood`**: Stores individual mood entries, including mood type, notes, rating, activities, and calculated sentiment.
*   **`tracker.models.Comment`**: Stores user comments linked to specific mood entries.
*   **`tracker.serializers`**:
    *   `MoodSerializer`, `CommentSerializer`: Handle serialization and validation for mood and comment data.
    *   `UserSerializer`, `UserRegisterSerializer`, `PasswordChangeSerializer`: Handle user-related data and authentication processes.
*   **`tracker.views`**:
    *   Authentication views (`UserRegisterAPIView`, `UserLoginAPIView`, etc.).
    *   Mood CRUD views (`MoodCreateAPIView`, `MoodHistoryAPIView`, `MoodDetailAPIView`).
    *   Comment views (`CommentListCreateAPIView`, `CommentDetailAPIView`).
    *   AI Suggestion views (`MotivationSuggestionAPIView`, `HabitImprovementAPIView`, `MoodPatternAnalysisAPIView`).
*   **`tracker.urls`**: Defines all API endpoints for the `tracker` application.
*   **`tracker.middleware.APIDebugMiddleware`**: Logs API request and response details for debugging purposes.

## Project Status

**Current Status: Backend API Fully Operational**

The backend for MoodSync is feature-complete and robust, providing a comprehensive API for all core functionalities.

**What's Working (Backend):**
*   Secure user registration and authentication (Token and JWT).
*   Full CRUD (Create, Read, Update, Delete) operations for mood entries.
*   Functionality to add, view, update, and delete comments on mood entries.
*   Personalized "AI-like" suggestions for motivation and habit improvement based on user data.
*   Mood pattern analysis (time of day, day of week).
*   Sentiment analysis of mood notes using `TextBlob`.
*   Data export in JSON and CSV formats.
*   Admin-only endpoint for cross-user sentiment analysis.
*   Comprehensive API documentation (Swagger & ReDoc).
*   Extensive automated tests ensuring API reliability.
*   Caching mechanisms for performance optimization on certain endpoints.
*   Customizable environment through `.env` file.
*   Docker support for containerized deployment.

**Next Steps for the Project:**
*   **Frontend Development:** Design and implement a user-friendly web application that consumes the backend API.
*   **Mobile App Implementation:** Develop native or cross-platform mobile applications for iOS and Android.
*   **Advanced AI Integration:**
    *   **Transition from Templates:** Evolve the current rule-based suggestion features (`MotivationSuggestionAPIView`, `HabitImprovementAPIView`) to use actual machine learning models.
    *   **NLP for Deeper Insights:** Implement NLP models for more advanced analysis of mood notes and comments. This could include theme extraction, more nuanced sentiment analysis, or even generating reflective prompts for users.
    *   **Personalized Habit Correlation:** Develop models to identify statistically significant correlations between user activities, logged moods, and notes to offer more data-driven habit suggestions.
    *   **Predictive Capabilities:** Explore models that might predict future mood states or suggest interventions based on learned patterns (requires significant data and ethical considerations).

    *   **Potential AI Model APIs for Integration (Free/Freemium Tiers):**
        When considering a move from template-based suggestions to more sophisticated AI, several external APIs offer access to pre-trained models. Many have free tiers suitable for development, experimentation, and low-traffic applications. Always check their current terms of service and pricing, as these can change.

        1.  **Hugging Face Inference API:**
            *   **What it offers:** Access to thousands of open-source pre-trained models for NLP tasks like text generation, summarization, sentiment analysis, question answering, and more.
            *   **Relevance to MoodSync:** Could be used for generating more dynamic motivational messages, summarizing user notes/comments, advanced sentiment analysis, or identifying themes in user reflections.
            *   **Considerations:** The free tier has rate limits. For higher usage, you might need to move to paid tiers or self-host open-source models from Hugging Face.

        2.  **OpenAI API (e.g., GPT models):**
            *   **What it offers:** Powerful models for text generation, understanding, and conversation (e.g., GPT-3.5, GPT-4).
            *   **Relevance to MoodSync:** Excellent for generating creative and context-aware motivational content, providing empathetic responses, or helping users reframe negative thoughts based on their input.
            *   **Considerations:** Typically offers initial free credits for new users. Beyond that, it's a paid service, though costs can be managed for low-volume use. API key management and cost monitoring are crucial.

        3.  **Google Cloud AI (Vertex AI / Natural Language API):**
            *   **What it offers:** A suite of AI services, including Natural Language API for sentiment analysis, entity recognition, content classification, and syntax analysis. Vertex AI provides a broader platform for custom model training and deployment.
            *   **Relevance to MoodSync:** Could provide more granular sentiment scores than TextBlob, identify key entities (people, places, events) in mood notes, or classify notes into broader emotional categories.
            *   **Considerations:** Google Cloud often has a "Free Tier" that includes a certain amount of free usage per month for many services. Exceeding these limits incurs costs.

        4.  **Perspective API (from Jigsaw, part of Google):**
            *   **What it offers:** Analyzes text for perceived impact, such as toxicity, insult, profanity, etc.
            *   **Relevance to MoodSync:** If user comments or notes are public or shared, this could be useful for moderation or for users to understand the potential impact of their own written reflections if they choose to analyze them.
            *   **Considerations:** Free for many use cases, especially non-commercial, up to a certain query-per-second (QPS) limit.

        **General Integration Steps:**
        *   Sign up for the API service and obtain an API key.
        *   Store the API key securely (e.g., in your `.env` file, not in version control).
        *   Install the necessary Python client library for the API (e.g., `openai`, `google-cloud-language`, `requests` for Hugging Face).
        *   Modify your Django views (e.g., `MotivationSuggestionAPIView`) to:
            *   Prepare the input data (e.g., user's recent notes).
            *   Make an HTTP request to the external AI API.
            *   Process the API's JSON response.
            *   Return the AI-generated suggestion to your app's frontend.
        *   Implement error handling for API calls (e.g., network issues, rate limits, API errors).

*   **Deployment to Production:** Set up a scalable production environment, considering the potential resource needs for AI model serving.

## Privacy First

Your emotional data is personal and sensitive. MoodSync's backend is designed with privacy as a core principle:
*   **Authentication Required:** All API endpoints (except for documentation and registration/login) require valid authentication tokens.
*   **Data Isolation:** Users can only access and modify their own data. Permissions are strictly enforced at the API level.
*   **Secure Password Handling:** Passwords are hashed and salted using Django's robust security mechanisms.
*   **(Future) Self-Hosted Option:** We aim to provide a straightforward way for users to self-host the backend for complete data control.

## How MoodSync Helps (Powered by the Backend)

The backend API enables features that help you:

### Understand Your Emotional Patterns
*   The API allows fetching mood history with filters, enabling frontend to display trends like:
    *   Mood fluctuations by time of day.
    *   Mood variations by day of the week.
    *   Correlation between activities and moods.
*   Sentiment scores for notes provide an objective measure of your written reflections.

### Develop Better Habits
*   `HabitImprovementAPIView` analyzes recent moods and activities to suggest potentially beneficial or detrimental habits.
*   The API can track which suggestions are offered and (future) how users respond to them.

### Manage Stress and Anxiety
*   `MotivationSuggestionAPIView` can provide tailored coping messages when patterns of anxiety or stress are detected in mood entries.
*   By logging moods and notes during stressful periods, the API provides data for later reflection and pattern identification.

## Contact & Support

For questions related to the backend API, development, or contributions:
*   Open an issue on the GitHub repository.
*   Email: backend-dev@moodsync.example.com

For general user inquiries (once the frontend is available):
*   Email: support@moodsync.example.com
*   Twitter: [@MoodSyncApp](#)
*   Support Portal: [help.moodsync.example.com](#)

## Join Our Community

Connect with other developers and future users:
*   [Discord](#) (For developer discussions and community building)
*   [Reddit](#)

---

MoodSync: Building a smarter way to understand and improve emotional wellbeing, one API call at a time.
