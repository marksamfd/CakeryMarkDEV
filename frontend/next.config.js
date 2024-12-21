const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
