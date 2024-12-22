const nextJest = require('next/jest')

/** @type {import('jest').Config} */
const createJestConfig = nextJest({
  dir: '.', 
})

const config = {
  clearMocks: true,
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageProvider: "v8",
  testEnvironment: "jsdom",
  testMatch: [
    '**/__tests__/**/*.test.js',
    '**/__tests__/customer/**/*.test.js',
    '**/__tests__/componentsTesting/**/*.test.js',
  ],
  transform: {
    '^.+\\.[tj]sx?$': 'ts-jest',
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/frontend/$1',
    '^@/components/(.*)$': '<rootDir>/frontend/app/(customer)/components/$1',
    '^@/img/(.*)$': '<rootDir>/frontend/app/img/$1',
  },
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: './test-reports',
      outputName: 'junit.xml',
    }],
    ['jest-html-reporter', {
      outputPath: './test-reports/test-report.html',
      pageTitle: 'Test Report',
    }],
  ],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
}

module.exports = createJestConfig(config)
