/*
  Copyright 2021 ipydrawio contributors

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

module.exports = {
  env: {
    browser: true,
    es6: true,
    commonjs: true,
    node: true,
  },
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier/@typescript-eslint',
    'plugin:react/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: 'tsconfig.eslint.json',
  },
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-floating-promises': ['error', { ignoreVoid: true }],
    // '@typescript-eslint/naming-convention': [
    //   'error',
    //   {
    //     selector: 'interface',
    //     format: ['PascalCase'],
    //     custom: {
    //       regex: '^I[A-Z]',
    //       match: true,
    //     },

    //   },
    // ],
    '@typescript-eslint/no-unused-vars': ['warn', { args: 'none' }],
    '@typescript-eslint/no-use-before-define': 'off',
    '@typescript-eslint/camelcase': 'off',
    '@typescript-eslint/no-explicit-any': 'off',
    '@typescript-eslint/no-non-null-assertion': 'off',
    '@typescript-eslint/no-namespace': 'off',
    '@typescript-eslint/interface-name-prefix': 'off',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/ban-ts-comment': ['warn', { 'ts-ignore': true }],
    '@typescript-eslint/ban-types': 'warn',
    '@typescript-eslint/no-non-null-asserted-optional-chain': 'warn',
    '@typescript-eslint/no-var-requires': 'off',
    '@typescript-eslint/no-empty-interface': 'off',
    '@typescript-eslint/triple-slash-reference': 'warn',
    '@typescript-eslint/no-inferrable-types': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    'no-inner-declarations': 'off',
    'no-prototype-builtins': 'off',
    'no-control-regex': 'warn',
    'no-undef': 'warn',
    'no-case-declarations': 'warn',
    'no-useless-escape': 'off',
    'prefer-const': 'off',
    'react/prop-types': 'warn',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
