// src/pages/participants/provider.tsx
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8000/api/v1";

type Referral = {
  id: string;
  created_at?: string;
  participantName: string;
  status: "new" | "in_review" | "approved" | "rejected";
  serviceType?: string;
};

const mockData: Referral[] = [
  { id: "R-0001", participantName: "Alex Johnson", status: "new", serviceType: "Physio" },
  { id: "R-0002", participantName: "Sam Lee", status: "in_review", serviceType: "Chiro" },
  { id: "R-0003", participantName: "Mia Patel", status: "approved", serviceType: "Psychologist" },
];

const ProviderReferralDashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [referrals, setReferrals] = useState<Referral[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError("");

        // Try real API first
        const res = await fetch(`${API_BASE_URL}/participants/referrals`);
        if (!res.ok) throw new Error("Failed to fetch referrals");
        const data = await res.json();

        // Map API → existing UI shape (non-breaking)
        const mapped: Referral[] = (Array.isArray(data) ? data : []).map((r: any) => ({
          id: String(r.id ?? r.referral_id ?? r.reference ?? ""),
          created_at: r.created_at,
          participantName:
            `${r.first_name ?? r.participant_first_name ?? ""} ${r.last_name ?? r.participant_last_name ?? ""}`.trim() ||
            r.participantName ||
            "Unnamed",
          status: (r.status ?? "new") as Referral["status"],
          serviceType: r.referred_for ?? r.serviceType ?? "-",
        }));

        setReferrals(mapped);
      } catch (e: any) {
        // Fallback to mock
        setReferrals(mockData);
        setError(e?.message || "Failed to load referrals (showing demo data)");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-start justify-between mb-1">
          <div>
            <h1 className="text-3xl font-bold text-blue-600">Provider Dashboard</h1>
            <p className="text-gray-600">Review new referrals and manage participant intake.</p>
          </div>

          {/* NEW: create-referral button */}
          <Link
            to="/provider/referrals/new"
            className="inline-flex items-center gap-2 rounded-lg bg-blue-600 text-white px-4 py-2 hover:opacity-90"
          >
            + New Referral
          </Link>
        </div>

        {error && (
          <div className="mt-4 mb-4 p-3 rounded border border-yellow-300 bg-yellow-50 text-yellow-800">
            {error}
          </div>
        )}

        {loading ? (
          <div className="py-10 text-center text-gray-500">Loading referrals…</div>
        ) : referrals.length === 0 ? (
          <div className="py-10 text-center text-gray-500">No referrals found.</div>
        ) : (
          <div className="mt-4 overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-gray-600 border-b">
                  <th className="py-3 pr-4">Referral ID</th>
                  <th className="py-3 pr-4">Participant</th>
                  <th className="py-3 pr-4">Service</th>
                  <th className="py-3 pr-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {referrals.map((r) => (
                  <tr key={r.id} className="border-b last:border-0">
                    <td className="py-3 pr-4 font-mono">{r.id}</td>
                    <td className="py-3 pr-4">{r.participantName}</td>
                    <td className="py-3 pr-4">{r.serviceType || "-"}</td>
                    <td className="py-3 pr-4">
                      <span
                        className={`px-2 py-1 rounded text-xs ${
                          r.status === "new"
                            ? "bg-blue-100 text-blue-700"
                            : r.status === "in_review"
                            ? "bg-amber-100 text-amber-700"
                            : r.status === "approved"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {r.status.replace("_", " ")}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProviderReferralDashboard;
