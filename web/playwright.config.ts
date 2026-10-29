import { defineConfig, devices } from '@playwright/test';

/**
 * Tests de bout en bout sur le build de production.
 *
 * Le serveur `astro preview` sert `dist/` : les tests valident exactement les
 * fichiers qui partiront en production, pas le serveur de développement.
 * En CI, `web/dist` est récupéré depuis l'artefact du job `web`.
 */
export default defineConfig({
  testDir: './e2e',
  outputDir: './test-results',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI
    ? [['github'], ['html', { outputFolder: 'playwright-report', open: 'never' }]]
    : [['list'], ['html', { outputFolder: 'playwright-report', open: 'never' }]],
  use: {
    baseURL: 'http://127.0.0.1:4321',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    locale: 'fr-FR',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run preview -- --host 127.0.0.1 --port 4321',
    url: 'http://127.0.0.1:4321/fr/',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
