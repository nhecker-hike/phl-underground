import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { execSync } from "child_process";

const AIRTABLE_BASE_ID = "appxxq3x01pY9HMwa";
const AIRTABLE_TABLE_ID = "tblJsG1O5EDMFhLvU";

function callAirtable(toolName: string, args: Record<string, unknown>): unknown {
  const params = JSON.stringify({
    source_id: "airtable_oauth__pipedream",
    tool_name: toolName,
    arguments: args,
  });
  const result = execSync(`external-tool call '${params.replace(/'/g, "'\\''")}' 2>/dev/null`, {
    encoding: "utf-8",
    timeout: 15000,
  });
  return JSON.parse(result);
}

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // Subscribe endpoint — collect email for PHL Underground updates
  app.post("/api/subscribe", async (req, res) => {
    try {
      const { email } = req.body;

      if (!email || typeof email !== "string") {
        return res.status(400).json({ error: "Email is required" });
      }

      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        return res.status(400).json({ error: "Invalid email format" });
      }

      const normalizedEmail = email.toLowerCase().trim();

      // Check for duplicates
      try {
        const existing = callAirtable("airtable_oauth-list-records", {
          baseId: AIRTABLE_BASE_ID,
          tableId: AIRTABLE_TABLE_ID,
          filterByFormula: `{Email}='${normalizedEmail}'`,
          maxRecords: 1,
        });

        if (Array.isArray(existing) && existing.length > 0) {
          return res.status(200).json({ success: true, message: "You're already on the list" });
        }
      } catch {
        // If duplicate check fails, still try to create — worst case is a dupe
      }

      // Create the record
      callAirtable("airtable_oauth-create-multiple-records", {
        baseId: AIRTABLE_BASE_ID,
        tableId: AIRTABLE_TABLE_ID,
        records: [
          JSON.stringify({
            Email: normalizedEmail,
            "Signed Up": new Date().toISOString(),
            Source: "phl-underground-web",
          }),
        ],
        typecast: true,
      });

      return res.status(201).json({ success: true, message: "You're in" });
    } catch (error: any) {
      console.error("Subscribe error:", error?.message || error);
      return res.status(422).json({ error: "Something went wrong. Try again." });
    }
  });

  return httpServer;
}
