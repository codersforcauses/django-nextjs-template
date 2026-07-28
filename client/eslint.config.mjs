import { defineConfig } from "eslint/config";
import tsParser from "@typescript-eslint/parser";
import nextPlugin from "@next/eslint-plugin-next";
import pluginQuery from "@tanstack/eslint-plugin-query";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import importX from "eslint-plugin-import-x";

export default defineConfig([
  {
    ignores: [".next/**", "node_modules/**"],
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    plugins: {
      "@next/next": nextPlugin,
      "simple-import-sort": simpleImportSort,
      import: importX,
    },
    languageOptions: {
      parser: tsParser,
    },
    rules: {
      ...nextPlugin.configs.recommended.rules,
      "simple-import-sort/imports": "warn",
      "simple-import-sort/exports": "warn",
      "import/first": "warn",
      "import/newline-after-import": "warn",
      "import/no-duplicates": "warn",
    },
  },
  ...pluginQuery.configs["flat/recommended"],
]);
