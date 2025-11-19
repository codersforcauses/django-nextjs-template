import { FlatCompat } from '@eslint/eslintrc'
import importPlugin from "eslint-plugin-import";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import tsParser from "@typescript-eslint/parser";

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
});

const eslintConfig =[
  ...compat.config({
    extends: ["next/core-web-vitals", "next/typescript"]
  }),
  {
    files: ["**/*.ts", "**/*.tsx"],
    plugins: {
      'simple-import-sort': simpleImportSort,
      import: importPlugin,
    },
    languageOptions: {
      parser: tsParser,
    },
    rules: {
      "simple-import-sort/imports": "warn",
      "simple-import-sort/exports": "warn",
      "import/first": "warn",
      "import/newline-after-import": "warn",
      "import/no-duplicates": "warn",
    },
  },
  {
    ignores: ["node_modules/**", ".next/**", "next-env.d.ts"]
  }
];

export default eslintConfig