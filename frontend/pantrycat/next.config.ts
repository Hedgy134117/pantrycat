import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
  reactStrictMode: true,
  env: {
    BASE_URL: process.env.BASE_URL,
  }
};

export default nextConfig;
