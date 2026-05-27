module.exports = function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({
      status: "error",
      error: "method_not_allowed",
      message: "Use POST to submit an agent payload.",
      allowed_methods: ["POST"],
      submission_status: "safe_stopped",
      proof_origin: "target_system"
    });
  }

  const payload = req.body || {};

  const requiredFields = [
    "agent_name",
    "task_id",
    "output_format",
    "output",
    "confidence"
  ];

  const missingFields = requiredFields.filter((field) => {
    return (
      payload[field] === undefined ||
      payload[field] === null ||
      payload[field] === ""
    );
  });

  const taskId =
    typeof payload.task_id === "string" && payload.task_id.length > 0
      ? payload.task_id
      : "unknown";

  const now = new Date().toISOString();

  if (missingFields.length > 0) {
    return res.status(400).json({
      status: "rejected",
      receipt_id: `rcpt_${Date.now()}_rejected`,
      task_id: taskId,
      received_at: now,
      submission_status: "invalid_payload",
      proof_origin: "target_system",
      validation: {
        status: "failed",
        required_fields_present: false,
        missing_fields: missingFields,
        task_id_exists: taskId !== "unknown",
        schema_version: "0.3-route-hardening"
      }
    });
  }

  return res.status(200).json({
    status: "received",
    receipt_id: `rcpt_${Date.now()}`,
    task_id: taskId,
    received_at: now,
    submission_status: "submitted_with_receipt",
    proof_origin: "target_system",
    validation: {
      status: "passed",
      required_fields_present: true,
      task_id_exists: true,
      schema_version: "0.3-route-hardening"
    }
  });
};