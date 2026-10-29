#!/usr/bin/env node
/**
 * Vérifie `npm audit --json` en tenant compte d'une liste d'exceptions datées.
 *
 * Politique :
 * - toute vulnérabilité haute ou critique non documentée fait échouer la CI ;
 * - une exception expirée, devenue obsolète ou dont la gravité a changé échoue
 *   aussi, pour forcer une revue régulière ;
 * - les vulnérabilités basses et modérées sont signalées sans bloquer.
 *
 * Usage :
 *   node .github/scripts/check-npm-audit.mjs <audit.json> <allowlist.json>
 */

import { readFile } from 'node:fs/promises';

const RANK = { info: 0, low: 1, moderate: 2, high: 3, critical: 4 };
const BLOCKING = new Set(['high', 'critical']);

const [auditPath, allowlistPath] = process.argv.slice(2);

if (!auditPath || !allowlistPath) {
  console.error('Usage: node .github/scripts/check-npm-audit.mjs <audit.json> <allowlist.json>');
  process.exit(2);
}

const readJson = async (path) => {
  try {
    return JSON.parse(await readFile(path, 'utf8'));
  } catch (error) {
    console.error(`Impossible de lire ${path} : ${error.message}`);
    process.exit(2);
  }
};

const audit = await readJson(auditPath);
const allowlist = await readJson(allowlistPath);

if (audit.error) {
  console.error(`npm audit a échoué : ${JSON.stringify(audit.error)}`);
  process.exit(2);
}

const today = new Date().toISOString().slice(0, 10);
const defaultExpiry = allowlist.expires;
const exceptions = new Map((allowlist.advisories ?? []).map((entry) => [entry.id, entry]));

// Les paquets agrègent les avis de leurs dépendances : on ne garde que les avis
// réels (objets `via`), dédupliqués par identifiant GHSA.
const advisories = new Map();
for (const vulnerability of Object.values(audit.vulnerabilities ?? {})) {
  for (const via of vulnerability.via ?? []) {
    if (typeof via !== 'object' || !via.url) continue;
    const id = via.url.split('/').pop();
    if (!advisories.has(id)) {
      advisories.set(id, {
        id,
        package: via.name,
        severity: via.severity,
        title: via.title,
        url: via.url,
      });
    }
  }
}

const errors = [];
const warnings = [];
const seen = new Set();
let allowed = 0;

for (const advisory of [...advisories.values()].sort(
  (a, b) => (RANK[b.severity] ?? 0) - (RANK[a.severity] ?? 0),
)) {
  if (!BLOCKING.has(advisory.severity)) {
    warnings.push(`${advisory.severity} ${advisory.id} (${advisory.package}) — non bloquant`);
    continue;
  }

  const exception = exceptions.get(advisory.id);
  if (!exception) {
    errors.push(
      `${advisory.severity} ${advisory.id} (${advisory.package}) non documenté — ${advisory.url}`,
    );
    continue;
  }

  seen.add(advisory.id);

  if (exception.package && exception.package !== advisory.package) {
    errors.push(
      `L'exception ${advisory.id} vise ${exception.package}, mais l'avis concerne ${advisory.package}.`,
    );
    continue;
  }

  if (RANK[exception.severity] !== RANK[advisory.severity]) {
    errors.push(
      `La gravité de ${advisory.id} a changé (${exception.severity} → ${advisory.severity}) : revoir l'exception.`,
    );
    continue;
  }

  const expiry = exception.expires ?? defaultExpiry;
  if (!expiry || expiry < today) {
    errors.push(`L'exception ${advisory.id} a expiré le ${expiry ?? 'date inconnue'} : revoir ou corriger.`);
    continue;
  }

  allowed += 1;
  console.log(`OK  ${advisory.severity.padEnd(8)} ${advisory.id} (${advisory.package}) — exception jusqu'au ${expiry}`);
}

for (const id of exceptions.keys()) {
  if (!seen.has(id)) {
    warnings.push(`Exception ${id} inutilisée : la retirer de la liste.`);
  }
}

for (const warning of warnings) console.warn(`ATTENTION  ${warning}`);

const counts = audit.metadata?.vulnerabilities ?? {};
const blocking = [...advisories.values()].filter((advisory) => BLOCKING.has(advisory.severity));
console.log(
  `\nRésumé : ${advisories.size} avis (${blocking.length} hauts/critiques) sur ` +
    `${counts.total ?? '?'} paquets vulnérables, ${allowed} exception(s) acceptée(s), ` +
    `${errors.length} problème(s) bloquant(s).`,
);

if (errors.length > 0) {
  console.error('\nÉchec de l’audit npm :');
  for (const error of errors) console.error(`  - ${error}`);
  console.error('\nCorriger les dépendances ou documenter une exception dans .github/security/npm-audit-allowlist.json.');
  process.exit(1);
}

console.log('Audit npm conforme à la politique de sécurité.');
