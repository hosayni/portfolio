/// <reference types="astro/client" />

interface ImportMetaEnv {
  /** "false" masque le formulaire de contact au build (SMTP non configuré). */
  readonly PUBLIC_CONTACT_ENABLED?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
