"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

const demoUsers = [
  { label: "CEO", email: "ceo@nexus.com", password: "ceo123" },
  { label: "COO", email: "coo@nexus.com", password: "coo123" },
  { label: "Manager", email: "manager@nexus.com", password: "manager123" },
  { label: "Employee", email: "employee@nexus.com", password: "employee123" },
];

export default function AuthGate({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const savedUser = localStorage.getItem("nexus_user");
    if (savedUser) setUser(JSON.parse(savedUser));
  }, []);

  async function login(email: string, password: string) {
    setLoading(true);

    try {
      const res = await api.post("/auth/login", { email, password });

      if (res.data.success) {
        localStorage.setItem("nexus_token", res.data.access_token);
        localStorage.setItem("nexus_user", JSON.stringify(res.data.user));
        setUser(res.data.user);
      } else {
        alert("Invalid login");
      }
    } catch (error) {
      alert("Login failed. Check backend.");
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("nexus_token");
    localStorage.removeItem("nexus_user");
    setUser(null);
  }

  if (!user) {
    return (
      <main className="min-h-screen bg-[#050505] p-8 text-white">
        <section className="mx-auto mt-24 max-w-3xl rounded-3xl border border-cyan-400/20 bg-zinc-950 p-8">
          <p className="text-xs tracking-[0.45em] text-cyan-300">
            NEXUS ENTERPRISE TWIN
          </p>

          <h1 className="mt-4 text-5xl font-black">Executive Login</h1>

          <p className="mt-4 text-zinc-400">
            Choose a demo role to access the AI COO mission control dashboard.
          </p>

          <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2">
            {demoUsers.map((item) => (
              <button
                key={item.email}
                onClick={() => login(item.email, item.password)}
                disabled={loading}
                className="rounded-2xl border border-cyan-400/20 bg-black p-6 text-left hover:bg-cyan-400/10 disabled:opacity-50"
              >
                <p className="text-xs tracking-[0.3em] text-cyan-300">
                  LOGIN AS
                </p>
                <h2 className="mt-3 text-3xl font-black">{item.label}</h2>
                <p className="mt-2 text-sm text-zinc-500">{item.email}</p>
              </button>
            ))}
          </div>
        </section>
      </main>
    );
  }

  return (
    <>
      <div className="fixed right-6 top-6 z-50 rounded-full border border-cyan-400/30 bg-black px-5 py-3 text-sm text-white shadow-lg">
        <span className="text-cyan-300">{user.role}</span>
        <span className="mx-2 text-zinc-600">|</span>
        <button onClick={logout} className="text-amber-300 hover:text-amber-200">
          Logout
        </button>
      </div>

      {children}
    </>
  );
}
