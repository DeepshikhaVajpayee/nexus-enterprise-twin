"use client";

import { useEffect, useMemo, useState } from "react";
import ReactFlow, { Background, Controls, MarkerType } from "reactflow";
import "reactflow/dist/style.css";
import { api } from "@/lib/api";

export default function Home() {
  const [risk, setRisk] = useState<any>(null);
  const [brief, setBrief] = useState<any>(null);
  const [simulation, setSimulation] = useState<any>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
const [timeline, setTimeline] = useState<any[]>([]);
  const [briefing, setBriefing] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<any>(null);
const [cooQuestion, setCooQuestion] = useState("");
const [cooAnswer, setCooAnswer] = useState<any>(null);
const [cooLoading, setCooLoading] = useState(false);

  const [graph, setGraph] = useState<any[]>([
    { source: "Project Alpha", relation: "DEPENDS_ON", target: "Project Beta" },
    { source: "Project Beta", relation: "OWNED_BY", target: "Team X" },
    { source: "Team X", relation: "HAS_RISK", target: "Resource Overload" },
  ]);

  useEffect(() => {
    refreshData();
  }, []);

  function refreshData() {
    api.get("/risk/P1").then((res) => setRisk(res.data));
    api.get("/coo/brief").then((res) => setBrief(res.data));
    api.get("/events").then((res) => setEvents(res.data)).catch(() => {});
    api.get("/autonomous-alerts").then((res) => { console.log("ALERTS", res.data); setAlerts(res.data); }).catch(console.error);
api.get("/timeline").then((res) => setTimeline(res.data)).catch(() => {});
    api.get("/executive/briefing").then((res) => setBriefing(res.data)).catch(() => {});

    api.get("/graph/live").then((res) => {
      if (res.data && res.data.length > 0) setGraph(res.data);
    }).catch(() => {});
  }

  function runSimulation(engineers: number) {
    api.get(`/simulate/team-loss/${engineers}`).then((res) => {
      setSimulation(res.data);
    });
  }

  function createEvent(eventType: string) {
    api.post("/events", {
      event_type: eventType,
      entity: "Project Beta",
      payload: {
        severity: "High",
        source: "Mission Control UI"
      }
    }).then(() => {
      refreshData();
      api.get("/autonomous-alerts").then((res) => { console.log("ALERTS", res.data); setAlerts(res.data); }).catch(console.error);
      api.get("/timeline").then((res) => setTimeline(res.data)).catch(() => {});
    });
  }

  async function askCoo() {
    if (!cooQuestion.trim()) return;
    setCooLoading(true);

    try {
      const res = await api.post("/coo/ask", {
        question: cooQuestion,
      });
      setCooAnswer(res.data);
    } catch (error) {
      setCooAnswer({ answer: "AI COO is temporarily unavailable." });
    } finally {
      setCooLoading(false);
    }
  }

  const nodes = useMemo(() => {
    const names = Array.from(new Set(graph.flatMap((r: any) => [r.source, r.target])));

    return names.map((name, index) => ({
      id: name,
      position: { x: 100 + index * 260, y: 160 },
      data: { label: name },
      style: nodeStyle(
        name.includes("Team")
          ? "amber"
          : name.includes("Risk") || name.includes("Overload")
          ? "red"
          : "cyan"
      ),
    }));
  }, [graph]);

  const edges = useMemo(() => {
    return graph.map((r: any, i: number) => ({
      id: `edge-${i}`,
      source: r.source,
      target: r.target,
      label: r.relation,
      animated: true,
      markerEnd: { type: MarkerType.ArrowClosed },
      style: { stroke: "#22d3ee", strokeWidth: 2 },
      labelStyle: { fill: "#fbbf24", fontWeight: 700 },
    }));
  }, [graph]);

  function getNodeIntel(name: string) {
    const outgoing = graph.filter((r) => r.source === name);
    const incoming = graph.filter((r) => r.target === name);

    return {
      name,
      incoming,
      outgoing,
      riskHint:
        name.includes("Alpha")
          ? "High delivery exposure due to downstream dependency."
          : name.includes("Beta")
          ? "Dependency owner for Project Alpha."
          : name.includes("Team")
          ? "Operational bottleneck and overload risk."
          : name.includes("Overload")
          ? "Critical resource risk affecting delivery."
          : "No critical risk detected.",
    };
  }

  return (
    <main className="min-h-screen bg-[#050505] p-8 text-white">
      <section className="border-b border-cyan-400/30 pb-6">
        <p className="text-xs tracking-[0.45em] text-cyan-300">
          NEXUS ENTERPRISE TWIN
        </p>
        <h1 className="mt-3 text-5xl font-black">Enterprise Mission Control</h1>
        <p className="mt-4 max-w-3xl text-zinc-400">
          Live graph reasoning, event intelligence, risk prediction, simulation, and AI COO recommendations.
        </p>
      </section>

      <section className="mt-8 grid grid-cols-1 gap-4 lg:grid-cols-4">
        <Card title="ENTERPRISE HEALTH" value="71%" tone="cyan" />
        <Card title="CRITICAL RISKS" value="03" tone="amber" />
        <Card title="AI CONFIDENCE" value={`${brief?.confidence ?? "--"}`} tone="silver" />
        <Card title="EXECUTIVE ALERTS" value={`${alerts.length}`} tone="amber" />
      </section>

      <section className="mt-6 rounded-2xl border border-cyan-400/20 bg-zinc-950 p-6">
        <p className="text-xs tracking-[0.3em] text-cyan-300">
          EXECUTIVE INTELLIGENCE BRIEFING
        </p>

        <h2 className="mt-4 text-3xl font-black text-white">
          {briefing?.title ?? "Generating executive briefing..."}
        </h2>

        <p className="mt-3 max-w-4xl text-zinc-400">
          {briefing?.summary ?? "Waiting for enterprise signals..."}
        </p>

        <div className="mt-5 grid grid-cols-1 gap-3 md:grid-cols-3">
          <MiniCard title="Enterprise Status" value={briefing?.enterprise_health?.status ?? "--"} />
          <MiniCard title="Delivery Risk" value={`${briefing?.enterprise_health?.delay_probability ?? "--"}%`} />
          <MiniCard title="Confidence" value={`${briefing?.enterprise_health?.confidence ?? "--"}`} />
        </div>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2 rounded-2xl border border-cyan-400/20 bg-zinc-950 p-6">
          <p className="text-xs tracking-[0.3em] text-cyan-300">
            LIVE ENTERPRISE KNOWLEDGE GRAPH
          </p>

          <div className="mt-5 h-[430px] overflow-hidden rounded-xl border border-zinc-800 bg-black">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              fitView
              onNodeClick={(_, node) => setSelectedNode(getNodeIntel(node.id))}
            >
              <Background />
              <Controls />
            </ReactFlow>
          </div>
        </div>

        <div className="rounded-2xl border border-amber-400/20 bg-zinc-950 p-6">
          <p className="text-xs tracking-[0.3em] text-amber-300">
            NODE INTELLIGENCE
          </p>

          {selectedNode ? (
            <div>
              <h2 className="mt-5 text-2xl font-black text-white">{selectedNode.name}</h2>
              <p className="mt-3 text-sm text-zinc-400">{selectedNode.riskHint}</p>

              <div className="mt-5">
                <p className="text-xs tracking-[0.25em] text-zinc-500">INCOMING</p>
                <div className="mt-2 space-y-2">
                  {selectedNode.incoming.length === 0 && (
                    <p className="text-sm text-zinc-600">No incoming dependencies.</p>
                  )}
                  {selectedNode.incoming.map((r: any, i: number) => (
                    <IntelRow key={i} text={`${r.source} -> ${r.relation}`} />
                  ))}
                </div>
              </div>

              <div className="mt-5">
                <p className="text-xs tracking-[0.25em] text-zinc-500">OUTGOING</p>
                <div className="mt-2 space-y-2">
                  {selectedNode.outgoing.length === 0 && (
                    <p className="text-sm text-zinc-600">No outgoing dependencies.</p>
                  )}
                  {selectedNode.outgoing.map((r: any, i: number) => (
                    <IntelRow key={i} text={`${r.relation} -> ${r.target}`} />
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <p className="mt-5 text-sm text-zinc-500">
              Click any graph node to inspect dependencies, ownership, and risk signals.
            </p>
          )}
        </div>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Panel title="RISK RADAR" tone="amber">
          <h2 className="mt-6 text-5xl font-black text-amber-300">
            {risk?.delay_probability ?? "--"}%
          </h2>
          <p className="mt-2 text-zinc-400">{risk?.project ?? "Project"} delay probability</p>
          <ul className="mt-6 space-y-2 text-sm text-zinc-400">
            {risk?.root_causes?.map((x: string, i: number) => (
              <li key={i}>- {x}</li>
            ))}
          </ul>
        </Panel>

        <Panel title="EVENT INGESTION ENGINE" tone="cyan">
          <p className="mt-4 text-sm text-zinc-400">
            Simulate enterprise signals entering Nexus.
          </p>

          <div className="mt-5 flex flex-wrap gap-3">
            <button onClick={() => createEvent("DEPENDENCY_BLOCKED")} className="rounded-lg border border-amber-400/30 px-4 py-2 text-amber-300 hover:bg-amber-400/10">
              Dependency Blocked
            </button>
            <button onClick={() => createEvent("TICKET_CREATED")} className="rounded-lg border border-cyan-400/30 px-4 py-2 text-cyan-300 hover:bg-cyan-400/10">
              Ticket Created
            </button>
            <button onClick={() => createEvent("EMPLOYEE_LEFT")} className="rounded-lg border border-red-400/30 px-4 py-2 text-red-300 hover:bg-red-400/10">
              Employee Left
            </button>
          </div>

          <div className="mt-6 max-h-[230px] space-y-3 overflow-auto">
            {timeline.length === 0 && (
              <p className="text-sm text-zinc-600">No enterprise timeline yet.</p>
            )}

            {timeline.map((item: any, i: number) => (
              <div key={i} className="rounded-xl border border-zinc-800 bg-black p-4">
                <p className="text-sm font-bold text-cyan-300">{item.title}</p>
                <p className="mt-1 text-xs text-zinc-500">{item.description}</p>
                <p className="mt-2 text-xs text-amber-300">{item.time}</p>
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Panel title="SCENARIO SIMULATION ENGINE" tone="cyan">
          <h2 className="mt-4 text-2xl font-bold">
            What happens if Team X loses engineers?
          </h2>

          <div className="mt-5 flex flex-wrap gap-3">
            <button onClick={() => runSimulation(1)} className="rounded-lg border border-cyan-400/30 px-4 py-2 text-cyan-300 hover:bg-cyan-400/10">
              Lose 1 Engineer
            </button>
            <button onClick={() => runSimulation(2)} className="rounded-lg border border-amber-400/30 px-4 py-2 text-amber-300 hover:bg-amber-400/10">
              Lose 2 Engineers
            </button>
            <button onClick={() => runSimulation(3)} className="rounded-lg border border-red-400/30 px-4 py-2 text-red-300 hover:bg-red-400/10">
              Lose 3 Engineers
            </button>
          </div>

          {simulation && (
            <div className="mt-6 grid grid-cols-1 gap-3 md:grid-cols-3">
              <MiniCard title="Delay" value={`${simulation.project_delay_days} days`} />
              <MiniCard title="Risk Increase" value={`${simulation.risk_increase_percent}%`} />
              <MiniCard title="Affected" value={`${simulation.affected_projects.length}`} />
            </div>
          )}
        </Panel>
<Panel title="EXECUTIVE ALERT CENTER" tone="amber">
          <div className="mt-5 space-y-3">
            {alerts.length === 0 && (
              <p className="text-sm text-zinc-600">No executive alerts yet.</p>
            )}

            {alerts.map((alert: any, i: number) => (
              <div key={i} className="rounded-xl border border-amber-400/20 bg-black p-4">
                <p className="text-xs tracking-[0.25em] text-amber-300">
                  {alert.severity}
                </p>
                <h3 className="mt-2 text-lg font-black text-white">
                  {alert.title}
                </h3>
                <p className="mt-2 text-sm text-zinc-400">
                  {alert.reason}
                </p>
                <p className="mt-3 text-sm text-cyan-300">
                  {alert.recommended_action}
                </p>
              </div>
            ))}
          </div>
        </Panel>
        <Panel title="AI COO AGENT" tone="amber">
          <h2 className="mt-4 text-2xl font-bold">
            Ask the AI COO anything about enterprise risk, projects, teams, or decisions.
          </h2>

          <div className="mt-5 flex gap-3">
            <input
              value={cooQuestion}
              onChange={(e) => setCooQuestion(e.target.value)}
              placeholder="Ask: What should leadership focus on today?"
              className="w-full rounded-lg border border-zinc-800 bg-black px-4 py-3 text-sm text-white outline-none focus:border-amber-400"
            />

            <button
              onClick={askCoo}
              disabled={cooLoading}
              className="rounded-lg border border-amber-400/30 px-5 py-3 text-sm font-bold text-amber-300 hover:bg-amber-400/10 disabled:opacity-50"
            >
              {cooLoading ? "Thinking..." : "Ask"}
            </button>
          </div>

          {cooAnswer && (
            <div className="mt-6 rounded-xl border border-zinc-800 bg-black p-5">
              <p className="text-xs tracking-[0.25em] text-amber-300">AI COO RESPONSE</p>

              <p className="mt-4 text-sm text-zinc-300">
                {cooAnswer.answer}
              </p>

              {cooAnswer.health && (
                <div className="mt-5 grid grid-cols-2 gap-3">
                  <MiniCard title="Health Score" value={`${cooAnswer.health.score}`} />
                  <MiniCard title="Status" value={cooAnswer.health.status} />
                </div>
              )}

              {cooAnswer.recommendations && (
                <div className="mt-5 space-y-3">
                  {cooAnswer.recommendations.map((rec: any, i: number) => (
                    <div key={i} className="rounded-lg border border-zinc-800 p-3">
                      <p className="text-xs text-amber-300">{rec.priority}</p>
                      <p className="mt-1 text-sm text-zinc-400">{rec.action}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </Panel>
      </section>
    </main>
  );
}

function nodeStyle(tone: string) {
  const color = tone === "amber" ? "#f59e0b" : tone === "red" ? "#f87171" : "#22d3ee";
  return {
    background: "#050505",
    color,
    border: `1px solid ${color}`,
    borderRadius: 14,
    padding: 14,
    fontWeight: 800,
    boxShadow: `0 0 25px ${color}30`,
  };
}

function Card({ title, value, tone }: any) {
  const color =
    tone === "amber"
      ? "border-amber-400/20 text-amber-300"
      : tone === "silver"
      ? "border-zinc-700 text-zinc-300"
      : "border-cyan-400/20 text-cyan-300";

  return (
    <div className={`rounded-2xl border ${color} bg-zinc-950 p-6`}>
      <p className="text-xs tracking-[0.3em]">{title}</p>
      <h2 className="mt-4 text-4xl font-black text-white">{value}</h2>
    </div>
  );
}

function Panel({ title, tone, children }: any) {
  const color = tone === "amber" ? "border-amber-400/20 text-amber-300" : "border-cyan-400/20 text-cyan-300";
  return (
    <div className={`rounded-2xl border ${color} bg-zinc-950 p-6`}>
      <p className="text-xs tracking-[0.3em]">{title}</p>
      {children}
    </div>
  );
}

function MiniCard({ title, value }: any) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-black p-4">
      <p className="text-xs text-zinc-500">{title}</p>
      <h3 className="mt-2 text-xl font-black text-white">{value}</h3>
    </div>
  );
}

function IntelRow({ text }: any) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-black p-3 text-sm text-zinc-400">
      {text}
    </div>
  );
}

















