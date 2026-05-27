function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
}

export function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
}

export function GET() {
  return jsonResponse(
    {
      status: "error",
      error: "method_not_allowed",
      message: "Use POST to submit an agent payload.",
      allowed_methods: ["POST"],
      submission_status: "safe_stopped",
      proof_origin: "target_system"
    },
    405
  );
}

export async function POST(request) {
  let payload = {};

  try {
    payload = await request.json();
  } catch {
    return jsonResponse(
      {
        status: "rejected",
        error: "invalid_json",
        message: "Request body must be valid JSON.",
        submission_status: "invalid_payload",
        proof_origin: "target_system"
      },
      400
    );
  }

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
    return jsonResponse(
      {
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
      },
      400
    );
  }

  return jsonResponse({
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
}