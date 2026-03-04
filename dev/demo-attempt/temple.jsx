import { useState, useEffect, useRef } from "react";

const HIEROGLYPHS = "𓂀𓃭𓅃𓆣𓇋𓈖𓉐𓊝𓋴𓌙𓍯𓎡𓏏";

const EMOJI_DATA = {
  "웃": {
    label: "Person",
    levels: {
      "-1": { name: "Genesis", desc: "What generates a person? Need, desire, the meeting of two paths." },
      "0": { name: "Personhood", desc: "The quality of being a person. Identity, consciousness, dignity." },
      "1": { name: "Individual", desc: "A single person. You. Me. The irreducible unit of meaning." },
      "2": { name: "People", desc: "The collective. Community, tribe, the space between individuals." },
      "3": { name: "Society", desc: "The system. Institutions, laws, the architecture of coexistence." },
      "4": { name: "Civilization", desc: "The meta-system. Culture across time, the long arc of human becoming." },
    }
  },
  "🏠": {
    label: "House",
    levels: {
      "-1": { name: "Genesis", desc: "What generates a house? The decision to stop wandering. Shelter as choice." },
      "0": { name: "Domesticity", desc: "The quality of home. Warmth, belonging, the walls we build inside." },
      "1": { name: "A House", desc: "One dwelling. Four walls and a door. The basic unit of shelter." },
      "2": { name: "Neighborhood", desc: "Houses in relation. Streets, fences, the geography of proximity." },
      "3": { name: "Urban System", desc: "City planning, housing policy, the politics of where we live." },
      "4": { name: "Habitat", desc: "Civilization's relationship to dwelling. Nomadism to megacity." },
    }
  },
  "🌳": {
    label: "Tree",
    levels: {
      "-1": { name: "Genesis", desc: "What generates a tree? A seed, patience, and the blind faith of soil." },
      "0": { name: "Arborescence", desc: "The quality of tree-ness. Branching, rootedness, vertical patience." },
      "1": { name: "A Tree", desc: "One organism. Bark, leaves, rings counting silent years." },
      "2": { name: "Forest", desc: "Trees in communion. Canopy, mycorrhiza, the wood wide web." },
      "3": { name: "Ecosystem", desc: "The living system. Climate, carbon, the lungs of a planet." },
      "4": { name: "Biosphere", desc: "Life's total architecture. The thin green film that makes Earth, Earth." },
    }
  },
  "📖": {
    label: "Book",
    levels: {
      "-1": { name: "Genesis", desc: "What generates a book? An idea that refused to stay unwritten." },
      "0": { name: "Knowledge", desc: "The quality of the written. Preserved thought, frozen speech." },
      "1": { name: "A Book", desc: "One volume. Pages bound, a world compressed into portable form." },
      "2": { name: "Library", desc: "Books in conversation. Shelves as civilization's memory palace." },
      "3": { name: "Literature", desc: "The system of texts. Canon, tradition, the ongoing argument of culture." },
      "4": { name: "Noosphere", desc: "The total sphere of human thought. Every word ever committed to form." },
    }
  },
  "⭐": {
    label: "Star",
    levels: {
      "-1": { name: "Genesis", desc: "What generates a star? Gravity's patience with hydrogen. Collapse as creation." },
      "0": { name: "Stardom", desc: "The quality of radiance. Brilliance, aspiration, the light that draws eyes." },
      "1": { name: "A Star", desc: "One burning point. Fusion sustained across billions of years." },
      "2": { name: "Constellation", desc: "Stars in pattern. Meaning projected onto the random by the hopeful." },
      "3": { name: "Galaxy", desc: "The system of stars. Spiral arms, dark matter scaffolding, cosmic architecture." },
      "4": { name: "Cosmos", desc: "Everything that is. The universe regarding itself through equations and awe." },
    }
  },
  "❤": {
    label: "Love",
    levels: {
      "-1": { name: "Genesis", desc: "What generates love? Vulnerability. The risk of needing another." },
      "0": { name: "Lovingness", desc: "The capacity to love. Tenderness as a state of being." },
      "1": { name: "A Love", desc: "One bond. Two people choosing each other against entropy." },
      "2": { name: "Community of Care", desc: "Love in plural. Friendship, kinship, the networks that hold us." },
      "3": { name: "Compassion System", desc: "Institutional care. Healthcare, charity, mercy codified into structure." },
      "4": { name: "Agape", desc: "Universal love. The improbable bet that strangers deserve kindness." },
    }
  },
  "⚒": {
    label: "Work",
    levels: {
      "-1": { name: "Genesis", desc: "What generates work? Necessity, ambition, or the restless need to make." },
      "0": { name: "Labor", desc: "The condition of working. Effort as identity, craft as devotion." },
      "1": { name: "A Task", desc: "One act of making. Hands on material, mind on purpose." },
      "2": { name: "Workshop", desc: "Workers together. Division of labor, shared purpose, the guild." },
      "3": { name: "Economy", desc: "The system of work. Markets, wages, the machinery of exchange." },
      "4": { name: "Techne", desc: "Civilization's relationship to making. From flint-knapping to AI." },
    }
  },
};

const POLYNOMIAL_PRESETS = {
  "Individualism": { w1: 0.7, w2: 0.2, w3: 0.1 },
  "Socialism": { w1: 0.1, w2: 0.5, w3: 0.4 },
  "Anarchism": { w1: 0.9, w2: 0.1, w3: 0.0 },
  "Totalitarianism": { w1: 0.0, w2: 0.1, w3: 0.9 },
};

const POWER_LABELS = ["-1", "0", "1", "2", "3", "4"];
const GLYPH_CHARS = HIEROGLYPHS.split("");

function FloatingGlyphs() {
  const [glyphs, setGlyphs] = useState([]);
  useEffect(() => {
    const g = Array.from({ length: 30 }, (_, i) => ({
      char: GLYPH_CHARS[i % GLYPH_CHARS.length],
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: 12 + Math.random() * 18,
      opacity: 0.03 + Math.random() * 0.06,
      duration: 30 + Math.random() * 40,
      delay: Math.random() * -30,
    }));
    setGlyphs(g);
  }, []);

  return (
    <div style={{ position: "fixed", inset: 0, pointerEvents: "none", zIndex: 0, overflow: "hidden" }}>
      {glyphs.map((g, i) => (
        <span
          key={i}
          style={{
            position: "absolute",
            left: `${g.x}%`,
            top: `${g.y}%`,
            fontSize: g.size,
            opacity: g.opacity,
            color: "#c9a84c",
            fontFamily: "serif",
            animation: `floatGlyph ${g.duration}s ease-in-out ${g.delay}s infinite`,
          }}
        >
          {g.char}
        </span>
      ))}
    </div>
  );
}

function HierarchyColumn({ emoji, data, isActive, delay }) {
  const [revealed, setRevealed] = useState(-1);

  useEffect(() => {
    if (!isActive) { setRevealed(-1); return; }
    let i = 0;
    const interval = setInterval(() => {
      setRevealed(i);
      i++;
      if (i >= POWER_LABELS.length) clearInterval(interval);
    }, 180);
    return () => clearInterval(interval);
  }, [isActive, emoji]);

  return (
    <div style={{
      display: "flex",
      flexDirection: "column-reverse",
      alignItems: "center",
      gap: 0,
      animation: isActive ? `fadeSlideUp 0.6s ease ${delay}ms both` : "none",
    }}>
      {POWER_LABELS.map((power, idx) => {
        const level = data.levels[power];
        const show = revealed >= idx;
        const isGenesis = power === "-1";
        const isEssence = power === "0";
        return (
          <div
            key={power}
            style={{
              opacity: show ? 1 : 0,
              transform: show ? "translateY(0) scale(1)" : "translateY(20px) scale(0.9)",
              transition: "all 0.5s cubic-bezier(0.23, 1, 0.32, 1)",
              padding: "14px 20px",
              margin: "4px 0",
              width: "100%",
              maxWidth: 420,
              background: isGenesis
                ? "linear-gradient(135deg, rgba(120,80,40,0.15), rgba(80,50,20,0.08))"
                : isEssence
                  ? "linear-gradient(135deg, rgba(201,168,76,0.12), rgba(201,168,76,0.04))"
                  : "rgba(255,252,245,0.5)",
              border: isGenesis
                ? "1px solid rgba(120,80,40,0.2)"
                : isEssence
                  ? "1px solid rgba(201,168,76,0.25)"
                  : "1px solid rgba(201,168,76,0.1)",
              borderRadius: 8,
              backdropFilter: "blur(8px)",
            }}
          >
            <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginBottom: 4 }}>
              <span style={{
                fontFamily: "'Cormorant Garamond', 'Garamond', serif",
                fontSize: 13,
                color: "#8a7340",
                letterSpacing: 1,
                fontVariantNumeric: "tabular-nums",
                minWidth: 36,
              }}>
                {emoji}<sup style={{ fontSize: 10 }}>{power}</sup>
              </span>
              <span style={{
                fontFamily: "'Cormorant Garamond', 'Garamond', serif",
                fontSize: 18,
                fontWeight: 600,
                color: "#2a2118",
                letterSpacing: 0.5,
              }}>
                {level.name}
              </span>
            </div>
            <p style={{
              margin: 0,
              fontFamily: "'EB Garamond', 'Garamond', 'Georgia', serif",
              fontSize: 14,
              lineHeight: 1.55,
              color: "#5a4d3a",
              fontStyle: isGenesis ? "italic" : "normal",
            }}>
              {level.desc}
            </p>
          </div>
        );
      })}
    </div>
  );
}

function PolynomialForge() {
  const [weights, setWeights] = useState({ w1: 0.33, w2: 0.34, w3: 0.33 });
  const [activePreset, setActivePreset] = useState(null);

  const setWeight = (key, val) => {
    const newW = { ...weights, [key]: val };
    const sum = newW.w1 + newW.w2 + newW.w3;
    if (sum > 0) {
      newW.w1 = Math.round((newW.w1 / sum) * 100) / 100;
      newW.w2 = Math.round((newW.w2 / sum) * 100) / 100;
      newW.w3 = Math.round((1 - newW.w1 - newW.w2) * 100) / 100;
    }
    setWeights(newW);
    setActivePreset(null);
  };

  const applyPreset = (name) => {
    setWeights(POLYNOMIAL_PRESETS[name]);
    setActivePreset(name);
  };

  const barStyle = (w, color) => ({
    height: 140 * w,
    minHeight: 2,
    width: 48,
    background: color,
    borderRadius: "4px 4px 0 0",
    transition: "height 0.4s cubic-bezier(0.23, 1, 0.32, 1)",
    position: "relative",
  });

  const describePhilosophy = () => {
    const { w1, w2, w3 } = weights;
    if (w1 >= 0.6) return "Radical individualism — the person above all else. Liberty as the highest value.";
    if (w3 >= 0.6) return "Strong systemic control — the structure governs. Order as the highest value.";
    if (w2 >= 0.5) return "Communitarian emphasis — the group as primary. Solidarity as the highest value.";
    if (w1 >= 0.4 && w2 >= 0.3) return "Liberal democracy — individual rights within community bonds.";
    if (w2 >= 0.3 && w3 >= 0.3) return "Social democracy — collective welfare anchored in institutional structure.";
    if (Math.abs(w1 - w2) < 0.1 && Math.abs(w2 - w3) < 0.1) return "Balanced triarchy — equal weight to person, people, and system. A rare equilibrium.";
    return "A hybrid philosophy — weighting individual, collective, and systemic forces in tension.";
  };

  const sliderLabels = [
    { key: "w1", symbol: "웃¹", label: "Individual", color: "#c9a84c" },
    { key: "w2", symbol: "웃²", label: "Collective", color: "#8a7340" },
    { key: "w3", symbol: "웃³", label: "System", color: "#5a4d3a" },
  ];

  return (
    <div style={{
      background: "linear-gradient(180deg, rgba(255,252,245,0.7), rgba(245,238,220,0.5))",
      border: "1px solid rgba(201,168,76,0.2)",
      borderRadius: 12,
      padding: "28px 24px",
      maxWidth: 520,
      margin: "0 auto",
      backdropFilter: "blur(12px)",
    }}>
      <h3 style={{
        fontFamily: "'Cormorant Garamond', 'Garamond', serif",
        fontSize: 20,
        fontWeight: 600,
        color: "#2a2118",
        margin: "0 0 4px 0",
        textAlign: "center",
        letterSpacing: 1,
      }}>
        The Polynomial Forge
      </h3>
      <p style={{
        fontFamily: "'EB Garamond', 'Garamond', 'Georgia', serif",
        fontSize: 14,
        color: "#8a7340",
        textAlign: "center",
        margin: "0 0 20px 0",
      }}>
        Tune the weights. Shape a worldview.
      </p>

      <div style={{
        fontFamily: "'Fira Code', 'Courier New', monospace",
        fontSize: 15,
        color: "#2a2118",
        textAlign: "center",
        padding: "12px 16px",
        background: "rgba(201,168,76,0.07)",
        borderRadius: 8,
        marginBottom: 20,
        letterSpacing: 0.5,
      }}>
        ㄕ(웃) = {weights.w1}웃 + {weights.w2}웃² + {weights.w3}웃³
      </div>

      <div style={{ display: "flex", justifyContent: "center", gap: 24, marginBottom: 20 }}>
        {sliderLabels.map(({ key, symbol, label, color }) => (
          <div key={key} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
            <div style={{
              display: "flex", flexDirection: "column-reverse", alignItems: "center",
              height: 140, justifyContent: "flex-start",
            }}>
              <div style={barStyle(weights[key], color)}>
                <span style={{
                  position: "absolute", top: -22, left: "50%", transform: "translateX(-50%)",
                  fontSize: 12, color, fontFamily: "monospace", fontWeight: 700, whiteSpace: "nowrap",
                }}>
                  {weights[key]}
                </span>
              </div>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              value={Math.round(weights[key] * 100)}
              onChange={(e) => setWeight(key, parseInt(e.target.value) / 100)}
              style={{ width: 48, accentColor: color }}
            />
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 16 }}>{symbol}</div>
              <div style={{
                fontSize: 11, color: "#8a7340",
                fontFamily: "'Cormorant Garamond', serif",
                letterSpacing: 0.5,
              }}>{label}</div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap", marginBottom: 16 }}>
        {Object.keys(POLYNOMIAL_PRESETS).map((name) => (
          <button
            key={name}
            onClick={() => applyPreset(name)}
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: 13,
              padding: "5px 14px",
              border: activePreset === name ? "1.5px solid #8a7340" : "1px solid rgba(201,168,76,0.3)",
              borderRadius: 20,
              background: activePreset === name ? "rgba(201,168,76,0.12)" : "transparent",
              color: "#2a2118",
              cursor: "pointer",
              letterSpacing: 0.5,
              transition: "all 0.2s",
            }}
          >
            {name}
          </button>
        ))}
      </div>

      <p style={{
        fontFamily: "'EB Garamond', 'Garamond', 'Georgia', serif",
        fontSize: 15,
        lineHeight: 1.6,
        color: "#5a4d3a",
        textAlign: "center",
        margin: 0,
        fontStyle: "italic",
        minHeight: 44,
      }}>
        {describePhilosophy()}
      </p>
    </div>
  );
}

export default function TempleOfPerson() {
  const [selectedEmoji, setSelectedEmoji] = useState("웃");
  const [isActive, setIsActive] = useState(true);
  const [activeTab, setActiveTab] = useState("hierarchy");

  const selectEmoji = (emoji) => {
    if (emoji === selectedEmoji) return;
    setIsActive(false);
    setTimeout(() => {
      setSelectedEmoji(emoji);
      setIsActive(true);
    }, 200);
  };

  const emojiKeys = Object.keys(EMOJI_DATA);

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(170deg, #fffcf5 0%, #f5eedd 40%, #ebe0c8 100%)",
      position: "relative",
      overflow: "hidden",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Fira+Code:wght@400;500&display=swap');
        
        @keyframes floatGlyph {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          33% { transform: translateY(-15px) rotate(3deg); }
          66% { transform: translateY(8px) rotate(-2deg); }
        }
        
        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulseGlow {
          0%, 100% { box-shadow: 0 0 0 0 rgba(201,168,76,0); }
          50% { box-shadow: 0 0 20px 4px rgba(201,168,76,0.15); }
        }
        
        @keyframes titleReveal {
          from { opacity: 0; letter-spacing: 12px; }
          to { opacity: 1; letter-spacing: 6px; }
        }
        
        @keyframes subtitleReveal {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        input[type="range"] {
          -webkit-appearance: none;
          height: 3px;
          background: rgba(201,168,76,0.3);
          border-radius: 2px;
          outline: none;
        }
        input[type="range"]::-webkit-slider-thumb {
          -webkit-appearance: none;
          width: 14px;
          height: 14px;
          border-radius: 50%;
          background: #8a7340;
          cursor: pointer;
          border: 2px solid #fffcf5;
          box-shadow: 0 1px 4px rgba(0,0,0,0.15);
        }
      `}</style>

      <FloatingGlyphs />

      <div style={{ position: "relative", zIndex: 1, maxWidth: 600, margin: "0 auto", padding: "20px 20px 60px" }}>
        {/* Header */}
        <header style={{ textAlign: "center", marginBottom: 32, paddingTop: 24 }}>
          <div style={{
            fontFamily: "'Cormorant Garamond', 'Garamond', serif",
            fontSize: 11,
            letterSpacing: 6,
            color: "#8a7340",
            textTransform: "uppercase",
            marginBottom: 8,
            animation: "titleReveal 1.2s ease both",
          }}>
            Temple of
          </div>
          <div style={{
            fontSize: 56,
            lineHeight: 1,
            marginBottom: 8,
            animation: "pulseGlow 4s ease-in-out infinite",
            display: "inline-block",
            borderRadius: "50%",
            padding: 8,
          }}>
            웃
          </div>
          <h1 style={{
            fontFamily: "'Cormorant Garamond', 'Garamond', serif",
            fontSize: 28,
            fontWeight: 300,
            color: "#2a2118",
            letterSpacing: 3,
            animation: "titleReveal 1.2s ease 0.2s both",
          }}>
            ㄕICTO<em>ji</em>
          </h1>
          <p style={{
            fontFamily: "'EB Garamond', 'Garamond', 'Georgia', serif",
            fontSize: 15,
            color: "#8a7340",
            marginTop: 8,
            fontStyle: "italic",
            animation: "subtitleReveal 1s ease 0.6s both",
          }}>
            Where meaning has structure, and you can see it
          </p>
        </header>

        {/* Decorative line */}
        <div style={{
          height: 1,
          background: "linear-gradient(90deg, transparent, rgba(201,168,76,0.4), transparent)",
          margin: "0 40px 28px",
        }} />

        {/* Tabs */}
        <div style={{ display: "flex", justifyContent: "center", gap: 4, marginBottom: 28 }}>
          {[
            { id: "hierarchy", label: "Power Hierarchy" },
            { id: "forge", label: "Polynomial Forge" },
          ].map(({ id, label }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: 14,
                letterSpacing: 1,
                padding: "8px 24px",
                border: "none",
                borderBottom: activeTab === id ? "2px solid #8a7340" : "2px solid transparent",
                background: "transparent",
                color: activeTab === id ? "#2a2118" : "#8a7340",
                cursor: "pointer",
                transition: "all 0.3s",
                fontWeight: activeTab === id ? 600 : 400,
              }}
            >
              {label}
            </button>
          ))}
        </div>

        {activeTab === "hierarchy" && (
          <>
            {/* Emoji selector */}
            <div style={{
              display: "flex",
              justifyContent: "center",
              gap: 6,
              marginBottom: 28,
              flexWrap: "wrap",
            }}>
              {emojiKeys.map((emoji) => (
                <button
                  key={emoji}
                  onClick={() => selectEmoji(emoji)}
                  style={{
                    width: 52,
                    height: 52,
                    borderRadius: 12,
                    border: selectedEmoji === emoji
                      ? "2px solid #8a7340"
                      : "1.5px solid rgba(201,168,76,0.2)",
                    background: selectedEmoji === emoji
                      ? "rgba(201,168,76,0.1)"
                      : "rgba(255,252,245,0.6)",
                    cursor: "pointer",
                    fontSize: 22,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: 0,
                    transition: "all 0.2s",
                    backdropFilter: "blur(8px)",
                    boxShadow: selectedEmoji === emoji
                      ? "0 2px 12px rgba(201,168,76,0.15)"
                      : "none",
                  }}
                >
                  <span>{emoji}</span>
                  <span style={{
                    fontSize: 8,
                    color: "#8a7340",
                    fontFamily: "'Cormorant Garamond', serif",
                    letterSpacing: 0.5,
                  }}>
                    {EMOJI_DATA[emoji].label}
                  </span>
                </button>
              ))}
            </div>

            {/* Active symbol display */}
            <div style={{ textAlign: "center", marginBottom: 20 }}>
              <span style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: 13,
                color: "#8a7340",
                letterSpacing: 2,
              }}>
                ASCENDING THE POWERS OF
              </span>
              <div style={{
                fontSize: 32,
                margin: "4px 0",
              }}>
                {selectedEmoji}
              </div>
              <span style={{
                fontFamily: "'EB Garamond', serif",
                fontSize: 14,
                color: "#5a4d3a",
                fontStyle: "italic",
              }}>
                {EMOJI_DATA[selectedEmoji].label}
              </span>
            </div>

            {/* Hierarchy column */}
            <HierarchyColumn
              emoji={selectedEmoji}
              data={EMOJI_DATA[selectedEmoji]}
              isActive={isActive}
              delay={100}
            />

            {/* Bottom inscription */}
            <div style={{
              textAlign: "center",
              marginTop: 32,
              padding: "16px 20px",
              borderTop: "1px solid rgba(201,168,76,0.15)",
            }}>
              <p style={{
                fontFamily: "'EB Garamond', serif",
                fontSize: 13,
                color: "#8a7340",
                fontStyle: "italic",
                lineHeight: 1.6,
              }}>
                {selectedEmoji}⁻¹ → {selectedEmoji}⁰ → {selectedEmoji}¹ → {selectedEmoji}² → {selectedEmoji}³ → {selectedEmoji}⁴
                <br />
                <span style={{ fontSize: 11, letterSpacing: 1 }}>
                  genesis → essence → individual → collective → system → civilization
                </span>
              </p>
            </div>
          </>
        )}

        {activeTab === "forge" && <PolynomialForge />}

        {/* Footer */}
        <div style={{
          textAlign: "center",
          marginTop: 40,
          opacity: 0.5,
        }}>
          <p style={{
            fontFamily: "'Cormorant Garamond', serif",
            fontSize: 11,
            color: "#8a7340",
            letterSpacing: 3,
          }}>
            🗿 ⨝ 웃²
          </p>
        </div>
      </div>
    </div>
  );
}
