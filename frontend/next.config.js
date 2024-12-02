const nextConfig = {
  rewrites: async () => {
    console.log(process.env.NODE_ENV);
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:5000/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
