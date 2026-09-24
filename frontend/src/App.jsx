import { useState } from "react";
import "./App.css";
import KnowledgeGraph from "./KnowledgeGraph";

function App() {
  const [searchedWord, setSearchedWord] = useState("");
  const [searchResult, setSearchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const startVoiceSearch = () => {
    if ("webkitSpeechRecognition" in window) {
      const recognition = new window.webkitSpeechRecognition();

      recognition.lang = "ta-IN";
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.start();

      recognition.onresult = (event) => {
        const transcript =
          event.results[0][0].transcript;

        document.getElementById("word-search").value =
          transcript;
      };

      recognition.onerror = () => {
        alert("Voice search could not be started.");
      };
    } else {
      alert(
        "Voice search is not supported in this browser. Try Google Chrome."
      );
    }
  };

  const exploreWord = async () => {
    const word =
      document.getElementById("word-search").value.trim();

    if (word === "") {
      alert("Please enter a Tamil word.");
      return;
    }

    // Show the searched word
    setSearchedWord(word);

    // Start loading
    setLoading(true);
    setError("");
    setSearchResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/search?word=${encodeURIComponent(
          word
        )}&top_k=3`
      );

      if (!response.ok) {
        throw new Error(
          "Failed to fetch data from backend"
        );
      }

      const data = await response.json();

      console.log("BACKEND RESPONSE:", data);

      setSearchResult(data);

      // Scroll AFTER the search result is available
      setTimeout(() => {
        document
          .getElementById("knowledge-graph")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });
      }, 300);

    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to the Tamil Literary Intelligence backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* ================= NAVBAR ================= */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-symbol">
            த
          </div>

          <div>
            <div className="brand-title">
              தமிழ்
            </div>

            <div className="brand-subtitle">
              LITERARY INTELLIGENCE
            </div>
          </div>

        </div>

        <div className="nav-links">

          <span className="active">
            Home
          </span>

          <span>
            Word Explorer
          </span>

          <span>
            Knowledge Graph
          </span>

          <span>
            Literature
          </span>

        </div>

      </nav>


      {/* ================= HERO ================= */}

      <section className="hero">

        <div className="hero-label">
          TAMIL • LANGUAGE • LITERATURE • AI
        </div>

        <h1>
          Discover the
          <br />

          <span>
            living world
          </span>{" "}
          of Tamil.
        </h1>

        <p>
          Explore meanings, relationships and literary
          connections hidden inside every Tamil word.
        </p>


        {/* SEARCH */}

        <div className="search-box">

          <span className="search-icon">
            ⌕
          </span>

          <input
            id="word-search"
            type="text"
            placeholder="Search a Tamil word..."
          />

          <button
            className="voice-button"
            onClick={startVoiceSearch}
            title="Voice Search"
          >
            🎙
          </button>

          <button
            className="explore-button"
            onClick={exploreWord}
            disabled={loading}
          >
            {loading
              ? "Exploring..."
              : "Explore →"}
          </button>

        </div>


        {/* SEARCH HINT */}

        <div className="voice-hint">

          <span className="voice-dot"></span>

          Type a word or use voice search in Tamil

        </div>


        {/* EXAMPLES */}

        <div className="examples">

          <span>
            Try exploring
          </span>

          <button
            onClick={() =>
              document.getElementById(
                "word-search"
              ).value = "அன்பு"
            }
          >
            அன்பு
          </button>

          <button
            onClick={() =>
              document.getElementById(
                "word-search"
              ).value = "அகம்"
            }
          >
            அகம்
          </button>

          <button
            onClick={() =>
              document.getElementById(
                "word-search"
              ).value = "அறம்"
            }
          >
            அறம்
          </button>

          <button
            onClick={() =>
              document.getElementById(
                "word-search"
              ).value = "வீரம்"
            }
          >
            வீரம்
          </button>

        </div>

      </section>


      {/* ================= SEARCH LOADING ================= */}

      {loading && (

        <section className="results-section">

          <div className="section-label">
            AI ANALYSIS
          </div>

          <h2>
            Analyzing Tamil literature...
          </h2>

          <p>
            Finding meanings, relationships and
            literary connections.
          </p>

        </section>

      )}


      {/* ================= ERROR ================= */}

      {error && (

        <section className="results-section">

          <div className="section-label">
            ERROR
          </div>

          <h2>
            Something went wrong
          </h2>

          <p>
            {error}
          </p>

        </section>

      )}


      {/* ================= SEARCH RESULTS ================= */}

      {searchResult && !loading && (

        <section className="results-section">

          <div className="section-label">
            WORD INTELLIGENCE
          </div>

          <h2>
            {searchResult.word}
          </h2>


          {/* TAMIL MEANINGS */}

          <div className="result-block">

            <h3>
              Tamil Meaning
            </h3>

            <div className="meaning-list">

              {searchResult.meanings_tamil?.map(
                (meaning, index) => (

                  <span key={index}>
                    {meaning}
                  </span>

                )
              )}

            </div>

          </div>


          {/* ENGLISH MEANINGS */}

          <div className="result-block">

            <h3>
              English Meaning
            </h3>

            <div className="meaning-list">

              {searchResult.meanings_english?.map(
                (meaning, index) => (

                  <span key={index}>
                    {meaning}
                  </span>

                )
              )}

            </div>

          </div>


          {/* RELATIONSHIPS LIST */}

          <div className="result-block">

            <h3>
              Word Relationships
            </h3>

            <div className="relationship-list">

              {searchResult.relationships?.map(
                (item, index) => (

                  <div
                    className="relationship-item"
                    key={index}
                  >

                    <strong>
                      {item.word}
                    </strong>

                    <span>
                      {item.relation}
                    </span>

                  </div>

                )
              )}

            </div>

          </div>


          {/* LITERATURE */}

          <div className="result-block">

            <h3>
              Literary Connections
            </h3>

            <div className="literature-list">

              {searchResult.literary_results?.map(
                (item, index) => (

                  <div
                    className="literature-card"
                    key={index}
                  >

                    <p>
                      {item.literary_text}
                    </p>

                    <div>
                      {item.work} • {item.author}
                    </div>

                    <small>
                      Theme: {item.theme}
                    </small>

                  </div>

                )
              )}

            </div>

          </div>

        </section>

      )}


      {/* ================= DISCOVER ================= */}

      <section className="discover">

        <div className="section-label">
          DISCOVER
        </div>

        <h2>
          One word.
          <br />
          Many connections.
        </h2>

        <p>
          A Tamil word can carry meaning, relationships,
          emotion and centuries of literary memory.
        </p>

      </section>


      {/* ================= THREE FEATURES ================= */}

      <section className="features">


        {/* WORD EXPLORER */}

        <div className="feature-card">

          <div className="feature-number">
            01
          </div>

          <div className="feature-icon">
            ◇
          </div>

          <div className="feature-label">
            EXPLORE
          </div>

          <h3>
            Word Explorer
          </h3>

          <p>
            Understand Tamil words through their meanings,
            English translations, synonyms and antonyms.
          </p>

          <button
            className="feature-link"
            onClick={() =>
              document
                .getElementById("word-search")
                ?.focus()
            }
          >
            Explore words →
          </button>

        </div>


        {/* KNOWLEDGE GRAPH */}

        <div className="feature-card highlight">

          <div className="feature-number">
            02
          </div>

          <div className="feature-icon">
            ✦
          </div>

          <div className="feature-label">
            CONNECT
          </div>

          <h3>
            Knowledge Graph
          </h3>

          <p>
            Visualize connections between synonyms,
            antonyms and related Tamil words.
          </p>

          <button
            className="feature-link"
            onClick={() => {

              if (!searchedWord) {
                document
                  .getElementById("word-search")
                  ?.focus();

                return;
              }

              document
                .getElementById("knowledge-graph")
                ?.scrollIntoView({
                  behavior: "smooth"
                });

            }}
          >
            Explore connections →
          </button>

        </div>


        {/* LITERARY CONTEXT */}

        <div className="feature-card">

          <div className="feature-number">
            03
          </div>

          <div className="feature-icon">
            ❖
          </div>

          <div className="feature-label">
            CONTEXT
          </div>

          <h3>
            Literary Context
          </h3>

          <p>
            Discover how Tamil words appear and evolve
            across Sangam, medieval and epic literature.
          </p>

          <button className="feature-link">
            Read literature →
          </button>

        </div>

      </section>


      {/* ================= KNOWLEDGE GRAPH ================= */}

      {searchedWord && (

        <KnowledgeGraph
          word={searchedWord}
          relationships={[]}
        />

      )}


      {/* ================= VOICE FEATURE ================= */}

      <section className="voice-section">

        <div className="voice-section-icon">
          🎙
        </div>

        <div>

          <div className="section-label">
            VOICE SEARCH
          </div>

          <h2>
            Speak in Tamil.
            <br />

            <span>
              Explore with your voice.
            </span>
          </h2>

          <p>
            Search Tamil words naturally using your voice
            and discover their meanings, relationships
            and literary context.
          </p>

        </div>

        <button
          className="voice-large-button"
          onClick={startVoiceSearch}
        >
          🎙 Start Voice Search
        </button>

      </section>


      {/* ================= CLOSING ================= */}

      <section className="closing">

        <div className="closing-line"></div>

        <div className="closing-label">
          TAMIL LITERARY INTELLIGENCE EXPLORER
        </div>

        <h2>
          From a word's meaning
          <br />

          <span>
            to its story.
          </span>
        </h2>

        <p>
          Ancient language. Connected knowledge.
        </p>

      </section>


      {/* ================= FOOTER ================= */}

      <footer>

        <div className="footer-brand">
          தமிழ்
        </div>

        <div>
          WORDS • LITERATURE • KNOWLEDGE
        </div>

      </footer>

    </div>
  );
}

export default App;