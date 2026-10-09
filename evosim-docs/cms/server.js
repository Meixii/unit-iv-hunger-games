/**
 * EvoSim Docs CMS: Self-hosted documentation admin app.
 *
 * Edits JSON files in content/, accepts image uploads, and triggers static builds.
 */

import express from "express";
import crypto from "node:crypto";
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawn, execFile } from "node:child_process";
import { schema } from "./schema.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CONTENT_DIR = path.join(ROOT, "content");
const PUBLIC_DIR = path.join(ROOT, "public");
const DIST_DIR = path.join(ROOT, "dist");
const UPLOADS_DIR = path.join(PUBLIC_DIR, "uploads");
const DATA_DIR = path.join(__dirname, "data");

loadEnv(path.join(__dirname, ".env"));

const PORT = Number(process.env.PORT || 4001);
const PASSWORD = process.env.CMS_PASSWORD || "changeme";
const SECRET = process.env.CMS_SECRET || crypto.randomBytes(32).toString("hex");
const SERVE_DIST = process.env.SERVE_DIST === "true";
const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000;
const MAX_UPLOAD_BYTES = 8 * 1024 * 1024;
const UPLOAD_EXT = [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"];

function loadEnv(file) {
  if (!fs.existsSync(file)) return;
  if (!fs.statSync(file).isFile()) return;
  for (const line of fs.readFileSync(file, "utf8").split("\n")) {
    const trimmed = line.trim();
    if (trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const [k, ...v] = trimmed.split("=");
    const key = k.trim();
    const val = v.join("=").trim().replace(/^["']|["']$/g, "");
    if (!(key in process.env)) process.env[key] = val;
  }
}

/* ------------------------------------------------------------------ auth */

function makeToken() {
  const expiresAt = Date.now() + SESSION_TTL_MS;
  const payload = `${expiresAt}`;
  const sig = crypto.createHmac("sha256", SECRET).update(payload).digest("hex");
  return `${payload}.${sig}`;
}

function verifyToken(token) {
  if (!token || typeof token !== "string") return false;
  const [expiresAtStr, sig] = token.split(".");
  if (!expiresAtStr || !sig) return false;
  const expiresAt = Number(expiresAtStr);
  if (!Number.isFinite(expiresAt) || Date.now() > expiresAt) return false;
  const expected = crypto.createHmac("sha256", SECRET).update(expiresAtStr).digest("hex");
  return safeEqual(sig, expected);
}

function safeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string") return false;
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
}

function getCookie(req, name) {
  const header = req.headers.cookie;
  if (!header) return null;
  for (const pair of header.split(";")) {
    const [k, v] = pair.trim().split("=");
    if (k === name) return decodeURIComponent(v || "");
  }
  return null;
}

function requireAuth(req, res, next) {
  if (!verifyToken(getCookie(req, "cms_session"))) {
    return res.status(401).json({ error: "Unauthorized. Please sign in." });
  }
  next();
}

/* --------------------------------------------------------------- content */

function getKey(key) {
  return schema[key] || null;
}

async function readContent(key) {
  const file = path.join(CONTENT_DIR, getKey(key).file);
  return JSON.parse(await fsp.readFile(file, "utf8"));
}

async function writeContent(key, value) {
  const file = path.join(CONTENT_DIR, getKey(key).file);
  const tmp = `${file}.tmp`;
  await fsp.writeFile(tmp, JSON.stringify(value, null, 2) + "\n", "utf8");
  await fsp.rename(tmp, file);
  return file;
}

/**
 * Git auto-commit helper.
 * Supports both standalone repository and monorepo structure (checks ROOT and ROOT/..).
 */
function autoCommit(relPaths, message) {
  let gitDir = null;
  let workTree = ROOT;
  if (fs.existsSync(path.join(ROOT, ".git"))) {
    gitDir = path.join(ROOT, ".git");
    workTree = ROOT;
  } else if (fs.existsSync(path.join(ROOT, "..", ".git"))) {
    gitDir = path.join(ROOT, "..", ".git");
    workTree = path.resolve(ROOT, "..");
  }
  if (!gitDir) return;

  const git = (args) =>
    new Promise((resolve) => {
      execFile("git", ["-C", workTree, ...args], { timeout: 15000 }, (error, stdout, stderr) =>
        resolve({ error, stderr })
      );
    });

  (async () => {
    try {
      await git(["add", "--", ...relPaths]);
      const res = await git([
        "-c", "user.name=EvoSim Docs CMS",
        "-c", "user.email=cms@evosim.local",
        "commit", "-m", message,
      ]);
      if (res.error) {
        if (!/nothing to commit/.test(res.stderr || "")) {
          console.warn(`Auto-commit note: ${(res.stderr || res.error.message || "").trim()}`);
        }
      } else {
        console.log(`Auto-committed: ${message}`);
      }
    } catch (err) {
      console.warn(`Auto-commit error: ${err.message}`);
    }
  })();
}

function getPath(obj, dotPath) {
  return dotPath.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);
}

function validateField(field, value, fullPath, errors) {
  if (value === undefined) {
    if (field.optional) return;
    errors.push(`${fullPath}: is missing`);
    return;
  }
  switch (field.type) {
    case "text":
    case "textarea":
    case "url":
      if (typeof value !== "string") errors.push(`${fullPath}: expected text`);
      break;
    case "number":
      if (typeof value !== "number" || !Number.isFinite(value)) {
        errors.push(`${fullPath}: expected a number`);
      }
      break;
    case "toggle":
      if (typeof value !== "boolean") errors.push(`${fullPath}: expected true or false`);
      break;
    case "select": {
      const allowed = field.options.map((o) => o.value);
      if (value !== "" && !allowed.includes(value)) {
        errors.push(`${fullPath}: must be one of ${allowed.join(", ")}`);
      }
      break;
    }
    case "image":
      if (typeof value !== "string") {
        errors.push(`${fullPath}: expected text (uploaded path or URL)`);
      }
      break;
    case "list": {
      if (!Array.isArray(value)) {
        errors.push(`${fullPath}: expected a list`);
        break;
      }
      if (field.itemType === "string") {
        value.forEach((item, i) => {
          if (typeof item !== "string") errors.push(`${fullPath}.${i}: expected text`);
        });
      } else if (field.itemFields) {
        value.forEach((item, i) => {
          if (typeof item !== "object" || item === null || Array.isArray(item)) {
            errors.push(`${fullPath}.${i}: expected an item object`);
            return;
          }
          validateFields(field.itemFields, item, `${fullPath}.${i}`, errors);
        });
      }
      break;
    }
    default:
      errors.push(`${fullPath}: unknown field type`);
  }
}

function validateFields(fields, data, prefix, errors) {
  for (const field of fields) {
    const fullPath = prefix ? `${prefix}.${field.name}` : field.name;
    validateField(field, getPath(data, field.name), fullPath, errors);
  }
}

/* ---------------------------------------------------------------- rebuild */

const build = { running: false, lastCode: null, log: "" };

function tailLog(n = 3000) {
  return build.log.length > n ? build.log.slice(-n) : build.log;
}

function startBuild() {
  if (build.running) return false;
  build.running = true;
  build.log = `$ npm run build\n`;
  const proc = spawn("npm", ["run", "build"], {
    cwd: ROOT,
    shell: process.platform === "win32",
    env: process.env,
  });
  proc.stdout.on("data", (d) => {
    build.log += d.toString();
  });
  proc.stderr.on("data", (d) => {
    build.log += d.toString();
  });
  proc.on("error", (err) => {
    build.log += `\nFailed to start build: ${err.message}\n`;
    build.running = false;
    build.lastCode = 1;
  });
  proc.on("close", (code) => {
    build.log += `\n$ exit ${code}\n`;
    build.running = false;
    build.lastCode = code;
  });
  return true;
}

/* ------------------------------------------------------------------ app */

const app = express();
app.disable("x-powered-by");
app.use(express.json({ limit: "12mb" }));

app.post("/api/login", (req, res) => {
  const { password } = req.body || {};
  if (!password || !safeEqual(password, PASSWORD)) {
    return res.status(401).json({ error: "Wrong password." });
  }
  res.setHeader(
    "Set-Cookie",
    `cms_session=${makeToken()}; HttpOnly; Path=/; SameSite=Lax; Max-Age=${SESSION_TTL_MS / 1000}`
  );
  res.json({ ok: true });
});

app.post("/api/logout", (req, res) => {
  res.setHeader("Set-Cookie", "cms_session=; HttpOnly; Path=/; SameSite=Lax; Max-Age=0");
  res.json({ ok: true });
});

app.get("/api/session", (req, res) => {
  if (verifyToken(getCookie(req, "cms_session"))) {
    return res.json({ signedIn: true, serveDist: SERVE_DIST });
  }
  res.status(401).json({ signedIn: false });
});

app.get("/api/schema", requireAuth, (req, res) => {
  res.json(schema);
});

app.get("/api/content/:key", requireAuth, (req, res) => {
  if (!getKey(req.params.key)) return res.status(404).json({ error: "Unknown page." });
  readContent(req.params.key)
    .then((value) => res.json(value))
    .catch(() => res.status(500).json({ error: "Could not read content file." }));
});

app.put("/api/content/:key", requireAuth, (req, res) => {
  const def = getKey(req.params.key);
  if (!def) return res.status(404).json({ error: "Unknown page." });
  const value = req.body?.value;
  if (typeof value !== "object" || value === null) {
    return res.status(400).json({ error: "Body must be { value: {...} }." });
  }
  const errors = [];
  if (def.fields) {
    validateFields(def.fields, value, "", errors);
  }
  if (errors.length > 0) {
    return res.status(400).json({ error: "Some fields are invalid.", details: errors });
  }
  writeContent(req.params.key, value)
    .then((file) => {
      autoCommit([file], `content: update ${def.label.toLowerCase()}`);
      res.json({ ok: true });
    })
    .catch(() => res.status(500).json({ error: "Could not write content file." }));
});

app.post("/api/upload", requireAuth, (req, res) => {
  const { name, data } = req.body || {};
  if (typeof name !== "string" || typeof data !== "string") {
    return res.status(400).json({ error: "Expected { name, data } with a base64 data URL." });
  }
  const match = /^data:([\w./+-]+);base64,(.+)$/.exec(data);
  const buffer = match
    ? Buffer.from(match[2], "base64")
    : Buffer.from(data.replace(/\s/g, ""), "base64");
  if (buffer.length === 0) return res.status(400).json({ error: "Empty upload." });
  if (buffer.length > MAX_UPLOAD_BYTES) {
    return res.status(413).json({ error: "File exceeds 8 MB." });
  }
  let ext = path.extname(name).toLowerCase();
  if (!UPLOAD_EXT.includes(ext) && match) {
    const fromMime = {
      "image/png": ".png",
      "image/jpeg": ".jpg",
      "image/webp": ".webp",
      "image/gif": ".gif",
      "image/svg+xml": ".svg",
      "image/avif": ".avif"
    };
    ext = fromMime[match[1]] || "";
  }
  if (!UPLOAD_EXT.includes(ext)) {
    return res.status(415).json({ error: `Allowed types: ${UPLOAD_EXT.join(" ")}` });
  }
  const base = path
    .basename(name, path.extname(name))
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60) || "asset";
  const filename = `${base}-${Date.now()}${ext}`;
  const dest = path.join(UPLOADS_DIR, filename);

  fsp.mkdir(UPLOADS_DIR, { recursive: true })
    .then(() => fsp.writeFile(dest, buffer))
    .then(() => {
      autoCommit([dest], "content: upload image");
      res.json({ ok: true, path: `/uploads/${filename}` });
    })
    .catch((err) => {
      res.status(500).json({ error: `Could not save file: ${err.message}` });
    });
});

app.post("/api/rebuild", requireAuth, (req, res) => {
  if (!startBuild()) return res.status(409).json({ error: "A build is already running." });
  res.json({ ok: true, running: true });
});

app.get("/api/rebuild/status", requireAuth, (req, res) => {
  res.json({ running: build.running, lastCode: build.lastCode, tail: tailLog() });
});

/* ---------------------------------------------------------------- static */

app.get("/admin", (req, res) => res.sendFile(path.join(__dirname, "public", "admin.html")));
app.use("/admin", express.static(path.join(__dirname, "public"), { index: false }));

if (!SERVE_DIST) app.get("/", (req, res) => res.redirect("/admin"));

app.use("/uploads", express.static(UPLOADS_DIR, { maxAge: "1h" }));
app.get("/favicon.ico", (req, res) => {
  const ico = path.join(PUBLIC_DIR, "favicon.ico");
  if (fs.existsSync(ico)) res.sendFile(ico);
  else res.status(404).end();
});

if (SERVE_DIST) {
  app.use(express.static(DIST_DIR, { maxAge: "1h", index: "index.html" }));
  app.use((req, res, next) => {
    if (req.method !== "GET" || !req.headers.accept?.includes("text/html")) return next();
    const notFound = path.join(DIST_DIR, "404.html");
    if (fs.existsSync(notFound)) return res.status(404).sendFile(notFound);
    next();
  });
}

fs.mkdirSync(DATA_DIR, { recursive: true });
app.listen(PORT, () => {
  console.log(`EvoSim Docs CMS running on http://localhost:${PORT}`);
  if (SERVE_DIST) console.log(`Serving Astro build from ${DIST_DIR}`);
});
