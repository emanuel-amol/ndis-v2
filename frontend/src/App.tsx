// src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/login";
import AdminDashboard from "./pages/dashboards/admin";
import ProviderDashboard from "./pages/dashboards/provider";
import WorkerDashboard from "./pages/dashboards/worker";
import FinanceDashboard from "./pages/dashboards/finance";

import NDISReferralForm from "./pages/participants/Referralform/form";

import CareSetup from "./pages/participants/Care/CareSetup";
import CarePlanEditor from "./pages/participants/Care/CarePlanEditor";
import CareSignoff from "./pages/participants/Care/CareSignOff";
import RiskAssessmentEditor from "./pages/participants/Care/RiskAssessmentEditor";

// EXTRA PAGES
import Participants from "./pages/participants/Participants";
import ParticipantProfile from "./pages/participants/profile";
import ProviderReferralDashboard from "./pages/participants/provider";
import Documents from "./pages/documents/Documents";
import SilHomes from "./pages/sil/SilHomes";
import DynamicData from "./pages/admin/DynamicData";
import Dashboard from "./pages/Dashboard";

type Role = "admin" | "coordinator" | "worker" | "finance";

function RequireRole({ role, children }: { role: Role; children: React.ReactNode }) {
  const current = (localStorage.getItem("ndis_role") || "") as Role;
  return current === role ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />

        {/* Public referral form - no authentication required */}
        <Route path="/referral" element={<NDISReferralForm />} />

        {/* Dashboards by role */}
        <Route
          path="/admin"
          element={
            <RequireRole role="admin">
              <AdminDashboard />
            </RequireRole>
          }
        />
        <Route
          path="/provider"
          element={
            <RequireRole role="coordinator">
              <ProviderDashboard />
            </RequireRole>
          }
        />
        <Route
          path="/worker"
          element={
            <RequireRole role="worker">
              <WorkerDashboard />
            </RequireRole>
          }
        />
        <Route
          path="/finance"
          element={
            <RequireRole role="finance">
              <FinanceDashboard />
            </RequireRole>
          }
        />

        {/* Generic Dashboard (coordinator view) */}
        <Route
          path="/dashboard"
          element={
            <RequireRole role="coordinator">
              <Dashboard />
            </RequireRole>
          }
        />

        {/* Admin-specific routes */}
        <Route
          path="/admin/dynamic-data"
          element={
            <RequireRole role="admin">
              <DynamicData />
            </RequireRole>
          }
        />

        {/* Referrals - Protected */}
        <Route
          path="/participants/referral/new"
          element={
            <RequireRole role="coordinator">
              <NDISReferralForm />
            </RequireRole>
          }
        />

        {/* Participants & profile - Protected */}
        <Route
          path="/participants"
          element={
            <RequireRole role="coordinator">
              <Participants />
            </RequireRole>
          }
        />
        <Route
          path="/participants/profile"
          element={
            <RequireRole role="coordinator">
              <ParticipantProfile />
            </RequireRole>
          }
        />

        {/* Provider referral dashboard (participants/provider page) - Protected */}
        <Route
          path="/participants/provider"
          element={
            <RequireRole role="coordinator">
              <ProviderReferralDashboard />
            </RequireRole>
          }
        />

        {/* Documents - Protected */}
        <Route
          path="/documents"
          element={
            <RequireRole role="coordinator">
              <Documents />
            </RequireRole>
          }
        />

        {/* SIL Homes - Protected */}
        <Route
          path="/sil-homes"
          element={
            <RequireRole role="coordinator">
              <SilHomes />
            </RequireRole>
          }
        />

        {/* Care flow - Protected */}
        <Route
          path="/care/setup/:participantId"
          element={
            <RequireRole role="coordinator">
              <CareSetup />
            </RequireRole>
          }
        />
        <Route
          path="/care/plan/:participantId/edit"
          element={
            <RequireRole role="coordinator">
              <CarePlanEditor />
            </RequireRole>
          }
        />
        <Route
          path="/care/risk/:participantId/edit"
          element={
            <RequireRole role="coordinator">
              <RiskAssessmentEditor />
            </RequireRole>
          }
        />
        <Route
          path="/care/signoff/:participantId"
          element={
            <RequireRole role="coordinator">
              <CareSignoff />
            </RequireRole>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}