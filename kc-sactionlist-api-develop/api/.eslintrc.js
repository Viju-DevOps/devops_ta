module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  overrides: [],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["@typescript-eslint", "prettier"],
  rules: {
    camelcase: "off",
    "no-console": "warn",
    "import/no-commonjs": "off",
    "class-methods-use-this": "off",
    "no-invalid-this": "off",
    "global-require": "off",
    "consistent-return": "off",
    "prettier/prettier": ["warn"],
    "no-unused-vars": [
      "warn",
      { ignoreRestSiblings: true, argsIgnorePattern: "next" },
    ],
    "no-plusplus": ["error", { allowForLoopAfterthoughts: true }],
    "@typescript-eslint/no-var-requires": 0
  },
};
