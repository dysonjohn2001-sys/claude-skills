import { Pool, type QueryResultRow } from "pg";

// One pool per process. Next.js hot-reloads modules in development, so the pool
// is stashed on globalThis to avoid opening a new one on every edit.
const globalForPg = globalThis as unknown as { phgPool?: Pool };

export const pool =
  globalForPg.phgPool ??
  new Pool({
    connectionString: process.env.DATABASE_URL,
    max: Number(process.env.PGPOOL_MAX ?? 10),
    idleTimeoutMillis: 30_000,
    // Reject rather than hang if PostgreSQL is unreachable: a page that errors
    // is better than one that spins.
    connectionTimeoutMillis: 5_000,
  });

if (process.env.NODE_ENV !== "production") globalForPg.phgPool = pool;

export async function query<T extends QueryResultRow>(
  text: string,
  params: unknown[] = [],
): Promise<T[]> {
  const result = await pool.query<T>(text, params);
  return result.rows;
}

export async function queryOne<T extends QueryResultRow>(
  text: string,
  params: unknown[] = [],
): Promise<T | null> {
  const rows = await query<T>(text, params);
  return rows[0] ?? null;
}

/** Run several statements in one transaction. */
export async function transaction<T>(
  fn: (run: <R extends QueryResultRow>(text: string, params?: unknown[]) => Promise<R[]>) => Promise<T>,
): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const result = await fn(async (text, params = []) => (await client.query(text, params)).rows as never);
    await client.query("COMMIT");
    return result;
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
}

/** Queue a background job for the Python worker. */
export async function enqueueJob(
  jobType: string,
  targetType: string,
  targetId: string,
  payload: Record<string, unknown> = {},
): Promise<string> {
  const row = await queryOne<{ id: string }>(
    `INSERT INTO jobs (job_type, target_type, target_id, payload)
     VALUES ($1, $2, $3, $4) RETURNING id`,
    [jobType, targetType, targetId, JSON.stringify(payload)],
  );
  return row!.id;
}

export async function audit(
  actorUserId: string | null,
  action: string,
  entityType: string,
  entityId: string | null,
  metadata: Record<string, unknown> = {},
): Promise<void> {
  await query(
    `INSERT INTO audit_log (actor_user_id, action, entity_type, entity_id, metadata)
     VALUES ($1, $2, $3, $4, $5)`,
    [actorUserId, action, entityType, entityId, JSON.stringify(metadata)],
  );
}
