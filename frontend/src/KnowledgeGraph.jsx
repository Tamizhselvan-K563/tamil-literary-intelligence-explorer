import ForceGraph2D from "react-force-graph-2d";

function KnowledgeGraph({
  word,
  relationships = []
}) {

  if (!word) {
    return null;
  }

  const nodes = [
    {
      id: word,
      label: word,
      type: "main"
    }
  ];

  const links = [];

  relationships.forEach((item) => {

    if (!item.word) {
      return;
    }

    nodes.push({
      id: item.word,
      label: item.word,
      type: item.relation
    });

    links.push({
      source: word,
      target: item.word,
      relation: item.relation,
      confidence: item.confidence
    });

  });


  const getColor = (type) => {

    const relation =
      String(type || "").toLowerCase();

    if (relation.includes("synonym")) {
      return "#78b7d4";
    }

    if (relation.includes("antonym")) {
      return "#d77a7a";
    }

    return "#9b8ac4";
  };


  return (

    <section
      id="knowledge-graph"
      className="knowledge-graph-section"
    >

      <div className="graph-header">

        <div className="section-label">
          KNOWLEDGE GRAPH
        </div>

        <h2>
          The world around{" "}
          <span>{word}</span>
        </h2>

        <p>
          Explore how this Tamil word connects with
          synonyms, antonyms and related words.
        </p>

      </div>


      <div className="knowledge-graph-card">

        <div className="graph-topbar">

          <div>
            <span className="graph-status-dot"></span>
            Interactive relationship map
          </div>

          <div className="graph-word">
            {word}
          </div>

        </div>


        <div className="graph-canvas">

          {nodes.length > 1 ? (

            <ForceGraph2D
              graphData={{
                nodes,
                links
              }}

              backgroundColor="#0d0d0d"

              nodeRelSize={8}

              linkWidth={2}

              linkColor={(link) =>
                getColor(link.relation)
              }

              linkDirectionalParticles={3}

              linkDirectionalParticleSpeed={0.006}

              linkDirectionalParticleWidth={2}

              cooldownTicks={100}

              d3VelocityDecay={0.35}

              nodeLabel={(node) =>
                `${node.label} ${
                  node.type !== "main"
                    ? `• ${node.type}`
                    : ""
                }`
              }


              nodeCanvasObject={(
                node,
                ctx,
                globalScale
              ) => {

                const isMain =
                  node.type === "main";

                const radius =
                  isMain ? 20 : 12;

                const color =
                  isMain
                    ? "#d6b56a"
                    : getColor(node.type);


                /* Glow */

                ctx.beginPath();

                ctx.arc(
                  node.x,
                  node.y,
                  radius + 6,
                  0,
                  Math.PI * 2
                );

                ctx.fillStyle =
                  `${color}22`;

                ctx.fill();


                /* Circle */

                ctx.beginPath();

                ctx.arc(
                  node.x,
                  node.y,
                  radius,
                  0,
                  Math.PI * 2
                );

                ctx.fillStyle = color;

                ctx.fill();


                /* Border */

                ctx.strokeStyle =
                  "#f5eee1";

                ctx.lineWidth =
                  isMain ? 2 : 1;

                ctx.stroke();


                /* Tamil label */

                const fontSize =
                  Math.max(
                    13,
                    16 / globalScale
                  );

                ctx.font =
                  `600 ${fontSize}px Arial`;

                ctx.textAlign =
                  "center";

                ctx.textBaseline =
                  "top";

                ctx.fillStyle =
                  "#f4efe6";

                ctx.fillText(
                  node.label,
                  node.x,
                  node.y + radius + 8
                );

              }}

            />

          ) : (

            <div className="graph-empty">

              No relationship data found for{" "}
              <strong>{word}</strong>.

            </div>

          )}

        </div>


        <div className="graph-legend">

          <div className="legend-item">

            <span className="legend-circle main"></span>

            Main Word

          </div>

          <div className="legend-item">

            <span className="legend-circle synonym"></span>

            Synonym

          </div>

          <div className="legend-item">

            <span className="legend-circle antonym"></span>

            Antonym

          </div>

          <div className="legend-item">

            <span className="legend-circle related"></span>

            Related Word

          </div>

        </div>

      </div>

    </section>
  );
}

export default KnowledgeGraph;