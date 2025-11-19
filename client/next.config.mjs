// import os from "node:os";
// import isInsideContainer from "is-inside-container";

// const isWindowsDevContainer = () =>
//   os.release().toLowerCase().includes("microsoft") && isInsideContainer();

/** @type {import('next').NextConfig} */

const config = {
  reactStrictMode: true,
  turbopack: {
    root: import.meta.dirname,
  }
  // Turns on file change polling for the Windows Dev Container
  // Doesn't work currently for turbopack, so file changes will not automatically update the client.
    // watchOptions: isWindowsDevContainer()
    // ? {
    //     pollIntervalMs: 1000
    //   }
    // : undefined,
};

export default config;
