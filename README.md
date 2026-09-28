# Digital Marketing FAQ Chatbot 🤖📈

An **AI/NLP-based FAQ chatbot** that answers frequently asked questions about digital marketing, including **SEO, social media marketing, Google Ads, content marketing, email marketing, and analytics**.

The chatbot uses **NLP preprocessing, TF-IDF vectorization, and cosine similarity** to find the most relevant FAQ instead of relying on hardcoded `if/else` rules.

> Developed as part of an **AI/NLP Internship – Task 2**.

---

## 📌 Project Description

This project is a full-stack FAQ chatbot for digital marketing.

A user enters a question through the web chat interface. The Flask backend preprocesses the question using NLP techniques such as tokenization, stopword removal, and lemmatization.

The processed question is converted into a TF-IDF vector and compared with the vectors of the FAQ questions using cosine similarity.

The FAQ with the highest similarity score is selected and its answer is returned.

If the similarity score is below the configured threshold, the chatbot returns a fallback response instead of providing an unreliable answer.

---

## ✨ Features

* 🤖 NLP-based FAQ chatbot
* 📚 **52 FAQ entries**
* 🔄 Multiple question variations for better matching
* 🔎 TF-IDF vectorization
* 📐 Cosine similarity matching
* 🧠 NLTK NLP preprocessing
* 🛡️ Similarity-threshold fallback
* 📊 Category and match-confidence display
* 💬 Modern chat interface
* ⌨️ Enter-to-send support
* 💡 Suggested questions
* ⏳ Typing indicator
* 🧹 Clear Chat functionality
* 📱 Responsive desktop and mobile design
* 🔒 HTML escaping for safer message rendering
* 🌐 Flask REST API

---

## 📂 FAQ Categories

The chatbot covers the following digital marketing topics:

| Category                              | Coverage                                                         |
| ------------------------------------- | ---------------------------------------------------------------- |
| SEO                                   | Search engine optimization, keywords, backlinks, rankings        |
| Social Media Marketing                | Platforms, engagement, hashtags, influencers, paid ads           |
| Google/Online Advertising             | Google Ads, PPC, CTR, Quality Score, retargeting                 |
| Content Marketing                     | Content strategy, evergreen content, storytelling                |
| Email Marketing                       | Email lists, open rates, segmentation, automation                |
| Analytics & General Digital Marketing | ROI, conversion rate, bounce rate, funnels, campaign performance |
| Greetings & Farewells                 | Hello, Hi, Goodbye, Bye and similar messages                     |

---

## 🛠 Technologies Used

| Layer                       | Technology            |
| --------------------------- | --------------------- |
| Backend                     | Python, Flask         |
| NLP                         | NLTK                  |
| Machine Learning / Matching | scikit-learn          |
| Vectorization               | TF-IDF                |
| Similarity                  | Cosine Similarity     |
| Frontend                    | HTML, CSS, JavaScript |
| Data                        | JSON                  |
| API                         | Flask REST API        |

---

## 🧠 NLP Preprocessing

Every FAQ question and every user question goes through the same preprocessing pipeline.

### 1. Lowercasing

Converts text to lowercase.

```text
What is SEO?
```

becomes:

```text
what is seo
```

### 2. Punctuation Removal

Removes unnecessary punctuation such as:

```text
?, !, ., ,
```

### 3. Tokenization

The sentence is divided into individual words using NLTK tokenization.

### 4. Stopword Removal

Common words with low information value are removed using NLTK stopwords.

Examples include words such as:

```text
is, the, a, how
```

### 5. Lemmatization

Words are reduced to their base form using `WordNetLemmatizer`.

This helps similar word forms match more effectively.

---

## 🔢 TF-IDF Vectorization

**TF-IDF (Term Frequency–Inverse Document Frequency)** converts text into numerical vectors.

### Term Frequency

Measures how frequently a word occurs in a question.

### Inverse Document Frequency

Measures how distinctive a word is across the FAQ dataset.

Common words receive lower importance, while distinctive terms such as:

```text
backlink
retargeting
conversion
```

can receive higher importance.

The project uses:

```python
TfidfVectorizer(
    ngram_range=(1, 2),
    sublinear_tf=True
)
```

The `(1, 2)` setting allows the chatbot to consider both individual words and two-word phrases.

---

## 📐 Cosine Similarity

Cosine similarity measures how similar two text vectors are.

The chatbot:

1. Processes the user's question.
2. Converts it into a TF-IDF vector.
3. Compares it with the FAQ vectors.
4. Finds the highest similarity score.
5. Returns the corresponding FAQ answer.

A score closer to **1.0** indicates greater similarity, while a score closer to **0.0** indicates little similarity.

The current matcher uses a similarity threshold of:

```text
0.30
```

If the best score is below this threshold, the chatbot returns a fallback response.

---

## 🔄 Project Workflow

```text
User enters a question
          │
          ▼
JavaScript frontend
          │
          ▼
POST /api/chat
          │
          ▼
Flask backend
          │
          ▼
FAQMatcher
          │
          ▼
NLP preprocessing
          │
          ▼
TF-IDF transformation
          │
          ▼
Cosine similarity
          │
          ▼
Find highest matching FAQ
          │
          ├── Score < 0.30
          │       │
          │       ▼
          │   Fallback response
          │
          └── Score >= 0.30
                  │
                  ▼
             FAQ answer
                  │
                  ▼
          JavaScript chat UI
```

---

## 📁 Folder Structure

```text
digital-marketing-faq-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── faqs.json
│
├── nlp/
│   └── preprocessing.py
│
├── chatbot/
│   └── matcher.py
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

---

## ⚙️ Installation

### 1. Clone or download the project

Open a terminal and move into the project folder:

```bash
cd digital-marketing-faq-chatbot
```

### 2. Create a virtual environment

Recommended:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. NLTK Resources

The project automatically downloads the required NLTK resources when necessary.

These include:

```text
punkt
punkt_tab
stopwords
wordnet
omw-1.4
```

An internet connection may be required during the first setup.

---

## ▶️ Run the Project

Start the Flask application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser.

---

## 🌐 API

The chatbot provides a REST API endpoint:

```text
POST /api/chat
```

### Request

```json
{
  "message": "How can I improve my website ranking?"
}
```

### Example Response

```json
{
  "answer": "You can improve your website ranking by creating high-quality content, using relevant keywords naturally, optimizing page titles and meta descriptions, improving site speed, making your site mobile-friendly, and earning backlinks from reputable websites.",
  "category": "SEO",
  "similarity": 0.78
}
```

---

## 💬 Example Questions

Try questions such as:

```text
What is SEO?

How can I improve my website ranking?

Can Instagram help me promote my business?

What is pay per click advertising?

How can I get more email subscribers?

What is evergreen marketing content?

How can I automatically send emails to customers?

What does ROI mean in marketing?

How can I measure my online campaign performance?

Hello!

Hi there!

Goodbye!
```

---

## 🧪 Testing

The chatbot was tested with both direct and differently-worded questions.

Examples include:

| User Question                              | Result                      |
| ------------------------------------------ | --------------------------- |
| What does SEO mean?                        | ✅ SEO                       |
| What is SEO?                               | ✅ SEO                       |
| I want my website to rank higher on Google | ✅ SEO                       |
| Can Instagram help me promote my business? | ✅ Social Media Marketing    |
| What is pay per click advertising?         | ✅ Google/Online Advertising |
| How can I get more email subscribers?      | ✅ Email Marketing           |
| What is evergreen marketing content?       | ✅ Content Marketing         |
| What does ROI mean in marketing?           | ✅ Analytics                 |
| What is the weather today?                 | ✅ Fallback                  |

The chatbot also supports question variations to improve matching when users phrase the same intent differently.

---

## 🛡️ Fallback Handling

The chatbot does not blindly return the closest FAQ.

If the best similarity score is below the configured threshold, it returns:

```text
I'm sorry, I couldn't find a relevant answer to that question.
Please try asking about SEO, social media marketing, online advertising,
content marketing, email marketing, or analytics.
```

This helps prevent unrelated questions from receiving misleading answers.

---

## 🚀 Future Enhancements

Possible future improvements include:

* 🧠 Semantic embeddings using Sentence Transformers
* 💭 Multi-turn conversation memory
* 👍 Helpful / Not Helpful feedback buttons
* 📚 Larger FAQ dataset
* 🛠️ Admin dashboard for FAQ management
* 🌐 Multilingual support
* 📊 Analytics dashboard
* 📝 Logging unanswered questions
* ☁️ Cloud deployment
* 🔐 Production authentication and security
* 📱 Progressive Web App support

---

## 🎓 Internship Project

This project was developed as part of an **AI/NLP Internship – Task 2**.

It demonstrates practical implementation of:

* Natural Language Processing
* Text preprocessing
* TF-IDF vectorization
* Cosine similarity
* FAQ intent matching
* Flask REST APIs
* Frontend-backend integration
* Responsive web development

The chatbot uses an NLP-based similarity approach rather than hardcoded question-to-answer `if/else` rules.

---

## 👩‍💻 Author

**Roshanbi Shaikh**

AI/NLP Internship Project
Digital Marketing FAQ Chatbot
