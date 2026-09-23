import "./App.css";

function App() {
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

  const exploreWord = () => {
    const word =
      document.getElementById("word-search").value;

    if (word.trim() === "") {
      alert("Please enter a Tamil word.");
      return;
    }

    alert(`Exploring: ${word}`);
  };

  return (
    <div className="app">

      {/* NAVBAR */}
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


      {/* HERO */}
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


          {/* VOICE BUTTON */}
          <button
            className="voice-button"
            onClick={startVoiceSearch}
            title="Voice Search"
          >
            🎙
          </button>


          {/* EXPLORE BUTTON */}
          <button
            className="explore-button"
            onClick={exploreWord}
          >
            Explore →
          </button>

        </div>


        {/* SEARCH DESCRIPTION */}
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
              document.getElementById("word-search").value =
                "அன்பு"
            }
          >
            அன்பு
          </button>

          <button
            onClick={() =>
              document.getElementById("word-search").value =
                "அகம்"
            }
          >
            அகம்
          </button>

          <button
            onClick={() =>
              document.getElementById("word-search").value =
                "அறம்"
            }
          >
            அறம்
          </button>

          <button
            onClick={() =>
              document.getElementById("word-search").value =
                "வீரம்"
            }
          >
            வீரம்
          </button>

        </div>

      </section>


      {/* DISCOVER */}
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


      {/* THREE FEATURES */}
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
                .focus()
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


          <button className="feature-link">
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


      {/* VOICE FEATURE */}
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
            <span>Explore with your voice.</span>
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


      {/* CLOSING */}
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


      {/* FOOTER */}
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