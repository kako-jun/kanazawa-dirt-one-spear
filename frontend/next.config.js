/** @type {import('next').NextConfig} */
const isGithubPages = process.env.GITHUB_PAGES === 'true'

const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: isGithubPages && process.env.NODE_ENV === 'production' ? '/kanazawa-dirt-one-spear' : '',
}

module.exports = nextConfig
