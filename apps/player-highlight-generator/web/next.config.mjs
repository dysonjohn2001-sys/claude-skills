/** @type {import('next').NextConfig} */
const nextConfig = {
  // Video files are large; the upload route streams to disk rather than
  // buffering, so the body-size limit applies only to form fields.
  experimental: {
    serverActions: { bodySizeLimit: "4mb" },
  },
  // This is a private application. Nothing here should be indexed or embedded.
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Robots-Tag", value: "noindex, nofollow, noarchive" },
          { key: "X-Frame-Options", value: "SAMEORIGIN" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "same-origin" },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=(), interest-cohort=()",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
