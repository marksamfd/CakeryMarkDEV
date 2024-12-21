const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND}/:path*`,
      },
    ];
  },
  images: {
    domains: [
      'github.com',
      'cdn.pixabay.com',
      'blogger.googleusercontent.com',
    ],
  },
};

module.exports = nextConfig;
