import { useState } from "react";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const TEAL = "#2ABFA3";
const ORANGE = "#E88E36";
const INDIGO = "#5C6BC0";
const AMBER = "#F9A825";
const RED = "#EF5350";
const DARK = "#0D1117";
const CARD = "#161B22";
const BORDER = "#21262D";
const TEXT = "#E6EDF3";
const MUTED = "#8B949E";

const providers = [
  { id: "claude", name: "Claude (Anthropic)", color: ORANGE, icon: "🤖", plan: "Pro", monthly: 20.00, daily: [18,19,20,20,20,20,20], tokens: "Unlimited (limits apply)" },
  { id: "copilot", name: "GitHub Copilot", color: INDIGO, icon: "🛸", plan: "Pro Max", monthly: 39.00, daily: [35,37,39,39,39,39,39], tokens: "1,500 premium req/mo" },
  { id: "gcp", name: "GCP / Vertex AI", color: TEAL, icon: "☁️", plan: "Pay-as-you-go", monthly: 7.43, daily: [0.80,1.10,0.95,1.20,0.88,1.30,1.20], tokens: "~148K tokens/day avg" },
  { id: "openai", name: "OpenAI API", color: AMBER, icon: "✦", plan: "Pay-as-you-go", monthly: 14.20, daily: [1.80,2.10,1.95,2.40,2.20,2.10,1.65], tokens: "~284K tokens/day avg" },
];

const weekLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const trendData = weekLabels.map((day, i) => ({
  day,
  claude: providers[0].daily[i],
  copilot: providers[1].daily[i],
  gcp: providers[2].daily[i],
  openai: providers[3].daily[i],
  total: providers.reduce((s, p) => s + p.daily[i], 0),
}));

const modelBreakdown = [
  { name: "claude-sonnet", provider: "Claude", cost: 8.40, pct: 42, color: ORANGE },
  { name: "gpt-4o", provider: "OpenAI", cost: 9.10, pct: 45, color: AMBER },
  { name: "gemini-1.5-pro", provider: "GCP", cost: 4.20, pct: 21, color: TEAL },
  { name: "claude-haiku", provider: "Claude", cost: 1.80, pct: 9, color: "#E8A870" },
  { name: "gpt-3.5-turbo", provider: "OpenAI", cost: 0.90, pct: 4, color: "#FBC02D" },
];

const alerts = [
  { level: "warn", msg: "GCP daily spend up 38% vs last week", time: "2h ago" },
  { level: "info", msg: "Copilot premium requests: 1,243 / 1,500 used", time: "4h ago" },
  { level: "danger", msg: "OpenAI monthly budget 85% consumed (18 days left)", time: "1d ago" },
];

const carbon = [
  { provider: "Claude Pro", kg: 0.12, color: ORANGE },
  { provider: "Copilot", kg: 0.31, color: INDIGO },
  { provider: "GCP", kg: 0.08, color: TEAL },
  { provider: "OpenAI", kg: 0.22, color: AMBER },
];

function MetricCard({ label, value, sub, color, icon }) {
  return (
    <div style={{
      background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12,
      padding: "20px 22px", display: "flex", flexDirection: "column", gap: 6,
      borderTop: `3px solid ${color}`,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 12, color: MUTED, letterSpacing: "0.06em", textTransform: "uppercase" }}>{label}</span>
        <span style={{ fontSize: 18 }}>{icon}</span>
      </div>
      <div style={{ fontSize: 28, fontWeight: 700, color: TEXT, fontFamily: "monospace" }}>{value}</div>
      <div style={{ fontSize: 12, color: MUTED }}>{sub}</div>
    </div>
  );
}

function AlertBadge({ level }) {
  const map = { warn: [AMBER, "⚠️"], info: [TEAL, "ℹ️"], danger: [RED, "🔴"] };
  const [col, icon] = map[level];
  return <span style={{ fontSize: 14 }}>{icon}</span>;
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "#1C2128", border: `1px solid ${BORDER}`, borderRadius: 8, padding: "10px 14px" }}>
      <div style={{ color: MUTED, fontSize: 11, marginBottom: 6 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color, fontSize: 12, display: "flex", justifyContent: "space-between", gap: 16 }}>
          <span>{p.name}</span><span style={{ fontFamily: "monospace" }}>${Number(p.value).toFixed(2)}</span>
        </div>
      ))}
    </div>
  );
};

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const totalMonthly = providers.reduce((s, p) => s + p.monthly, 0);
  const totalCarbon = carbon.reduce((s, c) => s + c.kg, 0);

  return (
    <div style={{
      background: DARK, minHeight: "100vh", color: TEXT,
      fontFamily: "'DM Mono', 'Fira Code', 'Courier New', monospace",
      padding: "28px 32px",
    }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 28 }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
            <div style={{ width: 32, height: 32, borderRadius: 8, background: `linear-gradient(135deg, ${TEAL}, ${ORANGE})`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>⚡</div>
            <span style={{ fontSize: 20, fontWeight: 700, letterSpacing: "-0.02em", color: TEXT }}>AI Cost Tracker</span>
            <span style={{ fontSize: 11, background: `${TEAL}22`, color: TEAL, padding: "2px 8px", borderRadius: 20, border: `1px solid ${TEAL}44` }}>BETA</span>
          </div>
          <div style={{ fontSize: 12, color: MUTED }}>MacambaX AI · April 2026 · marceloferreira@macambax.ai</div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {["overview", "providers", "carbon"].map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)} style={{
              background: activeTab === tab ? `${TEAL}22` : "transparent",
              border: `1px solid ${activeTab === tab ? TEAL : BORDER}`,
              color: activeTab === tab ? TEAL : MUTED,
              padding: "6px 14px", borderRadius: 8, cursor: "pointer",
              fontSize: 12, textTransform: "capitalize", letterSpacing: "0.04em",
            }}>{tab}</button>
          ))}
        </div>
      </div>

      {activeTab === "overview" && (
        <>
          {/* KPI Row */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14, marginBottom: 20 }}>
            <MetricCard label="Monthly Spend" value={`$${totalMonthly.toFixed(2)}`} sub="4 providers · Apr 2026" color={ORANGE} icon="💸" />
            <MetricCard label="Today's Spend" value="$4.13" sub="+12% vs yesterday" color={RED} icon="📈" />
            <MetricCard label="Tokens This Month" value="4.2M" sub="across all providers" color={TEAL} icon="🔢" />
            <MetricCard label="CO₂ Equivalent" value={`${totalCarbon.toFixed(2)} kg`} sub="↓8% vs last month" color={INDIGO} icon="🌍" />
          </div>

          {/* Charts row */}
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 14, marginBottom: 20 }}>
            {/* Spend trend */}
            <div style={{ background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12, padding: "18px 20px" }}>
              <div style={{ fontSize: 12, color: MUTED, marginBottom: 14, textTransform: "uppercase", letterSpacing: "0.06em" }}>Daily Spend — This Week</div>
              <ResponsiveContainer width="100%" height={180}>
                <LineChart data={trendData}>
                  <XAxis dataKey="day" tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `$${v}`} />
                  <Tooltip content={<CustomTooltip />} />
                  <Line type="monotone" dataKey="gcp" stroke={TEAL} strokeWidth={2} dot={false} name="GCP" />
                  <Line type="monotone" dataKey="openai" stroke={AMBER} strokeWidth={2} dot={false} name="OpenAI" />
                  <Line type="monotone" dataKey="total" stroke={ORANGE} strokeWidth={2.5} dot={{ fill: ORANGE, r: 3 }} name="Total" strokeDasharray="5 3" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Provider breakdown */}
            <div style={{ background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12, padding: "18px 20px" }}>
              <div style={{ fontSize: 12, color: MUTED, marginBottom: 14, textTransform: "uppercase", letterSpacing: "0.06em" }}>Monthly by Provider</div>
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={providers.map(p => ({ name: p.name.split(" ")[0], cost: p.monthly, color: p.color }))} barSize={32}>
                  <XAxis dataKey="name" tick={{ fill: MUTED, fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: MUTED, fontSize: 10 }} axisLine={false} tickLine={false} tickFormatter={v => `$${v}`} />
                  <Tooltip content={<CustomTooltip />} formatter={(v) => [`$${v}`, "Monthly"]} />
                  <Bar dataKey="cost" radius={[4, 4, 0, 0]}>
                    {providers.map((p, i) => <Cell key={i} fill={p.color} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Alerts + Model Breakdown */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            {/* Alerts */}
            <div style={{ background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12, padding: "18px 20px" }}>
              <div style={{ fontSize: 12, color: MUTED, marginBottom: 14, textTransform: "uppercase", letterSpacing: "0.06em" }}>Alerts & Thresholds</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {alerts.map((a, i) => (
                  <div key={i} style={{
                    display: "flex", alignItems: "flex-start", gap: 10,
                    background: "#0D1117", borderRadius: 8, padding: "10px 12px",
                    borderLeft: `3px solid ${a.level === "danger" ? RED : a.level === "warn" ? AMBER : TEAL}`,
                  }}>
                    <AlertBadge level={a.level} />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 12, color: TEXT }}>{a.msg}</div>
                      <div style={{ fontSize: 10, color: MUTED, marginTop: 2 }}>{a.time}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Top models */}
            <div style={{ background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12, padding: "18px 20px" }}>
              <div style={{ fontSize: 12, color: MUTED, marginBottom: 14, textTransform: "uppercase", letterSpacing: "0.06em" }}>Top Models by Cost</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 9 }}>
                {modelBreakdown.map((m, i) => (
                  <div key={i}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                      <span style={{ fontSize: 11, color: TEXT }}>{m.name}</span>
                      <span style={{ fontSize: 11, color: MUTED, fontFamily: "monospace" }}>${m.cost.toFixed(2)}</span>
                    </div>
                    <div style={{ height: 4, background: BORDER, borderRadius: 2 }}>
                      <div style={{ width: `${m.pct}%`, height: "100%", background: m.color, borderRadius: 2, transition: "width 0.6s ease" }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}

      {activeTab === "providers" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          {providers.map(p => (
            <div key={p.id} style={{
              background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12,
              padding: "20px 22px", borderTop: `3px solid ${p.color}`,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ fontSize: 20 }}>{p.icon}</span>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: TEXT }}>{p.name}</div>
                    <div style={{ fontSize: 11, color: MUTED }}>{p.plan}</div>
                  </div>
                </div>
                <div style={{ fontSize: 22, fontWeight: 700, color: p.color, fontFamily: "monospace" }}>
                  ${p.monthly.toFixed(2)}
                </div>
              </div>
              <div style={{ marginBottom: 14 }}>
                <div style={{ fontSize: 11, color: MUTED, marginBottom: 6 }}>Usage</div>
                <div style={{ fontSize: 12, color: TEXT }}>{p.tokens}</div>
              </div>
              <div>
                <div style={{ fontSize: 11, color: MUTED, marginBottom: 6 }}>Daily Trend (This Week)</div>
                <ResponsiveContainer width="100%" height={60}>
                  <LineChart data={weekLabels.map((day, i) => ({ day, cost: p.daily[i] }))}>
                    <Line type="monotone" dataKey="cost" stroke={p.color} strokeWidth={2} dot={false} />
                    <XAxis dataKey="day" hide />
                    <YAxis hide />
                    <Tooltip content={<CustomTooltip />} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div style={{ marginTop: 12, display: "flex", gap: 6 }}>
                <button style={{ flex: 1, background: `${p.color}18`, border: `1px solid ${p.color}44`, color: p.color, padding: "6px 0", borderRadius: 6, cursor: "pointer", fontSize: 11 }}>
                  Set Budget Alert
                </button>
                <button style={{ flex: 1, background: "transparent", border: `1px solid ${BORDER}`, color: MUTED, padding: "6px 0", borderRadius: 6, cursor: "pointer", fontSize: 11 }}>
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === "carbon" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          <div style={{ background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12, padding: "20px 22px" }}>
            <div style={{ fontSize: 12, color: MUTED, marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.06em" }}>CO₂ by Provider</div>
            <div style={{ fontSize: 11, color: MUTED, marginBottom: 16 }}>Estimated monthly footprint</div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={carbon} barSize={40}>
                <XAxis dataKey="provider" tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `${v}kg`} />
                <Tooltip formatter={(v) => [`${v} kg CO₂`, "Footprint"]} contentStyle={{ background: CARD, border: `1px solid ${BORDER}` }} />
                <Bar dataKey="kg" radius={[4, 4, 0, 0]}>
                  {carbon.map((c, i) => <Cell key={i} fill={c.color} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ background: CARD, border: `1px solid ${BORDER}`, borderRadius: 12, padding: "20px 22px" }}>
            <div style={{ fontSize: 12, color: MUTED, marginBottom: 16, textTransform: "uppercase", letterSpacing: "0.06em" }}>Carbon Breakdown</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {carbon.map((c, i) => (
                <div key={i}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ fontSize: 12, color: TEXT }}>{c.provider}</span>
                    <span style={{ fontSize: 12, fontFamily: "monospace", color: MUTED }}>{c.kg} kg CO₂</span>
                  </div>
                  <div style={{ height: 6, background: BORDER, borderRadius: 3 }}>
                    <div style={{ width: `${(c.kg / totalCarbon) * 100}%`, height: "100%", background: c.color, borderRadius: 3 }} />
                  </div>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 20, padding: "12px 14px", background: `${TEAL}11`, border: `1px solid ${TEAL}33`, borderRadius: 8 }}>
              <div style={{ fontSize: 11, color: TEAL, marginBottom: 4 }}>🌿 Total this month</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: TEXT, fontFamily: "monospace" }}>{totalCarbon.toFixed(2)} kg CO₂</div>
              <div style={{ fontSize: 11, color: MUTED, marginTop: 2 }}>Equivalent to driving ~1.8 miles</div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{ marginTop: 24, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontSize: 10, color: MUTED }}>MacambaX AI LLC · AI Cost Tracker · macambax.ai</div>
        <div style={{ display: "flex", gap: 6 }}>
          <div style={{ width: 8, height: 8, borderRadius: "50%", background: TEAL }} />
          <span style={{ fontSize: 10, color: MUTED }}>All providers synced · 2 min ago</span>
        </div>
      </div>
    </div>
  );
}
