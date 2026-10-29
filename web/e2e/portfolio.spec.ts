import { test, expect } from '@playwright/test';

/**
 * Parcours critiques du site public.
 *
 * Ces tests restent volontairement indépendants de l'API Flask : la CI ne
 * démarre pas de backend. Le formulaire est vérifié côté validation navigateur,
 * et les appels réseau éventuels sont couverts par les tests Pytest.
 */
test.describe('portfolio public', () => {
  test('la racine redirige vers la version française', async ({ page }) => {
    await page.goto('/');

    await expect(page).toHaveURL(/\/fr\/$/);
    await expect(page.locator('html')).toHaveAttribute('lang', 'fr');
    await expect(page.getByRole('heading', { level: 1 })).toHaveCount(1);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });

  test('le sélecteur de langue mène à la version anglaise', async ({ page }) => {
    await page.goto('/fr/');

    await page.getByRole('link', { name: 'English', exact: true }).click();

    await expect(page).toHaveURL(/\/en\/$/);
    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });

  test('le filtre projets met à jour le compteur et les boutons', async ({ page }) => {
    await page.goto('/fr/projets/');

    const filter = page.locator('[data-filter-tools]');
    await expect(filter).toBeVisible();

    await page.getByRole('button', { name: 'TypeScript', exact: true }).click();

    await expect(page.locator('[data-filter="TypeScript"]')).toHaveAttribute(
      'aria-pressed',
      'true',
    );
    await expect(page.locator('[data-filter-status]')).toHaveText('1 projet affiché');
    await expect(page.locator('[data-project-item]:visible')).toHaveCount(1);
  });

  test('le formulaire de contact signale les champs invalides', async ({ page }) => {
    await page.goto('/fr/contact/');

    await page.getByRole('button', { name: 'Envoyer le message' }).click();

    await expect(page.locator('#contact-name-error')).toHaveText('Ce champ est obligatoire.');
    await expect(page.locator('#contact-email-error')).toHaveText(
      'Saisissez une adresse email valide.',
    );
    await expect(page.locator('#contact-message-error')).toHaveText(
      'Le message doit contenir au moins 20 caractères.',
    );
    await expect(page.locator('#contact-name')).toBeFocused();
    await expect(page).toHaveURL(/\/fr\/contact\/$/);
  });
});
