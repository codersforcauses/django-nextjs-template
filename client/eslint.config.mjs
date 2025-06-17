import { defineConfig } from "eslint/config";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import _import from "eslint-plugin-import";
import { fixupPluginRules } from "@eslint/compat";
import tsParser from "@typescript-eslint/parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default defineConfig([
  {
    files: ["**/*.ts", "**/*.tsx"],
    extends: compat.extends(
      "plugin:@next/next/recommended",
      "plugin:@tanstack/eslint-plugin-query/recommended",
    ),

    plugins: {
      "simple-import-sort": simpleImportSort,
      import: fixupPluginRules(_import),
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
]);
