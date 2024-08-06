# Vocation.ai
Empowering rural India's youth through AI driven education and employment solutions. We bridge the gap between learning and earning, fostering nation's development and individual growth.

# How to use
- To see the output, use the prototype link.
- The project won't run locally as the API keys and system prompts have been removed.
- This was done to avoid unauthorized access to sensitive information and prevent plagiarism.
- However the full codebase is available for thorough review and evaluation.

# Prototype
[Try Out >](https://vocation-ai.web.app/)

# Technology
```mermaid
    graph TD
    A((Vocation.ai Technology)) --> B{Tutor AI}
    A --> C{Quiz AI}
    A --> D{Job AI}
    A --> ASSSA([Online Community])
    ASSSA --> SSSSA[Peers, Mentors, and Technical Admins]
    
    B --> XssaA[Retrieval-Augmented Generation 'RAG' Architecture]
    
    XssaA --> E[LangChain Framework]
    XssaA --> F[OpenAI GPT-4 Turbo]
    XssaA --> G[Google Gemini-1.5 Pro]
    XssaA --> H[Pinecone DB]
    
    H --> I[Vector Embeddings]
    I --> J[Knowledge Base]
    J --> QQWQ[Dynamic Knowledge Update through Internet Access]
    QQWQ --> SFAS[Curated by Admins]
    I --> K[Student Memory]
    K --> DSD[Strengths & Weaknesses, Topics Covered, Learning Style etc.]
    DSD --> DGFS[Adaptive and Personalised Learning]
    
    B --> L[Multimodal AI]
    L --> SS14[Multiple Indic Languages]
    SS14 --> DB168[Voice Recognition and Text-To-Speech 'ResponseVoice.JS API']
    DB168 --> X23100[Face expression detection AI using webcam 'Face++ API']
    X23100 --> M[Vision-powered System]

    M --> SS[Screen Monitoring]
    M --> DD[File / Image Upload]

    SS --> XY[Real-Time Guidance]
    DD --> XY
    XY --> Z141[Autograding Homework using vision capabilities]
    
    C --> N[Dynamic Question Generation]
    1JH23 --> QW[Learning Progress Tracking]
    N --> O[Test Student Knowledge]
    O --> 1JH23[Gamification and Reward Points]
    QW --> HFX[Determine Job Readiness]
    HFX --> DOP21[AI Proctoring monitors Tab switching, Shared Screen Content and Webcam Activity]

    D --> R[Job Search APIs & Web Scraping]
    R --> 4W1[Job Recommendation]
    4W1 --> S[Remote Job Opportunities]
    S --> D12[Job Quality Feedback Mechanism]
    
    D --> T[Vision-powered Chat System]
    T --> U[Assist with Job Tasks]
    T --> V[Quality Control]

    D --> 12HHQ[Resume AI]
    D --> 14HHQ[Interview AI]    

    B -.-> C
    C -.-> D
    D -.-> B
```
