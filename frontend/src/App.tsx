import { useEffect, useState } from "react";
import "./App.css";

interface Agent {
  name: string;
  load: number;
  capacity: number;
  available: boolean;
}

interface DashboardData {
  total_tickets: number;
  open_tickets: number;
  escalated_tickets: number;
  high_risk_tickets: number;
  agents: Agent[];
}

interface Ticket {
  id: number;
  customer_name: string;
  message: string;
  category: string;
  urgency: string;
  sla_deadline: string;
  sla_risk: string;
  status: string;
  assigned_agent: string | null;
}

function App() {
  const [dashboard, setDashboard] =
    useState<DashboardData | null>(null);

  const [customerName, setCustomerName] = useState("");
  const [message, setMessage] = useState("");

  const [createdTicket, setCreatedTicket] =
    useState<Ticket | null>(null);

  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [currentTime, setCurrentTime] = useState(new Date());

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Load dashboard data
  const loadDashboard = () => {
    fetch("http://127.0.0.1:8000/api/dashboard/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Dashboard request failed");
        }

        return response.json();
      })
      .then((data) => {
        setDashboard(data);
        setError("");
      })
      .catch(() => {
        setError("Unable to connect to Django backend.");
      });
  };

  // Load all tickets
  const loadTickets = () => {
    fetch("http://127.0.0.1:8000/api/tickets/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Ticket request failed");
        }

        return response.json();
      })
      .then((data) => {
        setTickets(data);
      })
      .catch(() => {
        setError("Unable to load tickets.");
      });
  };

  // Load data when page starts
  useEffect(() => {
    loadDashboard();
    loadTickets();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Create ticket
  const createTicket = async () => {
    if (!customerName.trim() || !message.trim()) {
      setError("Please enter customer name and ticket message.");
      return;
    }

    setLoading(true);
    setError("");
    setCreatedTicket(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/tickets/",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            customer_name: customerName,
            message: message,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Ticket creation failed");
      }

      const data = await response.json();

      setCreatedTicket(data);

      setCustomerName("");
      setMessage("");

      // Refresh dashboard and ticket table
      loadDashboard();
      loadTickets();

    } catch {
      setError("Unable to create ticket.");
    } finally {
      setLoading(false);
    }
  };

  const getRemainingTime = (deadline: string) => {
    const deadlineTime = new Date(deadline).getTime();
    const now = currentTime.getTime();

    const difference = deadlineTime - now;

    if (difference <= 0) {
      return "SLA Breached";
    }

    const totalSeconds = Math.floor(difference / 1000);

    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    if (hours > 0) {
      return `${hours}h ${minutes}m ${seconds}s`;
    }

    return `${minutes}m ${seconds}s`;
  };

  return (
    <div className="dashboard">

      {/* Header */}

      <header className="header">
        <div>
          <h1>SLA Support Dashboard</h1>

          <p>
            Smart Support Ticket Routing & Escalation System
          </p>
        </div>

        <div className="status">
          ● System Active
        </div>
      </header>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {/* Dashboard Statistics */}

      <section className="cards">

        <div className="card">
          <h3>Total Tickets</h3>

          <strong>
            {dashboard?.total_tickets ?? "-"}
          </strong>
        </div>

        <div className="card">
          <h3>Open Tickets</h3>

          <strong>
            {dashboard?.open_tickets ?? "-"}
          </strong>
        </div>

        <div className="card">
          <h3>High Risk</h3>

          <strong className="danger">
            {dashboard?.high_risk_tickets ?? "-"}
          </strong>
        </div>

        <div className="card">
          <h3>Escalated</h3>

          <strong className="warning">
            {dashboard?.escalated_tickets ?? "-"}
          </strong>
        </div>

      </section>

      {/* Create Ticket */}

      <section className="panel">

        <h2>Create Support Ticket</h2>

        <div className="form">

          <input
            type="text"
            placeholder="Customer name"
            value={customerName}
            onChange={(e) =>
              setCustomerName(e.target.value)
            }
          />

          <textarea
            placeholder="Describe the customer problem..."
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            rows={5}
          />

          <button
            onClick={createTicket}
            disabled={loading}
          >
            {loading
              ? "Processing..."
              : "Create Ticket"}
          </button>

        </div>

      </section>

      {/* Automation Result */}

      {createdTicket && (

        <section className="panel result">

          <h2>Automation Result</h2>

          <div className="result-grid">

            <div>
              <span>Ticket ID</span>

              <strong>
                #{createdTicket.id}
              </strong>
            </div>

            <div>
              <span>Category</span>

              <strong>
                {createdTicket.category}
              </strong>
            </div>

            <div>
              <span>Urgency</span>

              <strong>
                {createdTicket.urgency}
              </strong>
            </div>

            <div>
              <span>SLA Risk</span>

              <strong
                className={
                  createdTicket.sla_risk === "high"
                    ? "danger"
                    : ""
                }
              >
                {createdTicket.sla_risk}
              </strong>
            </div>

            <div>
              <span>Assigned Agent</span>

              <strong>
                {createdTicket.assigned_agent ??
                  "No agent available"}
              </strong>
            </div>

            <div>
              <span>Status</span>

              <strong>
                {createdTicket.status}
              </strong>
            </div>

          </div>

        </section>

      )}

      {/* Ticket Monitoring */}

      <section className="panel">

        <h2>Ticket Monitoring</h2>

        <div className="table-container">

          <table className="ticket-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Category</th>
                <th>Urgency</th>
                <th>SLA Risk</th>
                <th>SLA Remaining</th>
                <th>Agent</th>
                <th>Status</th>
              </tr>

            </thead>

            <tbody>

              {tickets.map((ticket) => (

                <tr key={ticket.id}>

                  <td>
                    #{ticket.id}
                  </td>

                  <td>
                    {ticket.customer_name}
                  </td>

                  <td className="capitalize">
                    {ticket.category}
                  </td>

                  <td>
                    <span
                      className={`badge ${ticket.urgency}`}
                    >
                      {ticket.urgency}
                    </span>
                  </td>

                  <td>
                    <span
                      className={`badge ${ticket.sla_risk}`}
                    >
                      {ticket.sla_risk}
                    </span>
                  </td>

                  <td>
                    <span
                      className={
                        getRemainingTime(ticket.sla_deadline) === "SLA Breached"
                          ? "sla-time breached"
                          : ticket.sla_risk === "high"
                          ? "sla-time high"
                          : ticket.sla_risk === "medium"
                          ? "sla-time medium"
                          : "sla-time low"
                      }
                    >
                      ⏱ {getRemainingTime(ticket.sla_deadline)}
                    </span>
                  </td>
                  
                  <td>
                    {ticket.assigned_agent ??
                      "Unassigned"}
                  </td>

                  <td>
                    <span
                      className={`status-badge ${ticket.status}`}
                    >
                      {ticket.status}
                    </span>
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </section>

      {/* Agent Queue */}

      <section className="panel">

        <h2>Agent Queue Load</h2>

        <div className="agent-list">

          {dashboard?.agents.map((agent) => {

            const percentage = Math.round(
              (agent.load / agent.capacity) * 100
            );

            return (

              <div
                className="agent"
                key={agent.name}
              >

                <div className="agent-info">

                  <div>

                    <strong>
                      {agent.name}
                    </strong>

                    <span>
                      {agent.load} / {agent.capacity} tickets
                    </span>

                  </div>

                  <span>
                    {agent.available
                      ? "Available"
                      : "Unavailable"}
                  </span>

                </div>

                <div className="progress-background">

                  <div
                    className="progress"
                    style={{
                      width: `${percentage}%`,
                    }}
                  />

                </div>

              </div>

            );

          })}

        </div>

      </section>

      {/* Automation Flow */}

      <section className="panel">

        <h2>Automation Flow</h2>

        <div className="flow">

          <div>Ticket</div>
          <span>→</span>

          <div>Classify</div>
          <span>→</span>

          <div>Urgency</div>
          <span>→</span>

          <div>SLA Risk</div>
          <span>→</span>

          <div>Route</div>
          <span>→</span>

          <div>Escalate</div>

        </div>

      </section>

    </div>
  );
}

export default App;