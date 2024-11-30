const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination:
          process.env.NODE_ENV === 'DEV'
            ? 'http://127.0.0.1:5000/api/:path*'
            : '/api/', // to be edited on deployment
      },
    ];
  },
};

module.exports = nextConfig;
